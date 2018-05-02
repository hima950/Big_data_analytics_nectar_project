
import json
import os
import time
import yaml
os.chdir('../')
from api.couch_db import TweetsDB
from glob import glob
import pandas as pd

with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


#db connections
couch_db_conf = cfg['COUCHDB']
#create an instance of TWEETSDB and pass the connection details
couch_db = TweetsDB(couch_db_conf)


df = pd.read_csv('notebooks/SA2_2016_AUST.csv')



columns = ['SA4_CODE_2016', 'SA4_NAME_2016', 'GCCSA_NAME_2016', 'STATE_NAME_2016']

mappings_df = df[columns].drop_duplicates().set_index('SA4_CODE_2016')
mappings_df.head()

with open('notebooks/SA4_data_for_geotagging.json', 'r') as fp:
    data = json.load(fp)

features = data['features']

from shapely.geometry import Point, Polygon

def geo_check(coordinates):
    if isinstance(coordinates[0], list):              #check if polygon
        coordinate_polygon = Polygon(coordinates[0])
        pnt = Point(coordinate_polygon.centroid)

    else:
        pnt = Point(coordinates)
         
    for i in range(len(features)):
        for j in range(len(features[i]['geometry']['coordinates'])):
     
            poly = Polygon(features[i]['geometry']['coordinates'][j][0])
            idx = int(features[i]['properties']['sa4_code16'])
            
            if pnt.within(poly):
                return {'SA4_name':features[i]['properties']['feature_name'],
                        'SA4_code':idx,
                        'GCCSA_name':mappings_df.loc[idx]['GCCSA_NAME_2016'],
                        'State_name':mappings_df.loc[idx]['STATE_NAME_2016']}
                break
            
            elif pnt.touches(poly):
                return {'SA4_name':features[i]['properties']['feature_name'],
                        'SA4_code':idx,
                        'GCCSA_name':mappings_df.loc[idx]['GCCSA_NAME_2016'],
                        'State_name':mappings_df.loc[idx]['STATE_NAME_2016']}
                break
            


def none_geo_check(coordinates):
    dist_from_point = []
    dist_point_id = []
    if isinstance(coordinates[0], list):              #check if polygon
        coordinate_polygon = Polygon(coordinates[0])
        pnt = Point(coordinate_polygon.centroid)

    else:
        pnt = Point(coordinates)
         
    for i in range(len(features)):
        for j in range(len(features[i]['geometry']['coordinates'])):
     
            poly = Polygon(features[i]['geometry']['coordinates'][j][0])
            
            dist_from_point.append(poly.exterior.distance(pnt))
            dist_point_id.append(i)
            

    min_index = dist_point_id[dist_from_point.index(min(dist_from_point))]   
    idx = int(features[min_index]['properties']['sa4_code16'])
    return {'SA4_name':features[min_index]['properties']['feature_name'],
                        'SA4_code':idx,
                        'GCCSA_name':mappings_df.loc[idx]['GCCSA_NAME_2016'],
                        'State_name':mappings_df.loc[idx]['STATE_NAME_2016']}


geo_tasks_path= cfg['QUEUES']['geo_tasks']

i = 1
while True:
    geo_tweets = glob('{}/*.txt'.format(geo_tasks_path))
 
    for path in geo_tweets:
        try:
            tweet_id = path.split('/')[-1].split('.')[0]
            with open(path, 'r') as fp:
                geo = json.load(fp)
            geo_doc =geo_check(geo['coordinates'])
            if geo_doc== None:
                none_geo = none_geo_check(geo['coordinates'])
                couch_db.update_document(tweet_id,none_geo)
            else:             
                couch_db.update_document(tweet_id,geo_doc)
            try:
                os.remove(path)
            except Exception as e:
                           # if failed, report it back to the user 
                print("Error: {} .".format(e))
        except Exception as e:
            print('Tweet {} wasn\'t geotagged and updated on DB due to error. {}'.format(tweet_id, e))
         
    print('Iteration: {}\tFiles processed: {}'.format(i, len(geo_tweets)))
    i+=1
    time.sleep(18)

