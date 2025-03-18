import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

nlcd_colors = {
    11: '#526079', 12: '#9CA1B6', 21: '#D99282', 22: '#EB8F6A', 23: '#ED0000',
    24: '#AA0000', 31: '#B3AFA4', 41: '#68AB63', 42: '#1C6330', 43: '#B5C98E',
    51: '#CCB879', 52: '#CCBA7C', 71: '#DFD355', 72: '#AA7028', 73: '#BAA065',
    74: '#D1BB80', 81: '#DDD83E', 82: '#AE7229', 90: '#87D19E', 95: '#71A4C1'
}

nlcd_labels = {
    11: "Open Water", 12: "Perennial Ice/Snow", 21: "Developed, Open Space", 22: "Developed, Low Intensity",
    23: "Developed, Medium Intensity", 24: "Developed, High Intensity", 31: "Barren Land", 41: "Deciduous Forest",
    42: "Evergreen Forest", 43: "Mixed Forest", 51: "Dwarf Scrub", 52: "Shrub/Scrub", 71: "Grassland/Herbaceous",
    72: "Sedge/Herbaceous", 73: "Lichens", 74: "Moss", 81: "Pasture/Hay", 82: "Cultivated Crops", 90: "Woody Wetlands",
    95: "Emergent Herbaceous Wetlands"
}

def _create_stats_legend(ax: plt.Axes, stats_dict: dict[str, float], color_dict: dict[str, str]) -> None:
    """
    Create a unified legend with key statistics for an elevation difference histogram.

    Parameters
    ----------
    ax : plt.Axes
        The matplotlib axes object to add the legend to.
    stats_dict : dict[str, float]
        Dictionary containing statistics (Mean, Med, Std, NMAD, Count) to display.
    color_dict : dict[str, str]
        Dictionary mapping statistic names (e.g., "Mean", "Med") to colors.
    """
    legend_elements = []
    for label in ["Mean", "Med"]:
        color = color_dict.get(label, "black")
        legend_elements.append(
            plt.Line2D([0], [0], color=color, label=f"{label}: {stats_dict[label]:.2f}")
        )
    for label in ["Std", "NMAD"]:
        legend_elements.append(
            plt.Line2D([0], [0], color="none", label=f"{label}: {stats_dict[label]:.2f}")
        )
    legend_elements.append(
        plt.Line2D([0], [0], color="none", label=f"Count: {int(stats_dict['Count'])}")
    )
    legend = ax.legend(
        handles=legend_elements,
        loc="upper right",
        bbox_to_anchor=(0.98, 0.98),
        fontsize=10,
        facecolor="lightgray",
        edgecolor="none",
    )
    legend.get_frame().set_alpha(0.5)

def hist_nlcd(gdf: pd.DataFrame, min_count: int = 30, color_dict: dict[str, str] | None = None) -> tuple[plt.Figure, np.ndarray]:
    """
    Plot histograms of elevation differences by NLCD land cover class.

    The GeoDataFrame must contain:
        - 'nlcd_value': numeric NLCD code
        - 'nlcd_label': text label for the NLCD code
        - 'elev_diff': elevation difference values to be histogrammed

    Histograms are only plotted for groups with at least `min_count` points.
    The plots are arranged in a grid with 3 rows.

    Parameters
    ----------
    gdf : pd.DataFrame or GeoDataFrame
        DataFrame containing the NLCD data and elevation differences.
    min_count : int, default=30
        Minimum number of data points required for a group to be included.
    color_dict : dict[str, str] or None, optional
        Dictionary mapping statistic names to colors for the legend. If None, defaults are used.

    Returns
    -------
    fig : plt.Figure
        The created matplotlib Figure.
    axes : np.ndarray
        Array of matplotlib Axes objects.
    """
    if color_dict is None:
        color_dict = {
            "Mean": "magenta",
            "Med": "deepskyblue",
            "Std": "black",
            "NMAD": "black",
            "Count": "black",
        }
    # Group by NLCD class using both nlcd_value and nlcd_label
    groups = gdf.groupby(["nlcd_value", "nlcd_label"])
    filtered_groups = [
        (nlcd_value, nlcd_label, group) 
        for (nlcd_value, nlcd_label), group in groups 
        if len(group) >= min_count
    ]
    
    num_groups = len(filtered_groups)
    if num_groups == 0:
        raise ValueError("No NLCD groups with at least min_count points.")
    
    # Use a fixed 3 rows; number of columns is computed accordingly.
    nrows = 3
    ncols = math.ceil(num_groups / nrows)
    
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 4 * nrows), 
                             constrained_layout=True, sharex=True, sharey=True)
    # Ensure axes is a 2D numpy array for easy indexing.
    axes = np.atleast_2d(axes)
    
    bins = np.arange(-30, 30.25, 0.25)
    
    for i, (nlcd_value, nlcd_label, group) in enumerate(filtered_groups):
        row = i // ncols
        col = i % ncols
        ax = axes[row, col]
        
        # Get the color for the group from nlcd_colors; default to a gray if not found.
        hist_color = nlcd_colors.get(nlcd_value, "#cccccc")
        
        # Drop NaN values in elevation difference
        elev_diff = group["elev_diff"].dropna()
        ax.hist(elev_diff, bins=bins, alpha=0.5, color=hist_color, log=True)
        ax.axvline(0, color="k", linestyle="dashed", linewidth=1)
        ax.set_title(nlcd_label, fontsize=12)
        ax.set_xlim(-20, 20)
        if col == 0:
            ax.set_ylabel("Log(Count)")
        else:
            ax.set_ylabel("")
        
        # Compute statistics for the group.
        stats_dict = {
            "Mean": np.mean(elev_diff),
            "Med": np.median(elev_diff),
            "Std": np.std(elev_diff),
            "NMAD": stats.median_abs_deviation(elev_diff, scale="normal"),
            "Count": len(elev_diff),
        }
        _create_stats_legend(ax, stats_dict, color_dict)
        
        ax.axvline(stats_dict["Med"], color="deepskyblue", lw=0.5)
        ax.axvline(stats_dict["Mean"], color="magenta", lw=0.5)
    
    # Remove any extra unused subplots
    total_subplots = nrows * ncols
    for j in range(num_groups, total_subplots):
        row = j // ncols
        col = j % ncols
        fig.delaxes(axes[row, col])
    
    fig.suptitle("Elevation Differences by Land Cover (NLCD)", fontsize=14)
    return fig, axes

