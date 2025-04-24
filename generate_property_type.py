from utilities import *

def generate_property_type():
    property_type_df = listing_df["property_type"].copy()
    # print(property_type_df.isnull().sum()) # Check for null values -> There are not null values

    unique_pt = property_type_df.drop_duplicates().reset_index(drop=True) # Unique property types

    unique_pt = pd.DataFrame(unique_pt, columns=["property_type"]) # Create a dataframe
    unique_pt["property_type_id"] = unique_pt.index + 1 # Add ids
    unique_pt = unique_pt[["property_type_id", "property_type"]] # Reorder columns to have ID first
    
    unique_pt.to_csv("analytical dataset/property_type.csv", index=False) # Save the dataframe