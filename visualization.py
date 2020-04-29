import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import date2num, DateFormatter

confirmed_df = pd.read_csv('confirmed.csv')
deaths_df = pd.read_csv('deaths.csv')
recovered_df = pd.read_csv('recovered.csv')


def autopct_data(data):
    def my_autopct(pct):
        total = sum(data)
        val = int(round(pct * total / 100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
    return my_autopct


def create_pie(df, pie_type):
    date = df.columns[-1]
    sorted_data = df.sort_values(by=[date], ascending=False)
    total = sorted_data.sum(axis=0)[date]
    data = [sorted_data.iloc[i, -1] for i in range(10)]
    others = sum([sorted_data.iloc[i, -1]
                  for i in range(10, len(sorted_data))])
    data.append(others)
    labels = [sorted_data.iloc[i, 0] for i in range(10)]
    labels.append('Others')
    colors = [
        'lightskyblue',
        'red',
        'purple',
        'green',
        'aqua',
        'pink',
        'violet',
        'brown',
        'grey',
        'teal',
        'yellow']

    _, ax = plt.subplots(figsize=(13, 6))
    ax.pie(
        data,
        autopct=autopct_data(data),
        startangle=90,
        colors=colors,
        pctdistance=1.2,
        labeldistance=1.1)
    plt.axis('equal')
    ax.legend(labels, loc='upper right')

    title = ''
    if(pie_type == 'c'):
        title = f"Confirmed cases of COVID-19 worldwide.\nTotal = {total} cases as of {date}"
    elif (pie_type == 'd'):
        title = f"Deaths due to COVID-19 worldwide.\nTotal = {total} deaths as of {date}"
    else:
        title = f"Number of patients recovered from COVID-19 worldwide.\nTotal = {total} recovered as of {date}"

    plt.title(title)
    plt.tight_layout()

    if(pie_type == 'c'):
        plt.savefig(f'plots/confirmed_{date}.png', bbox_inches='tight')
    elif (pie_type == 'd'):
        plt.savefig(f'plots/deaths_{date}.png', bbox_inches='tight')
    else:
        plt.savefig(f'plots/recovered_{date}.png', bbox_inches='tight')


def autolabel(ax, rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width()/2, height*0.8),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', size=7)


def create_total_bar(df1, df2, df3):
    dates = df1.columns[1:]

    x = date2num([datetime.strptime(date, "%d-%m-%y").date()
                  for date in dates])

    today = dates[-1]

    total1 = [df1.sum(axis=0)[date] for date in dates]
    total2 = [df2.sum(axis=0)[date] for date in dates]
    total3 = [df3.sum(axis=0)[date] for date in dates]
    totalActive = [total1[i] - total2[i] - total3[i]
                   for i in range(len(total1))]

    _, ax = plt.subplots(figsize=(8, 5))

    w = 0.3

    plt.xlabel('Date')
    plt.ylabel('Number of cases')
    plt.title('Summary by date')

    bar1 = ax.bar(x-w, totalActive, color='lightskyblue', width=w)
    bar2 = ax.bar(x, total2, color='red', width=w)
    bar3 = ax.bar(x+w, total3, color='lightgreen', width=w)

    plt.legend(labels=['Active', 'Deaths', 'Recovered'], loc='upper left')

    autolabel(ax, bar1)
    autolabel(ax, bar2)
    autolabel(ax, bar3)

    plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%m-%y'))
    plt.xticks([(datetime.strptime(date, "%d-%m-%y")) for date in dates])
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.savefig(f'plots/total_{today}.png', bbox_inches='tight')


def create_new_bar(df1, df2, df3):
    dates = df1.columns[1:]
    today = dates[-1]
    x = date2num([datetime.strptime(date, "%d-%m-%y").date()
                  for date in dates[1:]])

    total1 = [df1.sum(axis=0)[date] for date in dates]
    total2 = [df2.sum(axis=0)[date] for date in dates]
    total3 = [df3.sum(axis=0)[date] for date in dates]

    new1 = [total1[i] - total1[i - 1] for i in range(1, len(total1))]
    new2 = [total2[i] - total2[i - 1] for i in range(1, len(total2))]
    new3 = [total3[i] - total3[i - 1] for i in range(1, len(total3))]

    _, ax = plt.subplots(figsize=(8, 5))

    w = 0.3

    plt.xlabel('Date')
    plt.ylabel('Number of new cases')
    plt.title('Number of new cases by date')

    bar1 = ax.bar(x-w, new1, color='lightskyblue', width=w)
    bar2 = ax.bar(x, new2, color='red', width=w)
    bar3 = ax.bar(x+w, new3, color='lightgreen', width=w)

    plt.legend(labels=['Confirmed', 'Deaths', 'Recovered'], loc='upper right')

    autolabel(ax, bar1)
    autolabel(ax, bar2)
    autolabel(ax, bar3)

    plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%m-%y'))
    plt.xticks([(datetime.strptime(date, "%d-%m-%y")) for date in dates[1:]])
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.savefig(f'plots/new_{today}.png', bbox_inches='tight')


create_pie(confirmed_df, 'c')
create_pie(deaths_df, 'd')
create_pie(recovered_df, 'r')

create_total_bar(confirmed_df, deaths_df, recovered_df)
create_new_bar(confirmed_df, deaths_df, recovered_df)
