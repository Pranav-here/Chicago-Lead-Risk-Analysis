## Checks service line addresses for matches in assessor database
## Checks for matches in address and mailing_address column
## Saves a csv file with addresses only found in service line data
## Saves a csv file with all service line data and where a match was found if any
import pandas as pd
import os    


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load CSV files
service_line = pd.read_csv("T096318_Responsive_Document.csv")
assessor = pd.read_csv("Assessor__Archived_05-11-2022__-_Property_Locations_20250225.csv")

service_line.drop_duplicates(subset=["Address"], keep= "last")


# Rename property_address to address in assessor
assessor.rename(columns={"property_address": "address"}, inplace=True)
service_line.rename(columns={"Address": "address"}, inplace=True)


# Merge on address
merge_address = pd.merge(service_line, assessor, on="address", how="left", indicator=True)
# Merge on mailing_address separately
merge_mailing = pd.merge(service_line, assessor, left_on="address", right_on="mailing_address", how="left", indicator=True)

# Combine results to check if a match exists in either column
service_line["matched_on_address"] = service_line["address"].isin(assessor["address"])
service_line["matched_on_mailing"] = service_line["address"].isin(assessor["mailing_address"])

# Determine match status. Where we get a match in the assessors database (address, mailing_address, no match)
service_line["match_status"] = service_line.apply(
    lambda row: "Matched on Address and Mailing Address" if row["matched_on_address"] and row["matched_on_mailing"]
    else ("Matched on Address" if row["matched_on_address"]
    else ("Matched on Mailing Address" if row["matched_on_mailing"]
    else "Only in Service Line")),
    axis=1
)

# Filter out addresses that are only in service_line
only_in_service_line = service_line[service_line["match_status"] == "Only in Service Line"]

# Print summary
print(f"Total rows in service_line: {len(service_line)}")
print(f"Total rows in asessor: {len(assessor)}")

print(f"Matched on Address: {sum(service_line['match_status'] == 'Matched on Address')}")
print(f"Matched on Mailing Address: {sum(service_line['match_status'] == 'Matched on Mailing Address')}")
print(f"Only in Service Line: {len(only_in_service_line)}")

# Save results
only_in_service_line.to_csv("only_in_service_line.csv", index=False)
service_line.to_csv("service_line_match_status.csv", index=False)
