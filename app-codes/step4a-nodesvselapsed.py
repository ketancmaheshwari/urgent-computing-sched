#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import plotly.express as px
import csv
import numpy as np

cleaned_backfilled_data_by_year = {}

#Helper Methods
def convert_to_numbers(x):
    if isinstance(x, str):
        x = x.strip().upper()
        if x.endswith("K"):
            return float(x[:-1]) * 1000
    return pd.to_numeric(x, errors='coerce')

def create_scatter(data_dict):
    processed_dfs = []
    all_individual_plots = []
    combined_backfilled_plot = None

    # Iterate through the dictionary to access each DataFrame
    for year, df_original in data_dict.items():
        df = df_original.copy()

        if len(df.columns) >= 2:
            df.rename(columns={df.columns[0]: "Elapsed", df.columns[1]: "Nodes"}, inplace=True)
        else:
            print(f"Warning: DataFrame for {year} has fewer than 2 columns. Skipping individual plot creation.")
            all_individual_plots.append(None)
            continue

        # Convert 'Elapsed' and 'Nodes' to numeric, handling 'K' suffix
        df["Elapsed"] = df["Elapsed"].apply(convert_to_numbers)
        df["Nodes"] = df["Nodes"].apply(convert_to_numbers)

        df = df.dropna(subset=["Elapsed", "Nodes"])

        processed_dfs.append(df)

        # Create and show individual scatter plot for the current year
        if not df.empty:
            backfilled_plot = px.scatter(
                df,
                x='Elapsed',
                y='Nodes',
                title=f'Elapsed vs Nodes ({year})',
                log_x=True,
            )
            backfilled_plot.update_layout(
                xaxis=dict(range=[np.log10(10), np.log10(1000)])
            )
            #backfilled_plot.show()
            all_individual_plots.append(backfilled_plot)
        else:
            print(f"  DataFrame for {year} is empty after processing. Skipping individual plot creation.")
            all_individual_plots.append(None)

    if processed_dfs:
        combined_backfilled_data = pd.concat(processed_dfs)
        combined_backfilled_data = combined_backfilled_data.dropna(subset=["Elapsed", "Nodes"])

        if not combined_backfilled_data.empty:
            combined_backfilled_plot = px.scatter(
                combined_backfilled_data,
                x='Elapsed',
                y='Nodes',
                color='Year',
                title='Elapsed vs Nodes (All Years)',
                log_x=True,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            combined_backfilled_plot.update_layout(
                xaxis=dict(range=[np.log10(10), np.log10(1000)])
            )
            #combined_backfilled_plot.show()
        else:
            print("\nCombined DataFrame is empty after processing. Skipping combined plot.")
    else:
        print("\nNo dataframes were successfully processed for combined plotting.")

    return all_individual_plots, combined_backfilled_plot


cleaned_year_files = { 
    '2021': "/Users/km0/gitrepos/andy-borch-work/Data/CleanedBackfilled/cleaned-2021-backfilled.csv",
    '2022': "/Users/km0/gitrepos/andy-borch-work/Data/CleanedBackfilled/cleaned-2022-backfilled.csv",
    '2023': "/Users/km0/gitrepos/andy-borch-work/Data/CleanedBackfilled/cleaned-2023-backfilled.csv",
    '2024': "/Users/km0/gitrepos/andy-borch-work/Data/CleanedBackfilled/cleaned-2024-backfilled.csv"
}

# Loop through the year_files to load each CSV into a DataFrame
# and store it in the dictionary.
for year, file_path in cleaned_year_files.items():
    df = pd.read_csv(file_path, on_bad_lines='skip', header=None)
    df['Year'] = year
    cleaned_backfilled_data_by_year[year] = df

clean_scatter, clean_heat = create_scatter(cleaned_backfilled_data_by_year)

years_list = list(cleaned_backfilled_data_by_year.keys())
for i, plot in enumerate(clean_scatter):
    if i < len(years_list):
        year = years_list[i]
        if plot is not None:
            plot.write_html(f"Cleaned_ElapsedvsNode_{year}.html")
        else:
            print(f"Skipping saving individual plot for {year} because no plot object was generated.")
    else:
        print(f"Warning: Mismatch between plots generated and expected years at index {i}.")

