import pandas as pd
from flask import Flask, request, jsonify
import flask
import time
from collections import OrderedDict
import zipfile
import edgar_utils
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import geopandas as gpd
import re
import io
from shapely.geometry import Point, Polygon, box
import os
import csv

app = Flask(__name__)
last_requests = {}
ip_list = []
counter = 0
a = 0
b = 0

@app.route('/')
def home():
    with open("index.html") as f:
        html = f.read()
    global counter
    global a
    global b
    if counter % 2 == 1 and counter <10:
        #show version b
        html = html.replace('<a href="donate.html">Donate</a>', '<a href="donate.html?from=B">DONATE</a>')
    elif counter % 2 == 0 and counter <10:
        #show version a
        html = html.replace('<a href="donate.html">Donate</a>', '<a href="donate.html?from=A">donate</a>')
    else:
        if  a > b:
            html = html.replace('<a href="donate.html">Donate</a>', '<a href="donate.html?from=A">donate</a>')
        else:
            html = html.replace('<a href="donate.html">Donate</a>', '<a href="donate.html?from=B">DONATE</a>')
    counter += 1
    return html

@app.route('/donate.html')
def donate_html():
    global a
    global b
    global counter
    url = request.args.get("from")
    if counter <10 and url == "A":
        a += 1
    elif counter <10 and url == "B":
        b += 1
    return "<h1>Donation<h1><html>{}<html>".format("please give me money")

@app.route('/browse.html')
def browsehtml():
    needed = pd.read_csv("server_log.zip", compression = "zip")
    html = needed[:500].to_html()
    return "<h1>Browse first 500 rows of rows.csv</h1<html>{}<html>".format(html)

@app.route("/browse.json")
def browsejson():
    needed = pd.read_csv("server_log.zip", compression = "zip")
    dicty = needed[:500].to_dict()
    global last_requests
    global ip_list
    #limit to a request per min
    address = request.remote_addr
    if address in last_requests:
        last_request_time = time.time() - last_requests[address]
        if last_request_time < 60:
            return flask.Response("<b>go away</b>",
                              status=429,
                              headers={"Retry-After": "60"})
    last_requests[address] = time.time()
    ip_list.append(address)
    return jsonify(dicty)
    
    
@app.route("/analysis.html")
def q():
    serverlog = pd.read_csv("server_log.zip", compression = "zip")
    serie = serverlog.to_dict()
    series = pd.Series(serie["ip"])
    
    counts = series.value_counts()
    # Convert counts to a pandas Series and sort by values
    se = pd.Series(counts.values, index=counts.index)
    s = se.sort_values()
    a = s[-10:].to_dict()
    

    sorted_dict = {key: value for key, value in sorted(a.items(), key=lambda item: item[1], reverse = True)}
    
    string = """
                <p>Q1: how many filings have been accessed by the top ten IPs?</p>
                <p>?1?</p>
                <p>Q2: what is the distribution of SIC codes for the filings in docs.zip?</p>
                <p>?2?</p>
                <p>Q3: what are the most commonly seen street addresses?</p>
                <p>?3?</p>
                <h4>Dashboard: geographic plotting of postal code</h4>
                <img src ="/dashboard.svg">
                
                
            """
    
    # QUESTION 2
    zip_file_path = 'docs.zip'
    dicti = {}
    alldata = {}
    
    # Open the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Get the list of file names within the zip file
        file_names = zip_ref.namelist()

        # Iterate over each file name
        for file_name in file_names:
            if "htm" in file_name:
                # Open the file within the zip file
                with zip_ref.open(file_name) as file:
                    # Read the content of the file
                    file_content = file.read()
                    content = file_content.decode("utf-8")
                    if file_name != None:
                        dicti[file_name] = edgar_utils.Filing(content).sic
                        alldata[file_name] = edgar_utils.Filing(content)
                
    filtered = {key: value for key, value in dicti.items() if value is not None}
    counts = pd.Series(filtered).value_counts()
    series_sorted = pd.Series(counts.values, index = counts.index).sort_values(ascending = True)
    
    topbit = series_sorted.to_dict()
    
    top10 = sorted(topbit.items(), key=lambda l: (l[1],l[0]), reverse = True)
    top10 = top10[:10]
    
    top10sort = {key: value for key, value in sorted(top10, key=lambda item: item[1], reverse = True)}
    
    
    #QUESTION 3
    newone = []
    zipfil = zipfile.ZipFile("server_log.zip")
    z = zipfil.open("rows.csv")
    reader = csv.DictReader(io.TextIOWrapper(z))
    
    
    for row in reader:
        newone.append((row["cik"][:-2])+"/"+(row["accession"])+"/"+(row["extention"]))
    
    hi = {}
    for name in newone:
        if name in alldata:
            for address in alldata[name].addresses:
                if address not in hi:
                    hi[address] = 1
                else:
                    hi[address] += 1
    
    finaldict = {key: value for key, value in hi.items() if value >= 300}
        
        
    return string.replace("?1?", f"{sorted_dict}").replace("?2?", f"{top10sort}").replace("?3?", f"{finaldict}")



    
@app.route("/dashboard.svg")
def display():
    path = "locations.geojson"
    gdf = gpd.read_file(path)
    
    fig, ax = plt.subplots()
    shape = gpd.read_file('shapes/cb_2018_us_state_20m.shp')
    
    
    co = r"(\d\d\d\d\d)[-\d\d\d\d]?"
    gdf['postal_code'] = gdf['address'].str.findall(co).apply(lambda l: l[0] if l else None)
    
    # Fill NaN values with a integer placeholder
    gdf['postal_code'] = gdf['postal_code'].fillna(-1)
    
    # Convert postal codes to integers, using astype
    gdf['postal_code'] = gdf['postal_code'].astype(int)
    
    gdf_filtered = gdf[(gdf['postal_code'] >= 25000) & (gdf['postal_code'] <= 65000)]
    
    gdf_filtered = gdf_filtered.cx[-95:-60, 25:50]
    shape = shape.intersection(box(-95, 25, -60, 50))
    
    gdf_filtered = gdf_filtered.to_crs("epsg:2022")
    shape = shape.to_crs("epsg:2022")
    
    shape.plot(ax=ax, facecolor = "lightgray")
    gdf_filtered.plot(ax = ax, column='postal_code', cmap='RdBu', legend = True)  
    
    ax.set_axis_off()
    
    #save and return the picture
    f = io.StringIO()
    fig.savefig("dashboard.svg", format="svg")
    fig.savefig(f, format="svg")
    plt.close()
    
    return flask.Response(f.getvalue(), headers={"Content-type": "image/svg+xml"})
    
@app.route("/visitors.json")
def visitors_json():
    global ip_list
    return ip_list

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

#define no more functions below this, they won't run