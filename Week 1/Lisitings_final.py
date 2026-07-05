import pandas as pd 
import glob 
import os 

folder= "/Users/nandika/Desktop/IDX EXCHANGE /Raw Data /Listing /"

listing_files = glob.glob(os.path.join(folder, "CRMLSListing*.csv"))

listing_data = []

r_before_concat = 0

for file in listing_files:
    df = pd.read_csv(file)
    r_before_concat += len(df)
    listing_data.append(df)
    
print( "Total Rows Before Concatination:", r_before_concat )

listings = pd.concat(listing_data, ignore_index=True)

print("Rows After Concatenation:", len(listings))

print("Rows Before Residential filter:", len(listings))

listings = listings[listings["PropertyType"] == "Residential"]

print("Rows After Residential Filter:", len(listings))

output_file = "/Users/nandika/Desktop/IDX EXCHANGE /CombinedListings.csv"
listings.to_csv(output_file, index=False)

print("Saved to:", output_file)
print("CombinedListings.csv Saved Successfully!")
