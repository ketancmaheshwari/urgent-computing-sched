#!/usr/bin/env python
# coding: utf-8

# To run: python step4b-jobwaittimes.py --infile ../data/frontier-jobs-data-2024.csv --outfile plot.html

import argparse
import pandas as pd
import plotly.express as px
import csv

def convert_to_numbers(x):
    if isinstance(x, str):
        x = x.strip().upper()
        if x.endswith("K"):
            return float(x[:-1]) * 1000
    return pd.to_numeric(x, errors='coerce')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--infile",  help="Path to input data")
    parser.add_argument("--outfile", help="Path to output html")
    args = parser.parse_args()
    
    data = pd.read_csv(args.infile)
    data.columns = ['UID','GID','JobIDRaw','Group','Account','JobName','TimelimitRaw','Submit','Start','End','State','ExitCode',
                    'ReservationId','Reservation','Priority','Eligible','Constraints','SystemCPU','CPUTimeRAW','ElapsedRaw',
                    'Layout','NTasks','QOSREQ','QOS','Restarts','WorkDir','ConsumedEnergyRaw','FailedNode','AveDiskRead',
                    'AveDiskWrite','MaxDiskRead','MaxDiskWrite','Partition','Reason','Suspended','AllocNodes','AveRSS','MaxRSS',
                    'DerivedExitCode','AveVMSize','MaxVMSize','ReqMem','ReqNodes','NNodes','Planned','PlannedCPURAW','NCPUS',
                    'UserCPU','ReqCPUS','TotalCPU','TRESUsageInTot','TRESUsageOutTot','ReqTRES','AllocTRES','TRESUsageInMax',
                    'TRESUsageOutMax','Flags','Comment','SystemComment','AdminComment']
    
    data = data.dropna(subset=['JobIDRaw', 'Submit', 'Start'])
    
    #Removes Na values in JobIDRaw, Submit, Start
    data = data.sort_values(by=['JobIDRaw'], ascending=True)
    
    data['Start'] = pd.to_datetime(data["Start"], format='%Y-%m-%dT%H:%M:%S', errors='coerce')
    data['Start'] = (data["Start"] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1m')
    data['Submit'] = pd.to_datetime(data['Submit'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')
    data['Submit'] = (data['Submit'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1m')
    
    wait_times = []
    
    for i in range(len(data)):
        wait = data.iloc[i]['Start'] - data.iloc[i]['Submit']
        wait_times.append(wait)
    
    plot = px.line(data, x=data['JobIDRaw'], y=wait_times, color=data['State'],
                        title='Job Wait Times 2024',
                        labels={'x': 'JobID', 'y': 'Wait Time (mins)'},
                        color_discrete_map={'timeout': 'black'})
    
    plot.update_traces(mode='markers', marker=dict(size=6))
    plot.update_layout(xaxis=dict(range=[1346844, 2020113]))
    plot.update_layout(yaxis=dict(range=[-1, 200000]))
    plot.update_xaxes(showticklabels=False)
    
    plot.write_html(args.outfile)

if __name__=="__main__":
    main()

