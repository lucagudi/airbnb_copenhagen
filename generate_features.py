from utilities import *

def generate_features():
    features_df = listing_df[["id", "accommodates", "bathrooms", "bedrooms", "beds"]].copy()
    # print(features_df.isnull().sum())
    # id                 0
    # accommodates       0
    # bathrooms       7249
    # bedrooms         609
    # beds            7249
    
    # We use the number of accommodates as a predictor to estimate the likely values for bathrooms, bedrooms, and beds.
    # I also would like to further investigate this matter: could the room_type influance the presence of missing values?
    # Calculate percentage of missing values by room_type
    
    missing_percentage = listing_df.groupby("room_type")[["bathrooms", "bedrooms", "beds"]].apply(lambda x: x.isnull().mean() * 100)
    # print(missing_percentage)
    #                  bathrooms   bedrooms       beds
    # room_type
    # Entire home/apt  34.575112   0.420942  34.569850
    # Hotel room        0.000000   0.000000   0.000000
    # Private room     35.878270  27.923118  35.931660
    # Shared room      23.076923  23.076923  23.076923
    
    # We notice quite a correlation, therefore we want to assigne a realistic value that depends on the accomodates and the room_type. We take the median value
    features_df = listing_df[["id", "accommodates", "bathrooms", "bedrooms", "beds", "room_type"]].copy()

    # Ensure numeric types before processing
    features_df["bathrooms"] = pd.to_numeric(features_df["bathrooms"], errors="coerce")
    features_df["bedrooms"] = pd.to_numeric(features_df["bedrooms"], errors="coerce")
    features_df["beds"] = pd.to_numeric(features_df["beds"], errors="coerce")

    # Fill missing "bathrooms" based on room_type and accommodates median, keep as float with 1 decimal
    features_df["bathrooms"] = features_df["bathrooms"].fillna(
        features_df.groupby(["room_type", "accommodates"])["bathrooms"].transform("median")
    ).fillna(0.0).astype(float).round(1)

    # Fill missing "bedrooms" based on room_type and accommodates median, then convert to int
    features_df["bedrooms"] = features_df["bedrooms"].fillna(
        features_df.groupby(["room_type", "accommodates"])["bedrooms"].transform("median")
    ).fillna(0).astype(int)  # Fills missing values before conversion

    # Fill missing "beds" based on room_type and accommodates median, then convert to int
    features_df["beds"] = features_df["beds"].fillna(
        features_df.groupby(["room_type", "accommodates"])["beds"].transform("median")
    ).fillna(0).astype(int)  # Fills missing values before conversion

    # Handle any remaining null values by fallback to global median (though this should rarely happen now)
    features_df["bathrooms"] = features_df["bathrooms"].fillna(features_df["bathrooms"].median())
    features_df["bedrooms"] = features_df["bedrooms"].fillna(features_df["bedrooms"].median())
    features_df["beds"] = features_df["beds"].fillna(features_df["beds"].median())

    # Display final null values after imputation
    features_df = features_df[["id", "accommodates", "bathrooms", "bedrooms", "beds"]] # remove room_type
    # print(features_df.isnull().sum())
    # Missing values after imputation:
    # id              0
    # accommodates    0
    # bathrooms       0
    # bedrooms        0
    # beds            0
    
    features_df.to_csv("analytical dataset/features.csv", index=False)
    
generate_features()
    