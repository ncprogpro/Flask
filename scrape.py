import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as r
import os
import re
import json
# Site URL
site_url = 'http://jinya-ramenbar.com'

# Location URL
location_url = 'https://beachhutdeli.com/locations/'

# output path of CSV
output_path = os.path.dirname(os.path.realpath(__file__))

# file name of CSV output
file_name = 'data.csv'


# Function pull webpage content

def pull_content(url):

    soup = bs(r.get(url).content,'html.parser')

    return soup

def pull_content_json(url):

    results = r.get(url)

    return results.json()


def pull_info(content):
 
    store_data = []

    state_list = soup.find('select',{'id':'select-state'}).find_all('option')

    for state_item in state_list:
        state = state_item['value']
        if state != '0':
            href_url = location_url + 'results/?state=' + state
            content_store = pull_content_json(href_url)
            for item_content in content_store:
                locator_domain = href_url
                location = item_content['location']
                location_name = item_content['post_name']
                store_number = item_content['info']['store_number']
                if item_content['info']['phone'] == '':
                    phone = "<MISSING>"
                else:
                    phone = item_content['info']['phone']
                store_type = "<MISSING>"
                zip = location['zip']
                city = location['city']
                state = location['state']
                street_address = location['address']
                country_code = 'US'
                longitude = str(location['longitude']).split(',')[0]
                latitude = location['latitude']
                if item_content['info']['hours'] == '':
                    ul_for_hours = "<MISSING>"
                else:
                    ul_for_hours = str(item_content['info']['hours']).replace('<br />','')
          
                temp_data = [

                locator_domain,

                location_name,

                street_address,

                city,

                state,

                zip,

                country_code,

                store_number,

                phone,

                store_type,

                latitude,

                longitude,

                ul_for_hours

                ]
                store_data = store_data + [temp_data]


    final_columns = [

        'locator_domain',

        'location_name',

        'street_address', 

        'city',

        'state',

        'zip',

        'country_code',

        'store_number',

        'phone',

        'location_type',

        'latitude',

        'longitude',

        'hours_of_operation']

    final_df = pd.DataFrame(store_data,columns=final_columns)

    return final_df
         
            
  

  

                         



# # Pull URL Content

soup = pull_content(location_url)

# # Pull all stores and info

final_df = pull_info(soup)




# # write to csv

final_df.to_csv(output_path + '/' + file_name,index=False)