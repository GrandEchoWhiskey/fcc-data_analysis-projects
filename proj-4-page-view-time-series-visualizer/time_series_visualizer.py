import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
lower_bound = df["value"].quantile(0.025)
upper_bound = df["value"].quantile(0.975)
df = df[(df["value"] >= lower_bound) & (df["value"] <= upper_bound)]

def draw_line_plot():
    # Draw line plot

    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(df.index, df['value'], color='red', linewidth=2)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", fontsize=14)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Page Views", fontsize=12)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['month'] = df_bar.index.strftime('%B')
    df_bar['year'] = df_bar.index.year

    df_bar = df_bar.groupby(['year','month'])['value'].sum().reset_index()
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=months_order, ordered=True)
    df_bar = df_bar.sort_values(['year', 'month'])

    # Draw bar plot

    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar.pivot(index='year', columns='month', values='value').plot(kind='bar', ax=ax)
    
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title="Month")
    plt.xticks(rotation=90)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Draw box plot (Year-wise)
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    axes[0].set_yticks(range(0, 220000, 20000))
    axes[0].set_yticklabels([str(i) for i in range(0, 220000, 20000)])

    # Draw box plot (Month-wise)
    sns.boxplot(x="month", y="value", data=df_box, order=months_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    axes[1].set_yticks(range(0, 220000, 20000))
    axes[1].set_yticklabels([str(i) for i in range(0, 220000, 20000)])

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
