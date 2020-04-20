import requests
import os
from datetime import datetime, timedelta
import pandas as pd


def update_csv(file, df):
    global today
    if(os.path.exists(file)):
        original_countries = pd.read_csv('confirmed.csv')
        current_df = pd.read_csv(file)
        current_df[today] = pd.DataFrame(columns=[today])
        today_data = []
        yesterday = str(
            (datetime.strptime(
                today,
                "%d-%m-%y") -
                timedelta(
                days=1)).strftime("%d-%m-%y"))
        for country in original_countries.iloc[:, 0]:
            if (country in list(df.loc[:, 'Country'])):
                today_data.append(int(df[df['Country'] == country][today]))
            else:
                today_data.append(
                    current_df.loc[current_df['Country'] == country][yesterday].item())
        current_df[today] = pd.Series(today_data)
        current_df.to_csv(file, index=False)
    else:
        countries = requests.get("https://api.covid19api.com/countries").json()
        countries = sorted([i['Country'] for i in countries])
        country_df = pd.DataFrame(data=countries, columns=['Country'])
        country_df[today] = df[today]
        country_df.to_csv(file, index=False)


data = requests.get("https://api.covid19api.com/summary").json()
today = str(datetime.strptime(
    data['Countries'][0]['Date'][:10], "%Y-%m-%d").strftime("%d-%m-%y"))

global_data = data["Global"]
print(f"\nGlobal status as of {today}")
print(f"Total cases: {global_data['TotalConfirmed']}")
print(f"New cases since yesterday: {global_data['NewConfirmed']}")
print(f"Total Deaths: {global_data['TotalDeaths']}")
print(f"New Deaths since yesterday: {global_data['NewDeaths']}")
print(f"Total Recovered: {global_data['TotalRecovered']}")
print(f"New Recovered since yesterday: {global_data['NewRecovered']}")

country_df_confirmed = pd.DataFrame(columns=['Country', today])
country_df_deaths = pd.DataFrame(columns=['Country', today])
country_df_recovered = pd.DataFrame(columns=['Country', today])

for country in data["Countries"]:
    country_df_confirmed = country_df_confirmed.append(
        {'Country': country['Country'], today: country['TotalConfirmed']}, ignore_index=True)
    country_df_deaths = country_df_deaths.append(
        {'Country': country['Country'], today: country['TotalDeaths']}, ignore_index=True)
    country_df_recovered = country_df_recovered.append(
        {'Country': country['Country'], today: country['TotalRecovered']}, ignore_index=True)

update_csv('confirmed.csv', country_df_confirmed)
update_csv('deaths.csv', country_df_deaths)
update_csv('recovered.csv', country_df_recovered)

confirmed_df = pd.read_csv('confirmed.csv')
confirmed_df = confirmed_df.sort_values(by=today, ascending=False)
countries = [confirmed_df.iloc[i]['Country'] for i in range(5)]
recovered_df = pd.read_csv('recovered.csv')
deaths_df = pd.read_csv('deaths.csv')

print("\nTop 5 countries with maximum cases:\n")
for country in countries:
    confirmed = confirmed_df.loc[confirmed_df['Country']
                                 == country][today].item()
    deaths = deaths_df.loc[deaths_df['Country']
                           == country][today].item()
    recovered = recovered_df.loc[recovered_df['Country']
                                 == country][today].item()
    print(f"{country} - {confirmed} cases | {deaths} deaths | {recovered} recovered")
