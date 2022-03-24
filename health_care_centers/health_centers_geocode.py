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
health_centers['long'] = ""
health_centers['lat'] = ""