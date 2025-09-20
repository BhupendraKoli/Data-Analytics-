import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Import data (Make sure 'fcc-forum-pageviews.csv' is in the same folder)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Create line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df["value"], color="red", linewidth=1)

    # Set labels and title
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.tight_layout()
    return fig


def draw_bar_plot():
    # Copy and prepare data for bar plot
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month_name()

    # Group data
    df_grouped = df_bar.groupby(["year", "month"])["value"].mean().reset_index()

    # Ensure month order
    months_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df_grouped["month"] = pd.Categorical(df_grouped["month"], categories=months_order, ordered=True)

    # Pivot for bar plot
    df_pivot = df_grouped.pivot(index="year", columns="month", values="value")

    # Plot
    fig = df_pivot.plot(kind="bar", figsize=(10, 7)).get_figure()
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")
    fig.tight_layout()

    return fig


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy().reset_index()
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")
    df_box["month_num"] = df_box["date"].dt.month

    # Sort by month number to ensure correct order
    df_box = df_box.sort_values("month_num")

    # Draw plots (2 side by side)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise box plot
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(x="month", y="value", data=df_box, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.tight_layout()
    return fig
