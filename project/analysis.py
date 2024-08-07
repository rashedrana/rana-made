import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import pipeline

dataP = pipeline.main()
conn = sqlite3.connect(dataP[0])

data_query = f'''
SELECT	T1.Country_C [Country],
		T1.ISO3 [ISO3],
		T1.F2015_C,
		T1.F2015_F,
		T1.F2016_C,
		T1.F2017_C,
		T1.F2017_F,
		T1.F2018_C,
		T1.F2018_F,
		T1.F2019_C,
		T1.F2019_F,
		T1.F2020_C,
		T1.F2020_F,
		T1.F2021_C,
		T1.F2021_F
FROM	(
			SELECT 	DISTINCT * 
			FROM 	{dataP[1]}
			WHERE 	CTS_Code_F = 'ECGFTT' 
					AND CTS_Code_C = 'ECBTT' 
					AND Unit_F = 'Percent of GDP' 
					AND CTS_Name_C = 'CO2 Emissions Embodied in Trade; Trade Balance'
		) T1
WHERE	T1.ISO3 IN ("TUR", "LTU", "ARG", "IND", "JPN");
'''

data = pd.read_sql(data_query, conn)

conn.close()

countries = ["TUR", "LTU", "ARG", "IND", "JPN"]

filtered_data = data[data['ISO3'].isin(countries)]

years = ['F2015_C', 'F2016_C', 'F2017_C', 'F2018_C', 'F2019_C', 'F2020_C', 'F2021_C']

plt.figure(figsize=(12, 8))

for country in countries:
    country_data = filtered_data[filtered_data['ISO3'] == country]
    emissions = country_data[years].mean()  # Assuming multiple rows per country, take the mean
    plt.plot(years, emissions, marker='o', linestyle='-', label=country)

plt.title('CO2 Emissions from Fossil Fuel (2015-2021)')
plt.xlabel('Year')
plt.ylabel('CO2 Emissions (Millions of metric tons)')
plt.grid(True)
plt.legend(title='Country')
plt.show()

countries = ["TUR", "LTU", "ARG", "IND", "JPN"]
filtered_data = data[data['ISO3'].isin(countries)]

years = ['F2015_C', 'F2016_C', 'F2017_C', 'F2018_C', 'F2019_C', 'F2020_C', 'F2021_C']

long_data = pd.melt(filtered_data, id_vars=['Country', 'ISO3'], value_vars=years, var_name='Year', value_name='TradeBalance')

# Trade Balance Analysis
print("Trade Balance Analysis:")
for country in countries:
    country_data = long_data[long_data['ISO3'] == country]
    plt.figure(figsize=(10, 6))
    plt.plot(country_data['Year'], country_data['TradeBalance'], marker='o', linestyle='-')
    plt.title(f'Trade Balance of CO2 Emissions Embodied for {country} (2015-2021)')
    plt.xlabel('Year')
    plt.ylabel('Trade Balance (Percent of GDP)')
    plt.grid(True)
    plt.show()

# Ranking Countries by Trade Balance
print("\nRanking Countries by Trade Balance:")
rankings = pd.DataFrame(index=years, columns=countries)
for year in years:
    rankings.loc[year] = filtered_data.set_index('ISO3')[year].rank(ascending=False)
print(rankings)