def boxplot_nlcd(gdf: pd.DataFrame, min_count: int = 30, figsize: tuple = None) -> tuple[plt.Figure, plt.Axes]:
    """
    Create boxplots of elevation differences by NLCD land cover class with observation counts.
    
    Parameters
    ----------
    gdf : pd.DataFrame or GeoDataFrame
        DataFrame containing the NLCD data and elevation differences.
        Required columns:
        - 'nlcd_value': numeric NLCD code
        - 'nlcd_label': text label for the NLCD code
        - 'elev_diff': elevation difference values to be plotted
    min_count : int, default=30
        Minimum number of data points required for a group to be included.
    figsize : tuple, optional
        Figure size as (width, height). If None, size is calculated based on number of groups.
        
    Returns
    -------
    fig : plt.Figure
        The created matplotlib Figure.
    ax : plt.Axes
        The main matplotlib Axes object.
    """
    # Group by NLCD class using both nlcd_value and nlcd_label
    groups = gdf.groupby(["nlcd_value", "nlcd_label"])
    filtered_groups = [
        (nlcd_value, nlcd_label, group) 
        for (nlcd_value, nlcd_label), group in groups 
        if len(group) >= min_count
    ]
    
    num_groups = len(filtered_groups)
    if num_groups == 0:
        raise ValueError("No NLCD groups with at least min_count points.")
    
    # Calculate appropriate figure size based on number of groups if not provided
    if figsize is None:
        # Width increases with number of groups, but has a minimum
        width = max(10, num_groups * 0.6)
        figsize = (width, 8)
    
    fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
    
    # Prepare data for boxplot
    box_data = []
    group_labels = []
    counts = []  # For the secondary y-axis
    nlcd_colors_list = []  # To store colors for each group
    
    # First pass: collect data
    for nlcd_value, nlcd_label, group in filtered_groups:
        # Get clean elevation difference data (drop NaNs)
        elev_diff = group["elev_diff"].dropna()
        
        box_data.append(elev_diff)
        group_labels.append(nlcd_label)
        counts.append(len(elev_diff))
        nlcd_colors_list.append(nlcd_colors.get(nlcd_value, "#cccccc"))
    
    # Create the boxplot
    boxplots = ax.boxplot(
        box_data,
        orientation="vertical",
        patch_artist=True,
        showfliers=True,
        boxprops={"facecolor": "lightgray", "color": "black"},
        flierprops={"marker": "x", "color": "black", "markersize": 5, "alpha": 0.6},
        medianprops={"color": "black"},
        positions=np.arange(len(box_data)),
    )
    
    # Color each box according to the NLCD color
    for patch, color in zip(boxplots["boxes"], nlcd_colors_list):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Set x-axis labels
    ax.set_xticks(np.arange(len(group_labels)))
    ax.set_xticklabels(group_labels, rotation=45, ha="right")
    
    # Set y-axis label
    ax.set_ylabel("Elevation Difference (m)", fontsize=12)
    
    # Add reference lines
    ax.axhline(0, color="black", linestyle="dashed", linewidth=0.7)
    
    #global_median = np.nanmedian(np.concatenate([d for d in box_data]))
    global_median = np.nanmedian(gdf["elev_diff"])
    ax.axhline(
        global_median,
        color="magenta",
        linestyle="dashed",
        linewidth=0.7,
        label=f"Global Med: {global_median:.2f}m",
        alpha=0.8,
    )
    
    # Add legend for the global median
    ax.legend(loc="upper right")
    
    # Second axis for observation counts
    ax2 = ax.twinx()
    ax2.plot(np.arange(len(counts)), counts, "o", color="orange", alpha=0.6)
    
    # Dynamic y-ticks for observation counts
    magnitude = 10 ** np.floor(np.log10(max(counts)))
    min_count = np.floor(min(counts) / magnitude) * magnitude
    max_count = np.ceil(max(counts) / magnitude) * magnitude
    ticks = np.linspace(min_count, max_count, 11)
    ax2.set_yticks(ticks)
    
    # Style the secondary y-axis
    ax2.spines["right"].set_color("orange")
    ax2.tick_params(axis="y", colors="orange")
    ax2.set_ylabel("Count", color="orange", fontsize=12)
    
    # Set title
    fig.suptitle("Elevation Differences by Land Cover (NLCD)", fontsize=14)
    
    # Ensure the x-axis limits give some padding
    ax.set_xlim(-0.5, len(box_data) - 0.5)
    
    # Calculate reasonable y-axis limits for elevation differences
    # Using percentiles instead of min/max to avoid extreme outliers affecting the view
    all_diffs = np.concatenate(box_data)
    y_min = np.percentile(all_diffs, 1)
    y_max = np.percentile(all_diffs, 99)
    # Add some padding
    y_range = y_max - y_min
    ax.set_ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)
    
    return fig, ax