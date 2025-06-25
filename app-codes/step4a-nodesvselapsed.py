#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots 
import plotly.graph_objects as go
import argparse


def convert_to_numbers(x):
    if isinstance(x, str):
        x = x.strip().upper()
        if x.endswith("K"):
            return float(x[:-1]) * 1000
    return pd.to_numeric(x, errors='coerce')


def create_scatter(df):
    df = df.copy()

    if len(df.columns) >= 2:
        df.rename(columns={df.columns[0]: "Elapsed Time", df.columns[1]: "Nodes"}, inplace=True)
    else:
        raise ValueError("DataFrame must have at least two columns.")

    df["Elapsed Time"] = df["Elapsed Time"].apply(convert_to_numbers)
    df["Nodes"] = df["Nodes"].apply(convert_to_numbers)
    df = df.dropna(subset=["Elapsed Time", "Nodes"])

    if df.empty:
        print("DataFrame is empty after processing. No scatter plot will be generated.")
        return None

    scatter_plot = px.scatter(
        df,
        x='Elapsed Time',
        y='Nodes',
        title='Elapsed Time(s) vs Requested Nodes',
        log_x=True
    )
    scatter_plot.update_layout(
        xaxis=dict(range=[np.log10(10), np.log10(1000)])
    )

    return scatter_plot


def plot_heatmap(df):
    df = df.copy()
    df['Elapsed Time'] = pd.to_numeric(df['Elapsed Time'], errors='coerce')
    df['Nodes'] = pd.to_numeric(df['Nodes'], errors='coerce')
    df = df.dropna(subset=['Elapsed Time', 'Nodes'])

    if df.empty:
        print("DataFrame is empty after numeric conversion. No heatmap will be generated.")
        return None

    counts, xedges, yedges = np.histogram2d(df['Elapsed Time'], df['Nodes'], bins=[25, 25])
    counts_log = np.log1p(counts)

    hover_text = [
        [
            f"Elapsed Time: {xedges[i]:.0f}–{xedges[i+1]:.0f}<br>"
            f"Nodes: {yedges[j]:.0f}–{yedges[j+1]:.0f}<br>"
            f"Count: {int(counts[i, j])}<br>"
            f"Log(Count+1): {counts_log[i, j]:.2f}"
            for j in range(counts.shape[1])
        ]
        for i in range(counts.shape[0])
    ]
    hover_text = np.array(hover_text).T

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Log-scaled Heatmap", "Linear-scaled Heatmap"),
        shared_yaxes=True
    )

    fig.add_trace(
        go.Heatmap(
            z=counts_log.T,
            x=np.round(xedges[:-1], 1),
            y=np.round(yedges[:-1], 1),
            text=hover_text,
            hoverinfo='text',
            colorscale='Hot',
            colorbar=dict(
                title='Log(Count+1)',
                len=0.8,
                y=0.5,
                x=0.46,
                xanchor='left'
            )
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Heatmap(
            z=counts.T,
            x=np.round(xedges[:-1], 1),
            y=np.round(yedges[:-1], 1),
            text=hover_text,
            hoverinfo='text',
            colorscale='Hot',
            colorbar=dict(
                title='Raw Count',
                len=0.8,
                y=0.5,
                x=1.02,
                xanchor='left'
            )
        ),
        row=1, col=2
    )

    fig.update_layout(
        title={
            'text': 'Elapsed Time(s) vs Requested Nodes Heatmaps<br><sub>Left: Log-scaled; Right: Linear-scaled</sub>',
            'x': 0.5
        },
        xaxis_title='Elapsed Time',
        yaxis_title='Nodes',
        xaxis2_title='Elapsed Time',
        height=600,
        width=1500
    )

    return fig


def load_data(file):
    df = pd.read_csv(file)
    df.columns = ['Elapsed Time', 'Nodes']
    return df


def main():
    parser = argparse.ArgumentParser(description="Generate scatter and heatmap plots.")
    parser.add_argument("--infile", help="Path to the input csv file.", required=True)
    parser.add_argument("--outfile", help="Path to the output html file.", required=True)
    args = parser.parse_args()

    if not args.infile:
        raise ValueError("Input file must be specified with --infile argument.")
    if not args.outfile:
        raise ValueError("Output file must be specified with --outfile argument.")
    
    print(f"Input file: {args.infile}")
    print(f"Output file: {args.outfile}")

    data = load_data(args.infile)

    scatter_plot = create_scatter(data)
    scatter_plot.write_html(f"scatter_{args.outfile}")

    heatmap_plot = plot_heatmap(data)
    heatmap_plot.write_html(f"heatmap_{args.outfile}")


if __name__ == "__main__":
    main()
