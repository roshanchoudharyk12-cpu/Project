import pandas as pd
import numpy as np

df = pd.read_csv('global air pollution dataset.csv')
print("Total rows:", len(df))
print("Columns:", df.columns.tolist())
print("\nUnique countries count:", df['Country'].nunique())
print("Top 10 countries by number of cities in dataset:")
print(df['Country'].value_counts().head(10))

india_df = df[df['Country'] == 'India']
print("\n--- INDIA DATASET STATS ---")
print("Total Indian cities:", len(india_df))
print("AQI Value summary for India:")
print(india_df['AQI Value'].describe())

print("\nIndia AQI Categories distribution:")
print(india_df['AQI Category'].value_counts(normalize=True)*100)
print(india_df['AQI Category'].value_counts())

print("\nGlobal AQI Categories distribution:")
print(df['AQI Category'].value_counts(normalize=True)*100)

print("\nGlobal Top 15 Countries by Mean AQI (min 20 cities):")
country_stats = df.groupby('Country')['AQI Value'].agg(['count', 'mean', 'median', 'max'])
country_stats_filtered = country_stats[country_stats['count'] >= 20].sort_values(by='mean', ascending=False)
print(country_stats_filtered.head(15))

print("\nWhere does India rank globally in mean AQI (among countries with >= 20 cities)?")
rank = country_stats_filtered.index.get_loc('India') + 1 if 'India' in country_stats_filtered.index else "N/A"
print(f"India Rank: {rank} out of {len(country_stats_filtered)}")
print(country_stats_filtered.loc['India'] if 'India' in country_stats_filtered.index else "")

print("\nTop 15 Most Polluted Indian Cities:")
top_polluted_india = india_df.sort_values(by='AQI Value', ascending=False)[['City', 'AQI Value', 'AQI Category', 'PM2.5 AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'CO AQI Value']].head(15)
print(top_polluted_india.to_string())

print("\nTop 10 Cleanest Indian Cities:")
cleanest_india = india_df.sort_values(by='AQI Value', ascending=True)[['City', 'AQI Value', 'AQI Category', 'PM2.5 AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'CO AQI Value']].head(10)
print(cleanest_india.to_string())

print("\nCorrelation matrix for India pollutants:")
pollutant_cols = ['AQI Value', 'CO AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'PM2.5 AQI Value']
print(india_df[pollutant_cols].corr())

print("\nDominant Pollutant Analysis for India:")
# In how many cities is PM2.5 AQI == AQI Value?
pm25_dominant = (india_df['AQI Value'] == india_df['PM2.5 AQI Value']).sum()
ozone_dominant = (india_df['AQI Value'] == india_df['Ozone AQI Value']).sum()
no2_dominant = (india_df['AQI Value'] == india_df['NO2 AQI Value']).sum()
co_dominant = (india_df['AQI Value'] == india_df['CO AQI Value']).sum()
print(f"PM2.5 is dominant in: {pm25_dominant} / {len(india_df)} ({pm25_dominant/len(india_df)*100:.2f}%)")
print(f"Ozone is dominant in: {ozone_dominant} / {len(india_df)} ({ozone_dominant/len(india_df)*100:.2f}%)")
print(f"NO2 is dominant in: {no2_dominant} / {len(india_df)} ({no2_dominant/len(india_df)*100:.2f}%)")
print(f"CO is dominant in: {co_dominant} / {len(india_df)} ({co_dominant/len(india_df)*100:.2f}%)")

print("\nCheck missing values in dataset:")
print(df.isnull().sum())
