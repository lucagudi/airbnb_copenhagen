from utilities import *

def generate_room_type():
    # Extract unique room types
    room_type_df = listing_df["room_type"].copy()

    # Create a dataframe with unique room types
    unique_rt = room_type_df.drop_duplicates().reset_index(drop=True)
    unique_rt = pd.DataFrame(unique_rt, columns=["room_type"])

    # Add IDs
    unique_rt["room_type_id"] = unique_rt.index + 1

    # Reorder columns
    unique_rt = unique_rt[["room_type_id", "room_type"]]

    # Save the CSV with proper encoding and no BOM
    unique_rt.to_csv("analytical dataset/room_type.csv", index=False, encoding="utf-8", sep=",")