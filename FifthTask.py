import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def draw_plot():
    # 1) Import data
    df = pd.read_csv("epa-sea-level.csv")

    # 2) Create scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df["Year"], df["CSIRO Adjusted Sea Level"], alpha=0.6)

    # 3) Line of best fit for all data
    slope_all, intercept_all, r_value, p_value, std_err = linregress(
        df["Year"], df["CSIRO Adjusted Sea Level"]
    )

    years_extended = pd.Series(range(1880, 2051))
    sea_level_all = intercept_all + slope_all * years_extended
    ax.plot(years_extended, sea_level_all, "r", label="Best fit (1880-2050)")

    # 4) Line of best fit from year 2000 onwards
    df_recent = df[df["Year"] >= 2000]
    slope_recent, intercept_recent, *_ = linregress(
        df_recent["Year"], df_recent["CSIRO Adjusted Sea Level"]
    )

    years_recent = pd.Series(range(2000, 2051))
    sea_level_recent = intercept_recent + slope_recent * years_recent
    ax.plot(years_recent, sea_level_recent, "g", label="Best fit (2000-2050)")

    # 5) Labels and title
    ax.set_title("Rise in Sea Level")
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Level (inches)")
    ax.legend()

    # Save and return the plot
    plt.savefig("sea_level_plot.png")
    return plt.gca()
