import googlemaps
import pandas as pd
import numpy as np
import requests
import time

# Import the API key from the authentication file (this file is incuded in GitIgnore for privacy reasons)
from authentication import api_key

# Read in the excel file containing the addresses to be geocoded
health_centers = pd.read_excel("./health_care_centers/health_care_center.xlsx")

# Create columns for latitude and longitude in the dataframe so that the values can
# be written by the for loop below
health_centers['long'] = np.nan
health_centers['lat'] = np.nan

# Specify the API key for the googlemaps client
gmaps = googlemaps.Client(api_key)

# Loop over the rows in local_associations
for x in range(len(health_centers)):
    try:
        time.sleep(10) # to add delay so that google doesn't block you
        geocode_result = gmaps.geocode(health_centers['Address'][x]) # request the geocode result for the address in row x
        health_centers['lat'][x] = geocode_result[0]['geometry']['location'] ['lat'] # extract the lat from the responce
        health_centers['long'][x] = geocode_result[0]['geometry']['location']['lng'] # extract the long from the responce
        print(x) # print the row number so that you know the for loop is running
    except IndexError:
        print("Address was wrong...") # tell python what to do in case of an index error
    except Exception as e:
        print("Unexpected error occurred.", e ) # tell python what to do in case of an exception

print("Done!")

# Output the data to csv
health_centers.to_csv('./health_care_centers/health_care_center_with_lat_lon.csv', index= False)