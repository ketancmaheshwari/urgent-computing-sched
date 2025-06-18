#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import plotly.express as px
import argparse

def convert_to_numbers(x):
    if isinstance(x, str):
        x = x.strip().upper()
        if x.endswith("K"):
            return float(x[:-1]) * 1000
    return pd.to_numeric(x, errors='coerce')

def load_data(file):

    data = pd.read_csv(file)

    data.columns = ['UID','GID','JobIDRaw','Group','Account','JobName','TimelimitRaw','Submit','Start','End','State','ExitCode',
                    'ReservationId','Reservation','Priority','Eligible','Constraints','SystemCPU','CPUTimeRAW','ElapsedRaw',
                    'Layout','NTasks','QOSREQ','QOS','Restarts','WorkDir','ConsumedEnergyRaw','FailedNode','AveDiskRead',
                    'AveDiskWrite','MaxDiskRead','MaxDiskWrite','Partition','Reason','Suspended','AllocNodes','AveRSS','MaxRSS',
                    'DerivedExitCode','AveVMSize','MaxVMSize','ReqMem','ReqNodes','NNodes','Planned','PlannedCPURAW','NCPUS',
                    'UserCPU','ReqCPUS','TotalCPU','TRESUsageInTot','TRESUsageOutTot','ReqTRES','AllocTRES','TRESUsageInMax',
                    'TRESUsageOutMax','Flags','Comment','SystemComment','AdminComment']

    data = data.sort_values(by=['JobIDRaw'], ascending=True)

    return data


def main():

    parser = argparse.ArgumentParser(description="Process command-line arguments.")
    parser.add_argument("--infile", help="Path to the input csv file.")
    parser.add_argument("--outfile", help="Path to the output html file.")

    args = parser.parse_args()

    #print(f"Input file: {args.infile}")
    #print(f"Output file: {args.outfile}")

    if not args.infile:
        raise ValueError("Input file must be specified with --infile argument.")
    if not args.outfile:
        raise ValueError("Output file must be specified with --outfile argument.")

    data = load_data(args.infile)

    uid_job_counts = {}

    for uid in data['UID']:
        if uid in uid_job_counts:
            uid_job_counts[uid] += 1
        else:
            uid_job_counts[uid] = 1

    data['NormalizedState'] = data['State'].str.split().str[0]

    states = []
    for state in data['NormalizedState']:
        if pd.notna(state) and state not in states:
            states.append(state)

    grouped = data.value_counts(['UID', 'NormalizedState']).reset_index(name="Count")

    #This makes the x axis categorical instead of continuous, which makes it readable
    #Without this line, bars are too skinny to see
    grouped['UID'] = grouped['UID'].astype(str)

    bar = px.bar(grouped, x='UID', y='Count', color='NormalizedState',
                title='Jobs Submitted per User',
                labels={'Count': 'Number of Jobs Submitted', 'UID': 'User ID', 'NormalizedState': 'Job State'},
                category_orders={'NormalizedState': states})

    bar.update_xaxes(showticklabels=False)
    bar.write_html(args.outfile)

if __name__ == "__main__":
    main()

