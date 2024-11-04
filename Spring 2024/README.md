# Spring 2024 Projects

This repository contains various projects completed during the Spring 2024 semester as part of my **Data Science** studies at the University of Wisconsin-Madison.

## Overview

The projects in this repository showcase the intermediate-advanced steps for a major in Data Science, and highlights usage of Git commands/framework, objected-oriented programming, binary search trees, breadth and depth first searches, web scraping, building a website, regex, geopandas and geographical mapping, SQL queries, and machine learning. 

## Projects

### 1. MP1
- **Description**: This project is one that combines many different concepts and is meant as somewhat of a review of starting data science concepts. However, this project also intoduces git commands and git navigation, in addition to time complexity and the optimizing thereof. 
- **Key Techniques**: git commands, git structure, commits navigation, time complexity reduction, pandas
- **Files**: `mp1.ipynb`

### 1. MP2
- **Description**: This project introduces one of the most important structures in computer programming, the Binary Search Tree (BST) (and graphs/trees in general). Addtionally, it will focus on objected oriented programming and classes, as well as recursive processes. This project will apply these concepts by looking at every loan made in the state of Wisconsin in 2020 and perform various tasks with them.
- **Key Techniques**: Binary Search Trees, objected-oriented programming, classes, recursion, IO Wrappers
- **Files**: `MP2loans.py`, `MP2search.py`, `mp2.ipynb`, `banks.json`, `wi.zip`

### 1. MP3
- **Description**: One fantastic application of graphs and trees is that of a website and web scraping. This project will use web scraping, inheritance, breadth-first and depth-first searches (BFS, DFS), classes, and recursive web crawling to scrape a website and reveal various secrets needed to gain access to a password protected webpage. 
- **Key Techniques**: selenium module (web scraping, drivers), BFS, DFS, Inheritance, routing, pandas, scrape module, requests module 
- **Files**: `MP3scrape.py`, `file_nodes/*`

### 1. MP4
- **Description**: The next task is to turn our attention to making our own website, and implementing some techniques, plots, and libraries inside of it. This project is *massive* and involves many different moving parts and concepts. In this project we will look at data from the Securities and Exchange Commission, which public companies are required to upload all sorts of reports to. The logs of this organaization and publically available and the size of one day's worth of logs can be up to 2 GB. This project aims to use this trove of data in an efficient way by developing tools to extract information from the filings stored in EDGAR (the dataset) and then combine the findings with a self-built website that displays the analysis of user behavior and edgar visualization. Addtionally, we will correspond the filings with zip code logs in order to find out where and when reports are made, and then use geopandas to geographically visualize it. We will also implement A/B testing on this website. 
- **Key Techniques**: Big Data, URL reconstruction, regex, encoding, flask, correspondance, netaddr, rate limiting, A/B testing, visualization with geopandas, matplotlib, shape (shp) files, shapely geometry
- **Files**: `MP4.py`, `MP4edgar_utils.py`, `MP4index.html`, `MP4.py`, `docs.zip`, `server_log.zip`, `shapes/*`, `locations.geojson`

### 1. MP5
- **Description**: Shifting gears, we will now look to open our eyes to the field of machine learning. In order to do this, we wil continue to better our skills using geopandas, but supplement it with SQL queries and SKlearn's machine learning modules, and we will introduce masking of data with raster. The end goal is to make predictions about census data for Wisconsin using regression models.
- **Key Techniques**: SQL queries/usage, geopandas, shape (shp) files, shapely geometry, masking with raster, SKLearn module, machine learning
- **Files**: `mp5.ipynb`, `counties_tracts.db`, `counties.geojson`, `tracts.*`

### 1. MP6
- **Description**: This project is one that combines many different concepts and is meant as somewhat of a review of starting data science concepts. However, this project also intoduces git commands and git navigation, in addition to time complexity and the optimizing thereof. 
- **Key Techniques**: git commands, git structure, commits navigation, time complexity reduction, pandas
- **Files**: `MP6.py`, 
