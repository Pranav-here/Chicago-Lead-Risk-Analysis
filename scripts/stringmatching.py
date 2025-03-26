import pandas as pd

# Step 1: Read and clean the data from the Assessor data (df1)
dtypes = {
    'pin': 'float64',
    'property_address': 'str',
    'property_apt_no': 'str',
    'property_city': 'str',
    'property_zip': 'str',
    'mailing_address': 'str',
    'longitude': 'float64',
    'latitude': 'float64',
    'tract_pop': 'float64',
    'tract_midincome': 'float64',
    'tract_geoid': 'str',
    'tract_white_perc': 'float64',
    'tract_black_perc': 'float64',
    'tract_asian_perc': 'float64',
    'tract_his_perc': 'float64',
    'tract_other_perc': 'float64'
}

df1 = pd.read_csv(
    "data\Assessor__Archived_05-11-2022__-_Property_Locations_20250304.csv",
    usecols=['pin', 'property_address', 'property_apt_no', 'property_city', 'property_zip',
             'mailing_address', 'longitude', 'latitude', 'tract_pop', 'tract_midincome',
             'tract_geoid', 'tract_white_perc', 'tract_black_perc', 'tract_asian_perc',
             'tract_his_perc', 'tract_other_perc', 'nbhd'],
    dtype=dtypes,
    na_values=['NA', 'NaN', ''],  # Treat these values as NaN
)

# Step 2: Handle missing values in important columns
df1['tract_pop'] = df1['tract_pop'].fillna(0)
df1['tract_midincome'] = df1['tract_midincome'].fillna(0)

# Clean the 'property_address' by stripping spaces and converting to uppercase
df1['property_address'] = df1['property_address'].str.strip().str.upper()

# Step 3: Read and clean the address data (df2)
df2 = pd.read_csv("data\T096318_Responsive_Document.csv", usecols=['Address', 'Private Service Line Material', 'Public Service Line Material'], dtype={'Address': 'str'})

# Clean the 'Address' in df2 by stripping spaces and converting to uppercase
df2['Address'] = df2['Address'].str.strip().str.upper()

# Step 4: Merge the datasets on the cleaned address column
merged_df = pd.merge(df2, df1, left_on='Address', right_on='property_address', how='inner')

# Step 5: Select only the necessary columns for the final dataset
final_merged_df = merged_df[['pin', 'Address', 'Private Service Line Material', 'Public Service Line Material',
                              'property_apt_no', 'property_city', 'property_zip', 'mailing_address',
                              'longitude', 'latitude', 'tract_pop', 'tract_midincome', 'tract_geoid',
                              'tract_white_perc', 'tract_black_perc', 'tract_asian_perc', 'tract_his_perc',
                              'tract_other_perc']]

# Drop duplicate addresses based on the 'Address' column
final_merged_df = final_merged_df.drop_duplicates(subset=['Address'])

# Display the final dataset after dropping duplicates
print(final_merged_df.head())

# Save the final dataset without duplicates to a CSV file
final_merged_df.to_csv("property_service_line_census.csv", index=False)

# Optionally, print a message to confirm the file was saved
print("Final dataset with duplicates removed has been saved as 'final_merged_property_data_no_duplicates.csv'")
