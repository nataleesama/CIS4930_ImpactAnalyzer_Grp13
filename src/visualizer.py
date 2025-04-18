import matplotlib
#matplotlib.use('Agg')  # Ensures html translation

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import List, Tuple, Optional
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from IPython.display import HTML
from plotly.subplots import make_subplots
import plotly.io
import plotly.express
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import mpld3
#Working on: Implement a custom visualization technique for displaying multidimensional climate data, Create an animated visualization showing climate change over time
class Visualizer:
    @staticmethod
    def plot_precipitation_trend(years: List[int], precipitations: List[float], predictions: List[float]):
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        
        fig.add_trace(go.Scatter(x=[],y=[], name='Actual', line=dict(color='blue', width=3), mode='lines'))
    
        fig.add_trace(go.Scatter(x=[],y=[],name='Predicted',line=dict(color='red', width=3, dash='dash'),mode='lines'))
        
        frames = [go.Frame(data=[go.Scatter(x=years[:k+1], y=precipitations[:k+1]),go.Scatter(x=years[:k+1], y=predictions[:k+1])],name=str(year))for k, year in enumerate(years)]
        
        fig.frames = frames
        tick_vals = sorted(list(set([int(year) for year in years])))
        tick_labelAug = [f"8/{str(year)[-2:]}" for year in range(min(years),max(years))]
        fig.update_layout(
            title=f"Precipitation Trend vs Predicted Trend ({min(years)}-{max(years)})",
            xaxis=dict(
                title='Year',
                range=[min(years), max(years)],
                showgrid=True,
                tickmode='array',  # Use custom tick values
                tickvals=tick_vals,  # Only show whole years
                tickformat='d',
                ticktext = tick_labelAug
            ),
            yaxis=dict(
                title='Precipitation (normalized)',
                range=[min(precipitations+predictions)-0.1, max(precipitations+predictions)+0.1],
                showgrid=True
            ),
            hovermode='x unified',
            updatemenus=[{
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [
                            None, 
                            {
                            "frame": {"duration": 500, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 300}
                            }
                    ]
                },
                {
                    "label": "Pause",
                    "method": "animate",
                    "args": [
                        [None], 
                        {
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }
                    ]
                }
            ],
            "x": 0.1,
            "y": 0,
            "xanchor": "right",
            "yanchor": "top"
        }],
        sliders=[{
            "steps": [
                {
                    "args": [
                        [frame.name],
                        {"frame": {"duration": 0, "redraw": True},
                         "mode": "immediate"}
                    ],
                    "label": frame.name,
                    "method": "animate"
                }
                for frame in frames
            ],
            "x": 0.1,
            "len": 0.9,
            "currentvalue": {
                "prefix": "Year: ",
                "visible": True,
                "xanchor": "right"
            }
        }]
    )
    
    
        fig.update_layout(
            annotations=[
                dict(
                    x=0.95,
                    y=0.1,
                    xref="paper",
                    yref="paper",
                    text=f"Year: {years[0]}",
                    font=dict(size=20),
                    showarrow=False,
                    xanchor="right"
            )
        ]
        )
    
    
        for i, frame in enumerate(fig.frames):
            frame.layout.annotations = [
                dict(
                x=0.95,
                y=0.1,
                xref="paper",
                yref="paper",
                text=f"Year: {years[i]}",
                font=dict(size=20),
                showarrow=False,
                xanchor="right"
            )
        ]
    
        fig.show()
        #return only in order to display on html
        #return fig

    @staticmethod
    def plot_precipitation_trend_html(years: List[int], precipitations: List[float], predictions: List[float]):
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        
        fig.add_trace(go.Scatter(x=[years[0]],y=[precipitations[0]], name='Actual', line=dict(color='blue', width=3), mode='lines'))
    
        fig.add_trace(go.Scatter(x=[years[0]],y=[precipitations[0]],name='Predicted',line=dict(color='red', width=3, dash='dash'),mode='lines'))
        
        step = 5  # so much data, skip every 5 points
        frames = [
            go.Frame(
                data=[
                    go.Scatter(x=years[:k+1], y=precipitations[:k+1], mode='lines', line=dict(color='blue', width=3)),
                    go.Scatter(x=years[:k+1], y=predictions[:k+1], mode='lines', line=dict(color='red', width=3, dash='dash'))
                ],
                name=str(years[k])
            )
            for k in range(0, len(years), step)
        ]

        fig.frames = frames
        tick_vals = sorted(list(set([int(year) for year in years])))
        tick_labelAug = [f"8/{str(year)[-2:]}" for year in range(min(years),max(years))]
        fig.update_layout(
            title=f"Precipitation Trend vs Predicted Trend ({min(years)}-{max(years)})",
            xaxis=dict(
                title='Year',
                range=[min(years), max(years)],
                showgrid=True,
                tickmode='array',  # Use custom tick values
                tickvals=tick_vals,  # Only show whole years
                tickformat='d',
                ticktext = tick_labelAug
            ),
            yaxis=dict(
                title='Precipitation (normalized)',
                range=[min(precipitations+predictions)-0.1, max(precipitations+predictions)+0.1],
                showgrid=True
            ),
            hovermode='x unified',
            updatemenus=[{
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [
                            [None], 
                            {
                            "frame": {"duration": 0.01, "redraw": False},
                            "fromcurrent": True,
                            "transition": {"duration": 0}
                            }
                    ]
                },
                {
                    "label": "Pause",
                    "method": "animate",
                    "args": [
                        [None], 
                        {
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }
                    ]
                }
            ],
            "x": 0.1,
            "y": 0,
            "xanchor": "right",
            "yanchor": "top"
        }],
        sliders=[{
            "steps": [
                {
                    "args": [
                        [frame.name],
                        {"frame": {"duration": 0, "redraw": True},
                         "mode": "immediate"}
                    ],
                    "label": frame.name,
                    "method": "animate"
                }
                for frame in frames
            ],
            "x": 0.1,
            "len": 0.9,
            "currentvalue": {
                "prefix": "Year: ",
                "visible": True,
                "xanchor": "right"
            }
        }]
    )
    
    
        fig.update_layout(
            annotations=[
                dict(
                    x=0.95,
                    y=0.1,
                    xref="paper",
                    yref="paper",
                    text=f"Year: {years[0]}",
                    font=dict(size=20),
                    showarrow=False,
                    xanchor="right"
            )
        ]
        )
    
    
        for i, frame in enumerate(fig.frames):
            frame.layout.annotations = [
                dict(
                x=0.95,
                y=0.1,
                xref="paper",
                yref="paper",
                text=f"Year: {years[i]}",
                font=dict(size=20),
                showarrow=False,
                xanchor="right"
            )
        ]
    
        #return only in order to display on html
        return fig
    
    @staticmethod
    def plot_clustered_data(data: List[Tuple[float, float]], labels: List[int]) -> None:
        plt.figure(figsize=(10, 6)) #presetting the size for legibility
        
        dataArray = np.array(data)
        x = dataArray[:, 0]
        y = dataArray[:, 1]

        bounds = [2020,2025,0,100] #axis aka years, these would be the static markers for the xaxis
        plt.scatter(x, y)

        xTickYears = range(2020,2025)
        xTickLabels = [f"08/{year}" for year in xTickYears]

        plt.xticks(xTickYears,xTickLabels) #ticks need to be represented as integers, and aug 1 ~2020.58. fix later
        #plt.axis(bounds) #so this sets the max for both x and y
        plt.grid(True)
        plt.show()

        # Equivalent Code that allows html interactive abilities
        """
        x_value, y_value = zip(*data)

        fig = plotly.express.scatter(
            x=x_value,
            y=y_value,
            title="Clustered Data",
            labels={'x': 'Year', 'y': 'Precipitation'}
        )

        # Customize ticks
        fig.update_layout(
            xaxis=dict(
                tickvals=list(range(2020, 2025)),
                ticktext=[f"08/{year}" for year in range(2020, 2025)]
            ),
            xaxis_title='Date',
            yaxis_title='Precipitation',
            height=600
        )

        # to display in html
        return plotly.io.to_html(fig, full_html=False, include_plotlyjs='cdn')
        """

    # same approach as function below, but allows html display
    @staticmethod
    def plot_anomalies_to_html(station_data: dict) -> str:
        matplotlib.use('Agg')
        fig, ax = plt.subplots(figsize=(12, 6))

        # Calculate consistent thresholds
        for station in station_data:
            log_values = np.log1p(station_data[station]['values'])
            lower_bound = np.percentile(log_values, 5)
            upper_bound = np.percentile(log_values, 95)

            station_data[station]['anomalies'] = (log_values < lower_bound) | (log_values > upper_bound)
            station_data[station]['upper_whisker'] = upper_bound

        stations = list(station_data.keys())
        boxplot_data = [np.log1p(station_data[station]['values']) for station in stations]

        boxplot = ax.boxplot(boxplot_data,
                            positions=range(len(stations)),
                            patch_artist=True,
                            widths=0.6,
                            whis=[5, 95])

        colors = ['#1f77b4', '#2ca02c', '#d62728']
        for i, color in enumerate(colors):
            boxplot['boxes'][i].set_facecolor(color)
            boxplot['medians'][i].set_color('white')
            boxplot['whiskers'][2*i+1].set_color(color)
            boxplot['whiskers'][2*i+1].set_linestyle(':')
            ax.axhline(station_data[stations[i]]['upper_whisker'], 
                    color=color, linestyle=':', alpha=0.3)

        for i, (station, color) in enumerate(zip(stations, colors)):
            values = np.array(station_data[station]['values'])
            anomalies = np.array(station_data[station]['anomalies'], dtype=bool)
            log_values = np.log1p(values)

            normal = log_values[~anomalies]
            ax.scatter([i + 0.1]*len(normal), normal, color=color, alpha=0.5, s=30, edgecolors='white', linewidths=0.5)

            anomaly_vals = log_values[anomalies]
            ax.scatter([i - 0.1]*len(anomaly_vals), anomaly_vals, color='yellow', marker='X', s=150,
                    linewidths=2, edgecolors='black')

        def log_to_actual(y):
            return f"{np.expm1(y):.1f}" if y >= 0 else "0"

        y_ticks = [0, 1, 2, 3, 4]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([log_to_actual(y) for y in y_ticks])
        ax.set_ylabel('Precipitation (inches)', labelpad=20)
        ax.text(-0.08, 0.5, 'log(precip + 1)', rotation=90, va='center', ha='right', transform=ax.transAxes)

        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Normal', markerfacecolor='gray', markersize=10),
            Line2D([0], [0], marker='X', color='yellow', label='Anomaly', markeredgecolor='black', markersize=12),
            *[Patch(facecolor=color, label=station) for color, station in zip(colors, stations)]
        ]

        ax.legend(handles=legend_elements, loc='upper right', fontsize=12, framealpha=1)
        ax.set_xticks(range(len(stations)))
        ax.set_xticklabels(stations, fontsize=12)
        ax.set_title('Precipitation Anomalies (5th-95th Percentile Detection)', pad=25, fontsize=14)
        ax.grid(True, linestyle=':', alpha=0.3)

        plt.tight_layout()

        # Convert to interactive HTML with mpld3
        return mpld3.fig_to_html(fig)

    @staticmethod
    def plot_anomalies(station_data: dict):
        fig, ax = plt.subplots(figsize=(12, 6))

        # Calculate consistent thresholds for both boxplot and anomalies
        for station in station_data:
            log_values = np.log1p(station_data[station]['values'])

            # Calculate percentiles to match boxplot whis=[5,95]
            lower_bound = np.percentile(log_values, 5)
            upper_bound = np.percentile(log_values, 95)

            # Recalculate anomalies to match these bounds
            station_data[station]['anomalies'] = (log_values < lower_bound) | (log_values > upper_bound)
            station_data[station]['upper_whisker'] = upper_bound  # For reference line

        stations = list(station_data.keys())
        boxplot_data = [np.log1p(station_data[station]['values']) for station in stations]

        # Create boxplot with matching percentiles
        boxplot = ax.boxplot(boxplot_data,
                            positions=range(len(stations)),
                            patch_artist=True,
                            widths=0.6,
                            whis=[5, 95])  # Matches our anomaly bounds

        # Visual enhancements
        colors = ['#1f77b4', '#2ca02c', '#d62728']
        for i, color in enumerate(colors):
            boxplot['boxes'][i].set_facecolor(color)
            boxplot['medians'][i].set_color('white')
            boxplot['whiskers'][2*i+1].set_color(color)  # Upper whisker
            boxplot['whiskers'][2*i+1].set_linestyle(':')

            # Add threshold reference line
            ax.axhline(station_data[stations[i]]['upper_whisker'], 
                    color=color, linestyle=':', alpha=0.3)

        # Plot points with clear anomaly distinction
        for i, (station, color) in enumerate(zip(stations, colors)):
            values = np.array(station_data[station]['values'])
            anomalies = np.array(station_data[station]['anomalies'], dtype=bool)
            log_values = np.log1p(values)

            # Plot normal points (smaller, semi-transparent)
            normal = log_values[~anomalies]
            ax.scatter([i + 0.1]*len(normal), normal,
                    color=color, alpha=0.5, s=30, 
                    edgecolors='white', linewidths=0.5)

            # Plot anomalies (larger, bright)
            anomaly_vals = log_values[anomalies]
            ax.scatter([i - 0.1]*(len(anomaly_vals)), anomaly_vals,
                    color='yellow', marker='X', s=150,
                    linewidths=2, edgecolors='black')

        # Dual y-axis labels
        def log_to_actual(y):
            return f"{np.expm1(y):.1f}" if y >=0 else "0"

        y_ticks = [0, 1, 2, 3, 4]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([log_to_actual(y) for y in y_ticks])
        ax.set_ylabel('Precipitation (inches)', labelpad=20)
        ax.text(-0.08, 0.5, 'log(precip + 1)',
            rotation=90, va='center', ha='right',
            transform=ax.transAxes)

        # Enhanced legend
        legend_elements = [ Line2D([0], [0], marker='o', color='w', label='Normal', markerfacecolor='gray', markersize=10),
            Line2D([0], [0], marker='X', color='yellow', label='Anomaly',
                markeredgecolor='black', markersize=12),
            *[Patch(facecolor=color, label=station) 
            for color, station in zip(colors, stations)]]

        ax.legend(handles=legend_elements, loc='upper right',
                fontsize=12, framealpha=1)

        # Final formatting
        ax.set_xticks(range(len(stations)))
        ax.set_xticklabels(stations, fontsize=12)
        ax.set_title('Precipitation Anomalies (5th-95th Percentile Detection)', 
                    pad=25, fontsize=14)
        ax.grid(True, linestyle=':', alpha=0.3)

        plt.tight_layout()
        plt.show()
