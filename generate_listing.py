from utilities import *

def adjust_rating(fact_table):
        # print(fact_table.isnull().sum()) # Check for null values
        # id                                0
        # number_of_reviews                 0
        # review_scores_rating           3220
        # review_scores_accuracy         3244
        # review_scores_cleanliness      3244
        # review_scores_checkin          3244
        # review_scores_communication    3244
        # review_scores_location         3245
        # review_scores_value            3245
        
        # I want to check whether the listings with 0 reviews have of course no rating:
        zero_reviews = fact_table[fact_table["number_of_reviews"] == 0] # Check listings with 0 reviews
        # print(zero_reviews.isnull().sum())
        # id                                0
        # number_of_reviews                 0
        # review_scores_rating           3220
        # review_scores_accuracy         3220
        # review_scores_cleanliness      3220
        # review_scores_checkin          3220
        # review_scores_communication    3220
        # review_scores_location         3220
        # review_scores_value            3220
        
        # As we can see this is the case for most listings with missing values
        # We of course fill listings with 0 reviews with value 0:
        fact_table.loc[fact_table["number_of_reviews"] == 0, [
            "review_scores_rating", 
            "review_scores_accuracy", 
            "review_scores_cleanliness", 
            "review_scores_checkin", 
            "review_scores_communication", 
            "review_scores_location", 
            "review_scores_value"
        ]] = 0.0
        
        # print(fact_table.isnull().sum()) # We now check again for null value
        # id                              0
        # number_of_reviews               0
        # review_scores_rating            0
        # review_scores_accuracy         24
        # review_scores_cleanliness      24
        # review_scores_checkin          24
        # review_scores_communication    24
        # review_scores_location         25
        # review_scores_value            25  
        
        # Since there are very few remaining null values, and we can safely assume that listings with ratings should have consistent scores across fields, we can fill the missing values in other fields using the overall rating (review_scores_rating) for those listings.
        
        # We first create a list of the rating fields that depend on the general rating
        rating_fields = ["review_scores_accuracy", "review_scores_cleanliness", "review_scores_checkin", "review_scores_communication", "review_scores_location", "review_scores_value"]
        for field in rating_fields:
            fact_table[field] = fact_table[field].fillna(fact_table["review_scores_rating"]) # We fill null values with the review_scores_rating
        fact_table[rating_fields + ["review_scores_rating"]] = fact_table[rating_fields + ["review_scores_rating"]].astype(float) # Ensure all rating columns remain float type
        

        # print(fact_table.isnull().sum())
        # id                             0
        # number_of_reviews              0
        # review_scores_rating           0
        # review_scores_accuracy         0
        # review_scores_cleanliness      0
        # review_scores_checkin          0
        # review_scores_communication    0
        # review_scores_location         0
        # review_scores_value            0
        return fact_table



def generate_listing():
    fact_table = listing_df[[
        "id",
        "host_id", # FK
        "name",
        "latitude",
        "longitude",
        "minimum_nights",
        "maximum_nights",
        "instant_bookable",
        "number_of_reviews",
        "review_scores_rating",
        "review_scores_accuracy",
        "review_scores_cleanliness",
        "review_scores_checkin",
        "review_scores_communication",
        "review_scores_location",
        "review_scores_value",
        "neighbourhood_cleansed", # Temporary column for mapping  
        "property_type", # Temporary column for mapping
        "room_type" # Temporary column for mapping
    ]].copy()
    
    fact_table = adjust_rating(fact_table)
    
    # We now need to add the foreign keys (neighbourhood_id, property_type_id and room_type_id)
    
    # Load the dimension tables
    neighbourhood_df = pd.read_csv("analytical dataset/neighbourhood.csv")
    property_type_df = pd.read_csv("analytical dataset/property_type.csv")
    room_type_df = pd.read_csv("analytical dataset/room_type.csv")
    
    # Neighbourhood
    fact_table["neighbourhood_cleansed"] = fact_table["neighbourhood_cleansed"].astype(str).str.strip().str.capitalize() # Format "neighbourhood_cleansed" in the same way as in the neighbourhood table
    fact_table = fact_table.merge(neighbourhood_df, on="neighbourhood_cleansed", how="left") # Map neighbourhood_cleansed to neighbourhood_i   
    
    # Property Type
    fact_table = fact_table.merge(property_type_df, on="property_type", how="left")

    # Room Type
    fact_table = fact_table.merge(room_type_df, on="room_type", how="left")
    
    # I import the clendar csv in order to extract the average price and the amount of days the property was booked for the year
    calendar_df = pd.read_csv("data/calendar2024.csv")
    
    calendar_df["price"] = calendar_df["price"].str.replace("[\$,]", "", regex=True).str.strip().astype(float) # Format the price field to float
    
   
    calendar_summary = calendar_df.groupby("listing_id").agg(
        average_price = ("price", "mean"),
        total_days = ("listing_id", "count"),
        booked_days=("available", lambda x: (x == "f").sum())
    ).reset_index() # Calculate additional metrics per listing
    
    calendar_summary["non_booked_days"] = calendar_summary["total_days"] - calendar_summary["booked_days"] # Add non-booked days
    calendar_summary["booking_percentage"] = round((calendar_summary["booked_days"] / calendar_summary["total_days"]) * 100, 2) # Add percentage of days in a year the property was booked

    # # Merge the calendar data into the fact table
    fact_table = fact_table.merge(calendar_summary, left_on="id", right_on="listing_id", how="left")
    
    
    
    # There is one issue we need to address. There are some properties that have 100% booking just because they have been blocked by the host, therefore resulting as "inactive". To clasify properties like this, we add a column called active with boolean values. 1 = the property is active; 0 = the property is not active. It is likely to assume that properties with 100% booking_percentage are unbookable, therefore not active.
    fact_table["active"] = fact_table["booking_percentage"].apply(lambda x: 0 if pd.isna(x) or x == 100 else 1).astype(bool)
    
    

    # # Drop the temporary column after mapping
    fact_table.drop(columns = ["neighbourhood_cleansed", "property_type", "room_type", "listing_id"], inplace=True)
    fact_table.to_csv("analytical dataset/listing.csv", index=False) # Save the dataframe