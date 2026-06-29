

import pandas as pd 
import glob 
import os 

folder= "/Users/nandika/Desktop/IDX EXCHANGE /Raw Data /sold /"

sold_files = glob.glob(os.path.join(folder, "CRMLSSold*.csv"))

sold_data = []

r_before_concat = 0

for file in sold_files:
    df = pd.read_csv(file)
    r_before_concat += len(df)
    sold_data.append(df)
    
print( "Total Rows Before Concatination:", r_before_concat )

sellings = pd.concat(sold_data, ignore_index=True)

print("Rows After Concatenation:", len(sellings))

print("Rows Before Residential filter:", len(sellings))

sellings = sellings[sellings["PropertyType"] == "Residential"]

print("Rows After Residential Filter:", len(sellings))

output_file = "/Users/nandika/Desktop/IDX EXCHANGE /CombinedSellings.csv"
sellings.to_csv(output_file, index=False)

print("Saved to:", output_file)
print("CombinedSellings.csv Saved Successfully!")
