import pandas as pd
import os
import matplotlib.pyplot as plt

folder = "/Users/nandika/Desktop/IDX EXCHANGE /output "

listings = pd.read_csv(os.path.join(folder, "CombinedListings.csv"), low_memory=False)

print("\nRows and Coloumns:", listings.shape)
print("\nData Types:", listings.dtypes)
print("\nResidential Types included:", listings["PropertyType"].unique())
print("\nRow heads", listings.head())
print("\nColoumn names", listings.columns)

missing = listings.isnull().sum()
missing_percent = round(missing / len(listings) * 100)

missing_table = pd.DataFrame({
    "Missing Count": missing,
    "Missing Percent": missing_percent
})

print("\nMissing value summary:", missing_table)

more_missing = missing_table[missing_table["Missing Percent"] > 90]
print("\n90% + missing values:", more_missing)

numeric_columns = [
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt"
]

summary = listings[numeric_columns].describe(
    percentiles=[0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]
)

print("\nNumeric value summary", round(summary, 1))

market_fields = [
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt",
    "PropertyType",
    "CountyOrParish",
    "ListingContractDate"
]

metadata_fields = [
    col for col in listings.columns
    if col not in market_fields
]

print("\nMarket Analysis Fields", market_fields)
print("\nMetadata Fields", metadata_fields)

for col in numeric_columns:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    listings[col].hist(bins=30, ax=ax1)
    ax1.set_title(f"Histogram of {col}")
    ax1.set_xlabel(col)
    ax1.set_ylabel("Frequency")

    listings.boxplot(column=col, ax=ax2)
    ax2.set_title(f"Boxplot of {col}")

    plt.tight_layout()
    plt.show()

outlier_summary = {}

for col in numeric_columns:
    p1 = listings[col].quantile(0.01)
    p99 = listings[col].quantile(0.99)

    outliers = listings[
        (listings[col] < p1) |
        (listings[col] > p99)
    ]

    outlier_summary[col] = len(outliers)

print("\nOutlier Summary")

for col, count in outlier_summary.items():
    print(f"{col}: {count} outliers")

drop_columns = more_missing.index.tolist()

more_drop = [
    "ListingKey",
    "ListingKeyNumeric",
    "ListingId",
    "ListAgentEmail",
    "ListAgentFirstName",
    "ListAgentLastName",
    "ListAgentFullName",
    "CoListAgentFirstName",
    "CoListAgentLastName",
    "BuyerAgentFirstName",
    "BuyerAgentLastName",
    "BuyerAgentMlsId",
    "CoBuyerAgentFirstName",
    
]

listings = listings.drop(columns=drop_columns + more_drop)

print("\nShape after dropping columns:", listings.shape)

output_file = "/Users/nandika/Desktop/IDX EXCHANGE /output /CombinedListings_Cleaned.csv"

listings.to_csv(output_file, index=False)

print("\nCleaned dataset saved successfully!")
print(output_file)