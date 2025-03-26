## Merges service line data with matches assessor data
## Checks for matches in address and mailing_address column
## Saves a csv with matched data
## Saves a csvs for duplicate rows from address, mailing_address and service line address

import pandas as pd
import os    


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load CSV files
service_line = pd.read_csv("T096318_Responsive_Document.csv")
assessor = pd.read_csv("Assessor__Archived_05-11-2022__-_Property_Locations_20250225.csv")

# Some addresses recorded as Galvanized also have a duplicate record stating not lead
# To prevent matching each address unit to multiple records of same service line we will remove duplicates
# Keeping last match since the galvanized information seems to be at bottom but should probably clean data better
service_line.drop_duplicates(subset=["Address"], keep= "last")


# Rename property_address to address in assessor
assessor.rename(columns={"property_address": "address"}, inplace=True)
service_line.rename(columns={"Address": "address"}, inplace=True)


# Select columns we want to merge
assessor_selected = assessor[["address", "property_city", "property_zip", "mailing_address", "mailing_state", "latitude", "longitude", "township_name", "school_elem_district", "school_hs_district"]]

# Merge on address
merged_on_address = pd.merge(service_line, assessor_selected, on="address", how="inner")

# Merge on mailing_address separately
merged_on_mailing = pd.merge(service_line, assessor_selected, left_on="address", right_on="mailing_address", how="inner")

# Combine both matches to get all matched records
merged_combined = pd.concat([merged_on_address, merged_on_mailing])

# Count duplicate matches by address
# Looking through duplicates are caused by:
# Assessor: Duplicated due to units within an apartment. (Same address has different value in property_apt_no column)
# Service Line: Seems to have multiple records of same address if address uses galvanized service line. One stating not lead and another stating its galvanized
duplicate_count = merged_combined.duplicated(subset=["address"], keep=False).sum()

# Drop duplicates to get the final merged dataset
# Only drops rows that are completely similar (all columns), so multiple rows might still appear for same address based on conditions above
# From tests it looks like 
merged_matched = merged_combined.drop_duplicates()

# Save matches to CSV files.
merged_matched.to_csv("matched_addresses.csv", index=False)

# Create dataframes for duplicate addresses
# Allows us to see which addresses have multiple rows due to conditions listed above
service_line_duplicates = service_line[service_line.duplicated(subset=["address"], keep=False)]
assessor_duplicates = assessor[assessor.duplicated(subset=["address"], keep=False)]

# Save duplicates to CSV
# Duplicates are saved 
service_line_duplicates.to_csv("service_line_duplicates.csv", index=False)
assessor_duplicates.to_csv("assessor_address_duplicates.csv", index=False)

# I think this is important since addresses and mailing_addresses are not always similar
# I do think I need to find a way to filter out the data that is already present in the assessor_duplicates file
assessor_mailing_duplicates = assessor[assessor.duplicated(subset=["mailing_address"], keep=False)]
assessor_mailing_duplicates.to_csv("assessor_mailingaddress_duplicates.csv", index=False)

# Print summary
print(f"Total matched addresses saved: {len(merged_matched)}")
print(f"Total duplicate matches based on address before merging: {duplicate_count}")
print(f"Total duplicates in service line: {len(service_line_duplicates)}")
print(f"Duplicates in assessor:  {len(assessor_duplicates)}")