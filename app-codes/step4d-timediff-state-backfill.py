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
    data.columns = ['Diffsec', 'Nodes', 'State', 'Backfilled']
    return data


def main():
    parser = argparse.ArgumentParser(description="Process command-line arguments and generate a plot.")
    parser.add_argument("--infile", help="Path to the input CSV file.", required=True)
    parser.add_argument("--outfile", help="Path to the output HTML file.", required=True)

    args = parser.parse_args()

    print(f"Input file: {args.infile}")
    print(f"Output file: {args.outfile}")

    data = load_data(args.infile)

    color_map = {
        'COMPLETED': 'green',
        'FAILED/NODE_FAIL': 'red',
        'TIMEOUT': 'yellow',
        'OUT_OF_MEMORY': 'orange',
        'RESIZING/REQUEUED': 'blue',
        'CANCELLED': 'black'
    }

    state_group_map = {
        'FAILED': 'FAILED/NODE_FAIL',
        'NODE_FAIL': 'FAILED/NODE_FAIL',
        'RESIZING': 'RESIZING/REQUEUED',
        'REQUEUED': 'RESIZING/REQUEUED',
        'CANCELLED': 'CANCELLED',
        'COMPLETED': 'COMPLETED',
        'TIMEOUT': 'TIMEOUT',
        'OUT_OF_MEMORY': 'OUT_OF_MEMORY'
    }

    data['Nodes'] = data['Nodes'].apply(convert_to_numbers)

    data['State'] = data['State'].astype(str).str.replace(r'^CANCELLED.*', 'CANCELLED', regex=True)
    data['clean_state'] = data['State'].map(state_group_map)

    data['Backfilled'] = data['Backfilled'].astype(str).str.lower()
    data['backfilled_label'] = data['Backfilled'].apply(lambda x: 'yes' if x == 'yes' else 'no')

    try:
        year_from_filename = args.infile.split('/')[-1][:4]
        plot_title_year_part = f" for {year_from_filename}" if year_from_filename.isdigit() else ""
    except:
        plot_title_year_part = ""

    fig = px.scatter(
        data,
        x='Nodes',
        y='Diffsec', 
        color='clean_state',
        symbol='backfilled_label',
        color_discrete_map=color_map,
        symbol_sequence=['circle', 'cross'],
        title=f"Node vs Wait Time - Actual Time Difference (s){plot_title_year_part}"
    )

    for trace in fig.data:
        if isinstance(trace.name, str) and ',' in trace.name:
            parts = [part.strip() for part in trace.name.split(',')]
            state = parts[0]
            backfilled = parts[1]
        elif isinstance(trace.name, str):
            state = trace.name
            backfilled = 'no'

        backfilled_text = '(Backfilled)' if backfilled == 'yes' else ''
        trace.name = f"{state} {backfilled_text}"

    fig.update_xaxes(title_text='Number of Nodes', tickformat='~s')
    fig.update_yaxes(title_text='Time Difference (s)')

    fig.update_layout(
        #height=800, 
        #width=1000, 
        legend_title_text='Job State',
        showlegend=True,
    )

    fig.write_html(args.outfile)

if __name__ == "__main__":
    main()
