import requests
import geopandas
import json
import os
import dwmaps

CHART_ID = "HufI4"

r = requests.get("https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/BC_Flood_Advisory_and_Warning_Notifications_(Public_View)/FeatureServer/0/query?f=json&where=(Basin_Type%20=%20%27Y%27)%20AND%20(Advisory%20%3C%3E%201)&spatialRel=esriSpatialRelIntersects&geometry={%22xmin%22:-15196789.939130228,%22ymin%22:6215635.921167677,%22xmax%22:-12403475.17747749,%22ymax%22:8319182.939575167,%22spatialReference%22:{%22wkid%22:102100}}&geometryType=esriGeometryEnvelope&inSR=102100&outFields=OBJECTID,Major_Basin,Advisory,Sub_Basin,Basin_Type,Comments,Date_Modified&orderByFields=OBJECTID%20ASC&outSR=102100")

data = geopandas.read_file(json.dumps(r.json()))

data["stroke"] = data["Advisory"].replace(
    {
        1.0: "#f8c325",
        2.0: "#e06618",
        3.0: "#c42127"
    })

data["fill"] = data["stroke"]
data["opacity"] = 0.5
data['id'] = range(0, len(data))
data["id"] = data['id'].apply(lambda x: f"m{x}")
data["title"] = data["Advisory"].replace({1.0: "High Streamflow Advisory", 2.0: "Flood Watch", 3.0: "Flood Warning"})


chart = dwmaps.DatawrapperMaps(chart_id=CHART_ID)
dw = (chart
      .upload(data)
      .title("Current flood warnings in B.C.")
      .timestamp()
      )