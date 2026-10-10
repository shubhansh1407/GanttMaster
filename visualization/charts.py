import matplotlib.pyplot as plt
import pandas as pd
from typing import List
from core.models import GanttSegment

def plot_gantt_chart(segments: List[GanttSegment], max_time: int = None):
    fig, ax = plt.subplots(figsize=(10, 2.5))
    
    # Colors mapping
    unique_pids = list(set(s.pid for s in segments if s.pid != "IDLE"))
    # Use a clean colormap
    colors = plt.get_cmap('Set2', max(8, len(unique_pids)))
    color_map = {pid: colors(i) for i, pid in enumerate(unique_pids)}
    color_map["IDLE"] = "#e0e0e0" # Light Gray for idle
    
    ax.set_ylim(0, 1)
    if max_time is not None:
        ax.set_xlim(0, max_time)
    
    ticks = []
    
    for s in segments:
        duration = s.end_time - s.start_time
        facecolor = color_map[s.pid]
        edgecolor = '#444444' if s.pid != "IDLE" else '#999999'
        
        ax.broken_barh([(s.start_time, duration)], (0, 1), facecolors=facecolor, edgecolor=edgecolor, linewidth=1)
        
        # Add text in the middle
        if duration >= 1: # Only plot text if segment is large enough
            text_color = '#333333'
            ax.text(s.start_time + duration / 2, 0.5, s.pid, ha='center', va='center', color=text_color, fontweight='bold', fontsize=10)
        
        ticks.append(s.start_time)
        ticks.append(s.end_time)
        
    ticks = list(set(ticks))
    ticks.sort()
    
    ax.set_xticks(ticks)
    ax.set_yticks([])
    ax.set_xlabel('Time Units', fontsize=11, fontweight='medium')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    # Clean up spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.tight_layout()
    return fig

def plot_comparison_bar_chart(df: pd.DataFrame, metric_col: str, title: str, ylabel: str):
    fig, ax = plt.subplots(figsize=(7, 4))
    
    # Professional dark blue-gray color
    bar_color = '#3b5998'
    bars = ax.bar(df['Algorithm'], df[metric_col], color=bar_color, edgecolor='none', width=0.6, alpha=0.85)
    
    ax.set_title(title, pad=15, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)
                    
    # Clean up spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#dddddd')
    ax.spines['bottom'].set_color('#dddddd')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig
