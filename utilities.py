import pandas as pd
import re

listing_df = pd.read_csv("data/listings2024.csv")

# We drop the fields that will not be useful in the analysis nor in the creation of the analytical database
listing_df.drop(columns = [
    "listing_url",
    "scrape_id", 
    "last_scraped", 
    "source", 
    "description",
    "neighborhood_overview",
    "picture_url",
    "host_thumbnail_url",
    "host_picture_url",
    "calendar_updated",
    "calendar_last_scraped",
    "first_review",
    "last_review",
    "license",
    ], inplace=True)

# We drop columns with more than 35% of missing values:
threshold = len(listing_df) * 0.35
missing_counts = listing_df.isnull().sum()
dropped_columns = missing_counts[missing_counts > threshold].index.tolist()
listing_df = listing_df.drop(columns=dropped_columns)

# We drop rows with more than 25% of missing values:
threshold = len(listing_df.columns) * 0.25
listing_df = listing_df.dropna(axis=0, thresh=len(listing_df.columns) - threshold)

# After checking the datatype we change those which are wrong
listing_df["instant_bookable"] = listing_df["instant_bookable"].astype(bool)