# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:33:28 2023

@author: Diego Lovato
"""
import seaborn as sns
import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt


def Tornado_plot(SA_results, baseline):
    # Where SA_results is pd.DataFrame with {index.names: ['Variable', 'Extent', 'Year'], columns: ['Impact name (metric)'], values: values}
    # Where baseline is pd.Series with {index: Year}

    # sns.set_style("ticks", rc={'axes.edgecolor': 'gray',
    #                            'font.family': 'serif',
    #                            'font.serif': 'Times New Roman',
    #                            'font_scale': 1})
    tornado_plot_colors = {
        'Min': '#4292C6',
        'Max': '#D7191C'}

    display_values = {
        'Vent Volume (e3m3/month)': {'Min': 3.62 , 'Max': 27.87},
        'Grid Intensity': {'Min': 110, 'Max': 910},
        'Discount Rate': {'Min': 110, 'Max': 910},
        'Methane Concentration (mol%)': {'Min': 60, 'Max': 100},
        'GWP': {'Min': 25, 'Max': 84},
        'Equipment Capture Efficiency (%)': {'Min': 95, 'Max': 100},
        'CAPEX (% change)': {'Min': "-20%", 'Max': "+20%"},
        'OPEX (% change)': {'Min': "-20%", 'Max': "+20%"},
    }

    decimal_places = 2
    impact_category = SA_results.columns[0]  # Referring to the name of the impact in the DataFrame (column name)

    limits = ['Min', 'Max']
    variables = list(SA_results.index.unique('Variable'))

    # Calculating the difference between the baseline and local input change
    year = 2022
    baseline = 16.29
    compiled_data = pd.DataFrame()
    for max_min in limits:
        for variable in variables:
            uncertain = SA_results.loc[(variable, max_min, slice(None)), impact_category]
            variance = (uncertain - baseline).to_frame()
            variance.columns = ['$/tCO2e']
            compiled_data = pd.concat([compiled_data, variance.reset_index()], ignore_index=True)
    compiled_data = compiled_data.set_index(['Year', 'Extent', 'Variable'])
    # compiled_data[compiled_data['CAD'].between(-10**-10, 10**-10, inclusive = 'neither')] = 0    

    # Determining if the local change increases, decreases, or has no impact on the metric.
    bound_lower = pd.DataFrame(dtype='float')
    bound_upper = pd.DataFrame(dtype='float')
    bound_no_impact = pd.DataFrame(dtype='float')
    for variable in variables:
        for limit in limits:
            loop_array = copy.deepcopy(compiled_data.loc[(slice(None), limit, variable), impact_category])
            loop_sum = loop_array.sum()

            if loop_sum < 0 and abs(loop_sum) > 0.001:
                bound_lower = pd.concat([bound_lower, loop_array.reset_index()])
                pass

            elif loop_sum > 0 and abs(loop_sum) > 0.001:
                bound_upper = pd.concat([bound_upper, loop_array.reset_index()])
                pass

            elif abs(loop_sum) < 0.001:
                bound_no_impact = pd.concat([bound_no_impact, loop_array.reset_index()])
                pass
    # bound_no_impact.iloc[:,-1] = 0
    compiled_data.sort_index(inplace=True)
    compiled_data_cum_variance = compiled_data.loc[(2022, slice(None), slice(None)), :].groupby(
        ['Extent', 'Variable']).sum()
    rank = abs(compiled_data_cum_variance).groupby('Variable').sum().sort_values(impact_category, ascending=True)
    variables = rank.index.to_list()

    # Compilind data to be plotted in tornado plot
    data_tornado_plot = pd.DataFrame(dtype='float')
    for extent in ['Min', 'Max']:
        for variable in variables:
            cummulative_impact = np.round(SA_results.loc[(variable, extent, slice(None)), impact_category].mean(),
                                          decimal_places)

            loop_df = pd.DataFrame(dtype='float')
            loop_df.loc[0, 'Extent'] = extent
            loop_df.loc[0, 'Variable'] = variable
            loop_df.loc[0, impact_category] = cummulative_impact
            data_tornado_plot = pd.concat([data_tornado_plot, loop_df])
    data_tornado_plot = data_tornado_plot.reset_index(drop=True)

    base = np.round(baseline, decimal_places)
    plot_lows = data_tornado_plot[data_tornado_plot[impact_category] < base]
    plot_highs = data_tornado_plot[data_tornado_plot[impact_category] > base]
    plot_no_impact = data_tornado_plot[data_tornado_plot[impact_category] == base]

    # If the change in input has no impact, it must be plotted opposite to its change in the opposite direction
    for ix, row in plot_no_impact.iterrows():

        var = plot_no_impact.loc[ix].loc['Variable']
        variable_in_lows = plot_lows['Variable'].isin([var]).any()
        variable_in_highs = plot_highs['Variable'].isin([var]).any()

        if variable_in_lows == False and variable_in_highs == False:
            plot_lows = pd.concat([plot_lows, plot_no_impact.loc[ix:ix]])

        elif variable_in_lows == True and variable_in_highs == False:
            plot_highs = pd.concat([plot_highs, plot_no_impact.loc[ix:ix]])

        elif variable_in_lows == False and variable_in_highs == True:
            plot_lows = pd.concat([plot_lows, plot_no_impact.loc[ix:ix]])

    # Arranging the color of the horizontal bars
    colors_lows = plot_lows.set_index('Variable').loc[variables, 'Extent'].map(tornado_plot_colors).to_numpy()
    colors_highs = plot_highs.set_index('Variable').loc[variables, 'Extent'].map(tornado_plot_colors).to_numpy()
    clr = [list(x) for x in (zip(colors_lows, colors_highs))]
    lows = plot_lows.set_index('Variable').loc[variables, impact_category].to_numpy()
    highs = plot_highs.set_index('Variable').loc[variables, impact_category].to_numpy()

    # Calling average inputs to display in chart
    lows_inputs_average = plot_lows.set_index('Variable').loc[variables, 'Extent'].reset_index().to_numpy()
    lows_inputs_average_sorted = []
    for i in lows_inputs_average:
        lows_inputs_average_sorted.append(display_values[i[0]][i[1]])

    highs_inputs_average = plot_highs.set_index('Variable').loc[variables, 'Extent'].reset_index().to_numpy()
    highs_inputs_average_sorted = []
    for i in highs_inputs_average:
        highs_inputs_average_sorted.append(display_values[i[0]][i[1]])

    # The actual drawing part
    fig, ax = plt.subplots(ncols=2, dpi=400, gridspec_kw={'width_ratios': [0.0, 1]})

    # The y position for each variable
    ax[1].text(base, -1.5, f'{np.round(base, 1)}', va='center', ha='center')
    # Plot the bars, one by one
    ys = range(len(variables))
    for y, low, high, low_in, high_in in zip(ys, lows, highs, lows_inputs_average_sorted, highs_inputs_average_sorted):
        low = np.round(low, decimal_places)
        high = np.round(high, decimal_places)
        # The width of the 'low' and 'high' pieces
        low_width = base - low
        high_width = high - base

        # Each bar is a "broken" horizontal bar chart
        ax[1].broken_barh(
            [(low, low_width), (base, high_width)],
            (y - 0.4, 0.8),
            facecolors=clr[y]
        )
        # Display the value as text.
        # if round(high_width) != 0:
        x = high_width
        x = base + high_width
        ax[1].text(x, y, f' {high_in}', va='center', ha='left')
        # if round(low_width) != 0:
        x = low_width
        x = base - low_width
        ax[1].text(x, y, f'{low_in} ', va='center', ha='right')

        # Draw a vertical line down the middle
        ax[1].axvline(base, color='black')

        # Position the x-axis on the top, hide all the other spines (=axis lines)
        ax[1].xaxis.set_ticks_position('top')
        ax[1].set_yticks(ticks=list(range(len(variables))))
        ax[1].set_yticklabels(variables)
        ax[1].yaxis.tick_right()

        ax[1].set_title('Axis units')
        ax[1].grid(True)
        # ax[1].set_xlim(800, 3500)

    # Legend setup
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], color='#4292C6', lw=15, label='Min input'),
                       Line2D([0], [0], color='#D7191C', lw=15, label='Max input')]
    ax[1].legend(handles=legend_elements, loc='center', bbox_to_anchor=(0.46, -.25))

    fig.savefig('sensitivityfigure.png')

if __name__ == '__main__':
    SA_cost_results_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\Equipment Inventory\SA_cost_results.csv"
    SA_cost_results = pd.read_csv(SA_cost_results_path)
    SA_cost_results = SA_cost_results.set_index(['Variable', 'Extent', 'Year'])

    baseline_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\Equipment Inventory\baseline.csv"
    baseline = pd.read_csv(baseline_path)
    baseline = baseline.set_index('Year')

    Tornado_plot(SA_cost_results, baseline)