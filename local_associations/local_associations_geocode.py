import googlemaps
import pandas as pd
import numpy as np
import requests
import time

from authentication import api_key

# Read in the excel file containing the addresses to be geocoded
local_associations = pd.read_excel("./local_associations/local_associations.xlsx")

# Drop the column 'Unnamed: 6' as it is empty (most likely an excel error)
local_associations = local_associations.drop(labels='Unnamed: 6', axis=1)

# Create columns for latitude and longitude in the dataframe so that the values can
# be written by the for loop below
local_associations['long'] = ""
local_associations['lat'] = ""

# Specify the API key for the googlemaps client
gmaps = googlemaps.Client(api_key)

# Loop over the rows in local_associations
for x in range(len(local_associations)):
    try:
        time.sleep(1) # to add delay so that google doesn't block you
        geocode_result = gmaps.geocode(local_associations['Address'][x]) # request the geocode result for the address in row x
        local_associations['lat'][x] = geocode_result[0]['geometry']['location'] ['lat'] # extract the lat from the responce
        local_associations['long'][x] = geocode_result[0]['geometry']['location']['lng'] # extract the long from the responce
        print(x) # print the row number so that you know the for loop is running
    except IndexError:
        print("Address was wrong...") # tell python what to do in case of an index error
    except Exception as e:
        print("Unexpected error occurred.", e ) # tell python what to do in case of an exception

print("Done!")

# The googlemaps API was unable to find one of the addresses in the dataframe (the observation with index 206)
local_associations_missing = local_associations[local_associations['lat'] == '']

# I manually found the address on google and retrieved the lat and long for the address. The address is 
# 秋田県湯沢市表町三丁目３番14号消防庁舎２階 which is for a fire station in Yuzawa City, Akita Prefecture 
local_associations['lat'][206] = 39.16865465609167
local_associations['long'][206] = 140.49059627273175

# Double check there are no missing locations
local_associations_missing = local_associations[local_associations['lat'] == '']

# Output the data to csv
local_associations.to_csv('./local_associations/local_associations_with_lat_lon.csv', index= False)