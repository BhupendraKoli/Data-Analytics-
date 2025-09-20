import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def draw_cat_plot():
    # 1) Import data
    df = pd.read_csv('medical_examination.csv')

    # 2) Add 'overweight' column
    # BMI = weight(kg) / (height(m))^2 ; height is in cm in dataset
    bmi = df['weight'] / ((df['height'] / 100) ** 2)
    df['overweight'] = (bmi > 25).astype(int)

    # 3) Normalize data: 0 = good, 1 = bad
    # cholesterol and gluc: 1 -> 0, >1 -> 1
    df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
    df['gluc'] = (df['gluc'] > 1).astype(int)

    # 4) Create DataFrame for cat plot using pd.melt
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    # 5) Group and reformat the data to show counts of each feature split by cardio
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # 6) Draw the catplot with seaborn
    catplot = sns.catplot(
        data=df_cat,
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        kind='bar'
    )

    # 7) Get the figure for output
    fig = catplot.fig
    return fig


def draw_heat_map():
    # 1) Import data
    df = pd.read_csv('medical_examination.csv')

    # Add overweight (same as in cat plot)
    bmi = df['weight'] / ((df['height'] / 100) ** 2)
    df['overweight'] = (bmi > 25).astype(int)

    # Normalize cholesterol and gluc
    df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
    df['gluc'] = (df['gluc'] > 1).astype(int)

    # 2) Clean the data
    # Keep rows where ap_lo <= ap_hi
    df_heat = df[df['ap_lo'] <= df['ap_hi']].copy()

    # Height between 2.5th and 97.5th percentiles
    h_low = df_heat['height'].quantile(0.025)
    h_high = df_heat['height'].quantile(0.975)
    df_heat = df_heat[(df_heat['height'] >= h_low) & (df_heat['height'] <= h_high)]

    # Weight between 2.5th and 97.5th percentiles
    w_low = df_heat['weight'].quantile(0.025)
    w_high = df_heat['weight'].quantile(0.975)
    df_heat = df_heat[(df_heat['weight'] >= w_low) & (df_heat['weight'] <= w_high)]

    # 3) Calculate the correlation matrix
    corr = df_heat.corr()

    # 4) Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 5) Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 10))

    # 6) Draw the heatmap with seaborn
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.1f',
        center=0,
        vmax=0.3,
        vmin=-0.1,
        square=True,
        linewidths=.5,
        cbar_kws={"shrink": 0.5},
        ax=ax
    )

    return fig


fig1 = draw_cat_plot()
fig1.savefig('catplot.png')  # optional: save the figure

fig2 = draw_heat_map()
fig2.savefig('heatmap.png')  # optional: save the figure
