import requests
import json
import os
import datetime
from datawrapper import Datawrapper

class DatawrapperMaps:
    
    CHART_ID = None
    
    def __init__(self, chart_id):
        self.CHART_ID = chart_id
        
    def __auth(self):
        try:
            with open('./auth.txt', 'r') as f:
                DW_AUTH_TOKEN = f.read().strip()
        except:
            DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']
            
        return DW_AUTH_TOKEN
        
    def upload(self, data):
        
        
        data = data.to_crs("EPSG:4326")
        data.to_file("floodwarnings.geojson", driver='GeoJSON')
        
        headers = {
            "Authorization": f"Bearer {self.__auth()}"
        }

        with open("floodwarnings.geojson", 'r') as f:
            geojson = json.load(f)
            
        features = geojson["features"]
        
        new_features = []
        
        for feature in features:
        
            new_feature = {'id': feature["properties"]["id"],
                'data': feature["properties"],
                'type': 'area',
                'title': feature["properties"]["title"],
                'visible': True,
                'fill': True,
                'stroke': True,
                'exactShape': False,
                'highlight': False,
                'icon': {'id': 'area',
                        'path': 'M225-132a33 33 0 0 0-10 1 38 38 0 0 0-27 28l-187 798a39 39 0 0 0 9 34 37 37 0 0 0 33 12l691-93 205 145a38 38 0 0 0 40 2 38 38 0 0 0 20-36l-54-653a38 38 0 0 0-17-28 38 38 0 0 0-32-5l-369 108-274-301a39 39 0 0 0-28-12z',
                        'horiz-adv-x': 1000,
                        'scale': 1.1,
                        'outline': '2px'},
                'feature': feature,
                'properties': {'fill': feature["properties"]["fill"],
                            'fill-opacity': feature["properties"]["opacity"],
                            'stroke': feature["properties"]["stroke"],
                            'stroke-width': 1,
                            'stroke-opacity': 1,
                            'stroke-dasharray': '100000',
                            'pattern': 'solid',
                            'pattern-line-width': 2,
                            'pattern-line-gap': 2},
                'visibility': {'mobile': True, 'desktop': True}
                }
            
            new_features.append(new_feature)

        with open("shapes/bc.json", 'r') as f:
            bc = json.load(f)
            new_features.append(bc)
            
        payload = {"markers": new_features}

        response = requests.put(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}/data", headers=headers, data=json.dumps(payload))

        print(response)
        
        return self
    
    def title(self, string):


        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__auth()}"
        }
        
        data = {
            "title": string
            }

        response = requests.patch(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}", headers=headers, data=json.dumps(data))


        print(response.text)
        
        return self
    
    def timestamp(self):
        
        dw = Datawrapper(access_token=self.__auth())
        
        today = datetime.datetime.today()
        time = today.strftime('%I:%M') + " " + ".".join(list(today.strftime('%p'))).lower() + "."
        day = today.strftime('%B %d, %Y')
    

        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__auth()}"
        }
        
        note = f"Last updated on {day} at {time}".replace(" 0", " ")
        
        data = {
            "annotate": {
                "notes": note
            }
        }

        requests.patch(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}", headers=headers, data=json.dumps(data))
        dw.update_metadata(chart_id=self.CHART_ID, properties=data)
        
        return self