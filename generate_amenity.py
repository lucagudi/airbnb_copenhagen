from utilities import *
import re


def generate_amenity():
    listings_amenities = []
    # Extract amenities column
    amenities_series = listing_df[["id", "amenities"]]

    # Initialize an empty set to store unique amenities
    unique_amenities = set()

    # Preprocess and clean amenities
    def process_amenities(amenities):
        amenities = amenities.encode("utf-8").decode("unicode_escape")
        return [
            re.sub(r'\s+', ' ', am.strip(' "[].-')).strip('"').replace(" %", "%")  # Normalize spaces, trim characters, and remove quotes
            for am in amenities.split('",')
            if am.strip(' "[].-')
        ]

    # Iterate through each row and extract amenities
    for idx, amenities in amenities_series.itertuples(index=False):
        try:
            amenities_list = process_amenities(amenities)
            unique_amenities.update(amenities_list)
        except Exception as e:
            print(f"Error parsing amenities for id {idx}: {e}")

    # Create a dictionary with numerical IDs
    amenities_dict = {i + 1: key for i, key in enumerate(sorted(unique_amenities))}

    # Map listing_id to amenity IDs
    for idx, amenities in amenities_series.itertuples(index=False):
        try:
            amenities_list = process_amenities(amenities)
            for amenity in amenities_list:
                amenity_id = next((k for k, v in amenities_dict.items() if v == amenity), None)
                if amenity_id:
                    listings_amenities.append((idx, amenity_id))  # Append to listing-amenity mapping
        except Exception as e:
            print(f"Error mapping amenities for id {idx}: {e}")

    # Save the amenities dictionary as a CSV file
    amenities_df = pd.DataFrame(amenities_dict.items(), columns=["id", "amenity"])
    amenities_df.to_csv("analytical dataset/amenities.csv", index=False)

    # Save listing-amenities mapping
    listing_amenities_df = pd.DataFrame(listings_amenities, columns=["listing_id", "amenity_id"])
    listing_amenities_df.to_csv("analytical dataset/listing_amenities.csv", index=False)