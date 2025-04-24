# Airbnb Data Preparation and Cleaning

This repository contains Python code for preparing and cleaning Airbnb datasets for visualization in Tableau.

## Overview

The project transforms raw Airbnb listing data into a structured analytical database using a dimensional modeling approach with fact and dimension tables. The cleaned data is stored in CSV format for seamless integration with Tableau.

## Dataset

Download the dataset from [Google Drive Link]([https://drive.google.com/drive/folders/your-folder-id](https://drive.google.com/file/d/1b_6Xmv18RqVj7FD3m5uK8P0GfIZInjk4/view?usp=sharing))

## Data Preparation Process

### Initial Cleaning
- Removed irrelevant columns (listing_url, scrape_id, last_scraped, source, etc.)
- Dropped columns with >35% missing values
- Removed rows with >25% missing values

### Dimension Tables Creation

#### Host Table
- Selected relevant host-related columns
- Filled missing values in most fields with 0
- Preserved null values in host_response_time for specific handling during visualization
- Corrected data types and formatting

#### Neighbourhood Table
- Created from neighbourhood_cleansed field
- Standardized formatting
- Assigned unique IDs to each neighborhood

#### Property Type and Room Type Tables
- Identified unique values
- Assigned unique IDs to each distinct type

#### Features Table
- Implemented data-driven imputation strategy for missing values
- Filled missing values in bathrooms and beds based on room type and accommodates
- Used median values within groups
- Converted bedrooms and beds to integers
- Stored bathrooms as floats to accommodate fractional values

#### Amenity and Listing Amenity Tables
- Created to establish many-to-many relationships
- Cleaned amenities text using regular expressions:
  - Removed extra spaces
  - Trimmed unnecessary characters (brackets, quotes, hyphens)
  - Corrected spacing before percentage symbols
- Assigned unique IDs to each amenity
- Mapped listings to their respective amenities

### Fact Table (Listing Table)
- Handled null values in review-related fields
- Filled review scores with 0.0 for listings with zero reviews
- Used overall rating to fill remaining null values in dependent fields
- Added calculated metrics from calendar data:
  - Average price
  - Total days available
  - Booked days
  - Booking percentage
- Added 'active' boolean field to flag suspicious booking patterns

## Analytical Tools and Methods

- **Pandas**: Core library for data manipulation
- **Regular Expressions (re)**: Used for preprocessing textual data
- **Data Imputation Techniques**:
  - Median-based imputation for numerical fields
  - Zero-based filling for listings with no reviews
  - Cascaded imputation for review scores
- **Error Handling**: Implemented throughout scripts

## CSV vs SQL Database

CSV format was chosen over SQL for:
- Simplicity and efficiency with manageable dataset size
- Native compatibility with Tableau
- Pre-processed datasets ready for visualization
- Effective modeling of relationships through the CSV format

## Usage

```python
# Example usage of the data cleaning scripts
import pandas as pd
import re

# Load the raw data
listings_df = pd.read_csv('listing2024.csv')

# Run the cleaning and preparation functions
clean_listings = clean_listings_data(listings_df)

# Export the cleaned data
clean_listings.to_csv('clean_listings.csv', index=False)
```

## Tableau Integration

The prepared CSV files can be directly imported into Tableau for visualization and dashboard creation.
