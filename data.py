# URL : https://www.airbnb.com/api/v2/explore_tabs?version=1.3.9&satori_version=1.0.4&_format=for_explore_search_web&experiences_per_grid=20&items_per_grid=18&guidebooks_per_grid=20&auto_ib=true&fetch_filters=true&has_zero_guest_treatment=false&is_guided_search=true&is_new_cards_experiment=true&luxury_pre_launch=false&query_understanding_enabled=true&show_groupings=true&supports_for_you_v3=true&timezone_offset=-360&client_session_id=ba9ab095-4fc9-4005-b1c6-ead0b7d86719&metadata_only=false&is_standard_search=true&refinement_paths%5B%5D=%2Fhomes&selected_tab_id=home_tab&place_id=ChIJDYt7zkUSVIcRjm8CuWUqz-E&allow_override%5B%5D=&s_tag=i3cGuJZd&screen_size=medium&query=Garden%20City%2C%20Utah%2C%20United%20States&_intents=p1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=en
# Access Key ID: AKIAIZ3ZC5AOHIPDD5KA
# Secret Access Key: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

# importing the requests library
import requests
import datetime
import json
import boto
import boto.s3.connection
from boto.s3.key import Key

debug = False

access_key = "<access_key>"
secret = "<secret>"
listing_bucket = "hc-airbnb-data"
calendar_bucket = "hc-airbnb-data"
locale = "garden_city"

date = datetime.datetime.today().strftime('%Y-%m-%d')

# api-endpoint
listings_url = "https://www.airbnb.com/api/v2/explore_tabs"

 
# defining a params dict for the parameters to be sent to the API
PARAMS = {
    "https://www.airbnb.com/api/v2/explore_tabs?version":"1.3.9",
    "satori_version":"1.0.4",
    "_format":"for_explore_search_web",
    "experiences_per_grid":"0",
    "items_per_grid":"500",  # Change this to the number of listings to return
    "guidebooks_per_grid":"0",
    "auto_ib":"true",
    "fetch_filters":"true",
    "has_zero_guest_treatment":"false",
    "is_guided_search":"true",
    "is_new_cards_experiment":"true",
    "luxury_pre_launch":"false",
    "query_understanding_enabled":"true",
    "show_groupings":"true",
    "supports_for_you_v3":"true",
    "timezone_offset":"-360",
    "client_session_id":"ba9ab095-4fc9-4005-b1c6-ead0b7d86719",
    "metadata_only":"false",
    "is_standard_search":"true",
    "refinement_paths%5B%5D":"%2Fhomes",
    "selected_tab_id":"home_tab",
    "place_id":"ChIJDYt7zkUSVIcRjm8CuWUqz-E",
    "allow_override%5B%5D":"",
    "s_tag":"i3cGuJZd",
    "screen_size":"medium",
    "query":"Garden%20City%2C%20Utah%2C%20United%20States",
    "_intents":"p1",
    "key":"d306zoyjsyarp7ifhu67rjxn52tv0t20",
    "currency":"USD",
    "locale":"en"
}
 
# sending get request and saving the response as response object
r = requests.get(url = listings_url, params = PARAMS)
 
# extracting data in json format
data = r.json()


listings = data['explore_tabs'][0]['sections'][1]['listings']
listings_arr = []
listing_id_arr = []
for key in listings:
     listings_arr.append(str(key))
     listing_id_arr.append(key['listing']['id'])


listings_string = ''.join(listings_arr)

# write to s3
# s3 = boto3.resource('s3')
# object = s3.Object('my_bucket_name', 'hc-airbnb-data/'+date)
# object.put(Body=some_binary_data)

if debug is not True:
    # write to S3 - deprecated boto
    conn = boto.connect_s3(access_key, secret)
    bucket = conn.get_bucket(listing_bucket, validate=False)
    k = Key(bucket)
    k.key = locale+"/listings/"+date
    k.set_contents_from_string(listings_string)

# Get Calendar Data
#https://www.airbnb.com/api/v2/calendar_months?_format=with_conditions&count=4&listing_id=20094028&month=8&year=2018&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=en

calendar_url = "https://www.airbnb.com/api/v2/calendar_months"

params = {
    "_format":"with_conditions",
    "count":"14",
    "month":"7",
    "year":"2018",
    "key":"d306zoyjsyarp7ifhu67rjxn52tv0t20",
    "currency":"USD",
    "locale":"en"
}

calendar_data = []

for count, value in enumerate(listing_id_arr):
    params['listing_id'] = value
    r = requests.get(url = calendar_url, params = params)
    data = r.json()
    calendar_data.append(str(data))
    
calendar_string = ''.join(calendar_data)

if debug is not True:
    # write to S3 - deprecated boto
    bucket = conn.get_bucket(calendar_bucket, validate=False)
    k = Key(bucket)
    k.key = locale+"/calendar/"+date
    k.set_contents_from_string(calendar_string)

