## Checks assessor addresses for matches in service line database
## Checks for matches in address and mailing_address column
## Saves a csv file with all assessor data and where a match was found if any
## Saves a csv file with addresses only found in asessor data
## Saves a csv file with only addresses that had a match

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

# Rename address columns in each dataset to address
assessor.rename(columns={"property_address": "address"}, inplace=True)
service_line.rename(columns={"Address": "address"}, inplace=True)

# Check if assessor address is in service_line address
assessor["matched_on_address"] = assessor["address"].isin(service_line["address"])
assessor["matched_on_mailing"] = assessor["mailing_address"].isin(service_line["address"])

# Determine match status (address, mailing_address, or no match)
# Determine match status (address, mailing_address, or no match)
assessor["match_status"] = assessor.apply(
    lambda row: "Matches on Address and Mailing Address" if row["matched_on_address"] and row["matched_on_mailing"]
    else ("Matches on Address" if row["matched_on_address"]
    else ("Matches on Mailing Address" if row["matched_on_mailing"]
    else "Only in Assessor")),
    axis=1
)


# Filter out addresses that are only in assessor or have a match
only_in_assessor = assessor[assessor["match_status"] == "Only in Assessor"]
assessor_match = assessor[assessor["match_status"].isin(["Matches on Address", "Matches on Mailing Address"])]

# Print summary
print(f"Total rows in assessor: {len(assessor)}")
print(f"Total rows in service_line: {len(service_line)}")

print(f"Matches on Address: {sum(assessor['match_status'] == 'Matches on Address')}")
print(f"Matches on Mailing Address: {sum(assessor['match_status'] == 'Matches on Mailing Address')}")
print(f"Only in Assessor: {len(only_in_assessor)}")

# Save results
assessor.to_csv("assessor_match_status.csv", index=False)
only_in_assessor.to_csv("only_in_assessor.csv", index=False)
assessor_match.to_csv("assessor_matches.csv")
