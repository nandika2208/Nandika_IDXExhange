import pandas as pd
import os 
import matplotlib.pyplot as plt 

folder="/Users/nandika/Desktop/IDX EXCHANGE /"
sold =   pd.read_csv(os.path.join(folder, "CombinedSellings.csv"), low_memory=False)

print("\nRows and Coloumns:","", sold.shape)
print("\nData Types:", sold.dtypes)
print("\nResidential Types included:", sold["PropertyType"].unique())
print("\nRow heads", sold.head())
print("\nColoumn names", sold.columns)

missing=sold.isnull().sum()
missing_percent = round(missing/len(sold)*100,)
missing_table=pd.DataFrame({
"Missing Count":missing,
"Missing Percent":missing_percent
})

print("\nMissing value summary:", missing_table )

more_missing=missing_table[missing_table["Missing Percent"]>90]
print("\n90% + missing values:", more_missing)

numeric_columns = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt"
]

summary = sold[numeric_columns].describe(percentiles=[0.01,0.05,0.25,0.50,0.75,0.95,0.99])
print("\nNumeric value summary", round(summary,1))

market_fields = [
    "ClosePrice",
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
    "ListingContractDate",
    "CloseDate"
]

metadata_fields = [
    col for col in sold.columns
    if col not in market_fields
]

print("\nMarket Analysis Fields" , market_fields)
print("\nMetadata Fields", metadata_fields)


for col in numeric_columns:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    sold[col].hist(bins=30, ax=ax1)
    ax1.set_title(f"Histogram of {col}")
    ax1.set_xlabel(col)
    ax1.set_ylabel("Frequency")
    
    sold.boxplot(column=col, ax=ax2)
    ax2.set_title(f"Boxplot of {col}")

    plt.tight_layout()
    plt.show()
    
outlier_summary = {}
for col in numeric_columns:
    p1 = sold[col].quantile(0.01)
    p99 = sold[col].quantile(0.99)
    outliers = sold[
        (sold[col] < p1) |
        (sold[col] > p99)
    ]
    outlier_summary[col] = len(outliers)

print("\nOutlier Summary")

for col, count in outlier_summary.items():

    print(f"{col}: {count} outliers")
    

    