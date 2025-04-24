from utilities import *

def generate_neighbourhood():
    neighbourhood_df = listing_df[["neighbourhood_cleansed"]].copy() # Create a dataframe with unique neighbourhoods
    # print(neighbourhood_df.isnull().sum()) # Check for null values
    neighbourhood_df["neighbourhood_cleansed"] = neighbourhood_df["neighbourhood_cleansed"].astype(str).str.strip().str.capitalize()  # Standardize and clean "neighbourhood_cleansed"
    unique_neighbourhoods = neighbourhood_df["neighbourhood_cleansed"].drop_duplicates().reset_index(drop=True) # Extract unique neighbourhoods
    unique_neighbourhoods_df = pd.DataFrame(unique_neighbourhoods, columns=["neighbourhood_cleansed"]) # Create a dataframe with IDs
    unique_neighbourhoods_df["neighbourhood_id"] = unique_neighbourhoods_df.index + 1
    unique_neighbourhoods_df = unique_neighbourhoods_df[["neighbourhood_id", "neighbourhood_cleansed"]] # Reorder columns to have ID first
    
    unique_neighbourhoods_df.to_csv("analytical dataset/neighbourhood.csv", index=False) # Save the dataframe