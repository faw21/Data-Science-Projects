import json
import requests
import sys
import re
import pandas as pd
from math import cos, asin, sqrt

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def total_bikes():
    print('Command=' + command)
    print('Parameters=')
    
    print('Output=' + str(station_status['num_bikes_available'].sum()))

def total_docks():
    print('Command=' + command)
    print('Parameters=')
    print('Output=' + str(station_status['num_docks_available'].sum()))

def percent_avail(s_number):
    print('Command=' + command)
    print('Parameters=' + s_number)
    temp = station_status.loc[station_status['station_id']==s_number]
    print('Output=' + str(int(temp.num_docks_available/(temp.num_bikes_available+temp.num_docks_available)*100)) + '%')

def closest_stations(latitude, longtitude):
    print('Command=' + command)
    print('Parameters=' + latitude + ' ' + longtitude)

    df = pd.DataFrame(columns = ['station_id', 'name', 'dist'])
    for num in station_info.iterrows():
    	station = num[1]
    	dist = distance(station['lat'], station['lon'], float(latitude), float(longtitude))
    	df = df.append({'station_id':station['station_id'], 'name': station['name'], 'dist': dist}, ignore_index = True)
    	
    
    #print(df.head())
    df = df.sort_values(by=['dist'])
    print('Output=')
    print(df['station_id'].iloc[0] + ', ' + df['name'].iloc[0]) #+ ', ' + str(df['dist'].iloc[0]))
    print(df['station_id'].iloc[1] + ', ' + df['name'].iloc[1]) #+ ', ' + str(df['dist'].iloc[1]))
    print(df['station_id'].iloc[2] + ', ' + df['name'].iloc[2]) #+ ', ' + str(df['dist'].iloc[2]))

def closest_bike(latitude, longtitude):
    print('Command=' + command)
    print('Parameters=' + latitude + ' ' + longtitude)

    df = pd.DataFrame(columns = ['station_id', 'name', 'dist', 'num_bikes_available'])
    for num in station_info.iterrows():
    	station = num[1]
    	dist = distance(station['lat'], station['lon'], float(latitude), float(longtitude))
    	df = df.append({'station_id':station['station_id'], 'name': station['name'], 'dist': dist, 
    		'num_bikes_available': station_status.loc[station_status['station_id']==station['station_id']]['num_bikes_available']},
    		 ignore_index = True)

    df = df.sort_values(by=['dist'])
    for i in df.iterrows():
    	if station_status.loc[station_status['station_id']==i[1]['station_id']].num_bikes_available.iloc[0]>0:
    		print('Output=' + i[1]['station_id'] + ', ' + i[1]['name'])
    		return


def get_df(url):
    r = requests.get(url)
    temp = re.sub('[^[]*[[]','',str(r.json()))
    temp = re.sub(']}}','', temp)
    df = pd.DataFrame(eval(temp))
    return df



if len(sys.argv)<3:
    print ('usage: python3 mybikes.py baseURL command [parameter]')
    exit()
else:
    baseURL = sys.argv[1]
    command = sys.argv[2]


station_infoURL = baseURL + '/station_information.json'
station_statusURL = baseURL + '/station_status.json'


station_info = get_df(station_infoURL)
station_status = get_df(station_statusURL)



if command == 'total_bikes':
    total_bikes()
elif command == 'total_docks':
    total_docks()
elif command == 'percent_avail':
    percent_avail(sys.argv[3])
elif command == 'closest_stations':
    closest_stations(sys.argv[3], sys.argv[4])
elif command == 'closest_bike':
    closest_bike(sys.argv[3], sys.argv[4])
else:
    print('Invalid command! Please try again')

