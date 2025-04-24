from utilities import *

def generate_host():
    # Extract host table based on ER diagram
    host_dataframe = listing_df[[
        "host_id", 
        "host_name", 
        "host_since", 
        "host_is_superhost", 
        "host_response_rate", 
        "host_response_time", 
        "host_acceptance_rate",
        "host_identity_verified", 
        "host_has_profile_pic", 
        "host_total_listings_count"
    ]].copy()

    # print(host_dataframe.isnull().sum()) # We check what missing values each column has:
    # host_id                         0
    # host_name                       1 -> fill with "Unknown"
    # host_since                      1 -> Leave null for visualization handling
    # host_is_superhost             224 -> Fill with 0 (meaning that they probably are not superhost if the value is missing)
    # host_response_rate           6468 -> Fill with 0%
    # host_response_time           6468 -> Leave null for visualization handling
    # host_acceptance_rate         3748 -> Fill with 0%
    # host_identity_verified          1 -> Fill with 0 (meaning that they probably are not verified if the value is missing)
    # host_has_profile_pic            1 -> Fill with 0 (meaning that they probably dont have a profile pic if the value is missing)
    # host_total_listings_count       1 -> Fill with 0


    host_dataframe["host_name"] = host_dataframe["host_name"].fillna("Unknown")
    host_dataframe["host_since"] = pd.to_datetime(host_dataframe["host_since"], errors="coerce") # We make sure the field is of datetime type
    host_dataframe["host_is_superhost"] = host_dataframe["host_is_superhost"].map({"t": 1, "f": 0}).fillna(0).astype(bool)  # Fill missing as 0 and convert t (true) to 1 and f (false) to 0
    host_dataframe["host_response_rate"] = host_dataframe["host_response_rate"].fillna("0%")  # Replace missing rates with 0%
    host_dataframe["host_acceptance_rate"] = host_dataframe["host_acceptance_rate"].fillna("0%")  # Replace missing with 0%
    host_dataframe["host_identity_verified"] = host_dataframe["host_identity_verified"].map({"t": 1, "f": 0}).fillna(0).astype(bool)  # Fill missing as 0
    host_dataframe["host_has_profile_pic"] = host_dataframe["host_has_profile_pic"].map({"t": 1, "f": 0}).fillna(0).astype(bool)  # Fill missing as 0
    host_dataframe["host_total_listings_count"] = host_dataframe["host_total_listings_count"].fillna(0).astype(int)


    # Save the host table as a CSV file
    host_dataframe.to_csv("analytical dataset/host.csv", index=False)