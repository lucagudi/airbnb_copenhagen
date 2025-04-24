from utilities import *
from generate_amenity import *
from generate_host import *
from generate_neighbourhood import *
from generate_property_type import *
from generate_room_type import *
from generate_features import *
from generate_listing import *

# Generate dimension tables
print("Generating Amenity Table...")
generate_amenity()
print("Amenity Table Generated Successfully.\n")

print("Generating Host Table...")
generate_host()
print("Host Table Generated Successfully.\n")

print("Generating Neighbourhood Table...")
generate_neighbourhood()
print("Neighbourhood Table Generated Successfully.\n")

print("Generating Property Type Table...")
generate_property_type()
print("Property Type Table Generated Successfully.\n")

print("Generating Room Type Table...")
generate_room_type()
print("Room Type Table Generated Successfully.\n")

print("Generating Features Table...")
generate_features()
print("Features Table Generated Successfully.\n")

# Generate fact table
print("Generating Listing Table...")
generate_listing()
print("Listing Table Generated Successfully.\n")

print("All tables generated successfully!")