import pandas as pd 
import os 

folder="/Users/nandika/Desktop/IDX EXCHANGE /output /csv "
sold= pd.read_csv(os.path.join(folder, "Merged_Sellings.csv"), low_memory= False)

print("\nRows before final cleaning", len(sold))

# CONVERT DATES 

date_fields = ["CloseDate", 
               "PurchaseContractDate",
               "ListingContractDate",
             "ContractStatusChangeDate"]

for col in date_fields:
    sold[col] = pd.to_datetime(sold[col], errors="coerce")

print("\nFormat of date fields:")
print(sold[date_fields].dtypes)

# CONVERT NUMERIC 

numeric_fields = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt"]


for col in numeric_fields:
    sold[col]= pd.to_numeric(sold[col], errors="coerce")
    
print("\nFormat of numeric fields:")   
print(sold[numeric_fields].dtypes)
 
# POSITVIE FIELDS   
    
positive_fields = [
    "ClosePrice",
    "LivingArea",
    "BedroomsTotal",
    "BathroomsTotalInteger"]

for col in positive_fields:
    sold = sold[sold[col] > 0]

sold = sold[sold["DaysOnMarket"] >= 0]

# CHRONOLOGICAL ORDERS 

sold["listing_after_close_flag"] = (
    sold["ListingContractDate"] >
    sold["CloseDate"])

sold["purchase_after_close_flag"]= (
    sold["PurchaseContractDate"]>
    sold["CloseDate"])

sold["negative_timeline_flag"] = (
    sold["PurchaseContractDate"] <
    sold["ListingContractDate"])

print("\nListing after close:",sold["listing_after_close_flag"].sum())

print("Purchase after close:",sold["purchase_after_close_flag"].sum())

print("Negative timeline:", sold["negative_timeline_flag"].sum())

# GEOGRAPHICAL FLAGGING  

sold["missing_coordinates_flag"] = (
    sold["Latitude"].isna() |
    sold["Longitude"].isna())

sold["zero_coordinates_flag"] = (
    (sold["Latitude"] == 0) |
    (sold["Longitude"] == 0))

sold["positive_longitude_flag"] = (
    sold["Longitude"] > 0)

sold["invalid_coordinate_flag"] = (
    (sold["Latitude"] < 32) |
    (sold["Latitude"] > 42) |
    (sold["Longitude"] < -124) |
    (sold["Longitude"] > -114))

print("\nMissing Coordinates:",
      sold["missing_coordinates_flag"].sum())

print("Zero Coordinates:",
      sold["zero_coordinates_flag"].sum())

print("Positive Longitude:",
      sold["positive_longitude_flag"].sum())

print("Invalid Coordinates:",
      sold["invalid_coordinate_flag"].sum())

# MISSING VALUES 

required_columns = [
    "ClosePrice",
    "LivingArea",
    "DaysOnMarket",
    "Latitude",
    "Longitude"]

sold = sold.dropna(subset=required_columns)


print("\nRows after final cleaning", len(sold))

output_file = "/Users/nandika/Desktop/IDX EXCHANGE /output /Week4_Cleaned.csv"
sold.to_csv(output_file, index=False)

print("\nCleaned dataset saved successfully!")
print(output_file)




