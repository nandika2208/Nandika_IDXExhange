import pandas as pd
import os

folder="/Users/nandika/Desktop/IDX EXCHANGE /output /csv "
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"

mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
mortgage.groupby('year_month')['rate_30yr_fixed']
.mean()
.reset_index()
)

sold= pd.read_csv( os.path.join(folder, "CombinedSellings_Cleaned.csv"), 
                  low_memory=False)
listing= pd.read_csv(os.path.join(folder, "CombinedListings_Cleaned.csv"), 
                     low_memory=False)


sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')


listing['year_month'] = pd.to_datetime(
listing['ListingContractDate']).dt.to_period('M')

sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listing_with_rates = listing.merge(mortgage_monthly, on='year_month', how='left')

print("\nNull rate values in sold",sold_with_rates['rate_30yr_fixed'].isnull().sum())
print("\nNull rate values in listing",listing_with_rates['rate_30yr_fixed'].isnull().sum())

print( "\n Preview",
sold_with_rates[
['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']
].head()
)


sell_o="/Users/nandika/Desktop/IDX EXCHANGE /output /csv /Merged_Sellings.csv"
list_o="/Users/nandika/Desktop/IDX EXCHANGE /output /csv /Merged_Listings.csv"
sold.to_csv(sell_o, index=False )
listing.to_csv(list_o, index=False)
print("\nNew files saved successfully!")
print(sell_o, list_o)