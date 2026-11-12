import pandas as pd
df = pd.read_csv('global air pollution dataset.csv')
india_df = df[df['Country'] == 'India']
from geo_data import CITY_COORDS

# Let's inspect some other cities in India
unmatched_polluted = india_df[~india_df['City'].isin(CITY_COORDS.keys())].sort_values(by='AQI Value', ascending=False).head(30)
print("Unmatched Top Polluted:")
print(unmatched_polluted[['City', 'AQI Value']].to_string())

unmatched_clean = india_df[~india_df['City'].isin(CITY_COORDS.keys())].sort_values(by='AQI Value', ascending=True).head(30)
print("\nUnmatched Clean:")
print(unmatched_clean[['City', 'AQI Value']].to_string())
