# project: MP3
# submitter: emanter
# partner: none
# hours: 5

from collections import deque as dq
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


from IPython.display import display, Image

import pandas as pd

import time
import requests

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ Record the node value in self.order, and return its children
        param: node
        return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        # 1. clear out visited set and order list
        self.visited.clear()
        self.order.clear()
        # 2. start recursive search by calling dfs_visit
        self.dfs_visit(node)
        
    def dfs_visit(self, node):
        
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return
        # 2. mark node as visited by adding it to the set
        self.visited.add(node)
        # 3. call self.visit_and_get_children(node) to get the children
        children = self.visit_and_get_children(node)
        # 4. in a loop, call dfs_visit on each of the children
        for child in children:
            self.dfs_visit(child)
        
    def bfs_search(self, node):
        self.visited.clear()
        self.order.clear()
        to_visit = dq([self])
        added = {self}
    
        children = self.visit_and_get_children(node)
        while len(to_visit) > 0:
            curr = to_visit.popleft()
            if curr in self.visited:
                return
            self.visited.add(node)
            for child in children:
                if child not in added:
                    to_visit.append(child)
                    added.add(child)
                    children.extend(self.visit_and_get_children(child))
        

class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def visit_and_get_children(self, node):
        # TODO: Record the node value in self.order
        children = []
        self.order.append(node)
        # TODO: use `self.df` to determine what children the node has and append them
        for node, has_edge in self.df.loc[node].items():
            if has_edge:
                children.append(node)
        return children
    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
    
    def visit_and_get_children(self, file):
        children = []
        with open(os.path.join("file_nodes", file)) as f:
            listy = f.read().split("\n")
            self.order.append(listy[0])
            children.extend(listy[1].split(","))
        return children
    
    def concat_order(self):
        s = ""
        for item in self.order:
            s += item
        return s

class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.tables = []
    
    
    def visit_and_get_children(self, url):
        self.driver.get(url)
        self.order.append(url)
        children = []
        for anchor in self.driver.find_elements("tag name", "a"):
            children.append(anchor.get_attribute("href"))
        self.tables.extend(pd.read_html(url))
        return children
    
    def table(self):
        return pd.concat(self.tables, ignore_index=True).dropna(axis = 1)


def reveal_secrets(driver, url, travellog):
    driver.get(url)
    word = "" 
    for item in travellog["clue"]:
        word += str(int(item))
    text = driver.find_element("id", "password-textbox")
    button = driver.find_element("id", "submit-button")
    text.send_keys(word)
    button.click()
    time.sleep(4)
    button1 = driver.find_element("id", "view-location-button")
    button1.click()
    time.sleep(4)
    wholesrc = driver.find_element("id", "image")
    ssrc = wholesrc.get_attribute("src")
    r = requests.get(ssrc)
    r.raise_for_status()
    pic = r.content
    with open("Current_Location.jpg", "wb") as f:
        f.write(pic)
    b = driver.find_element("id", "location")
    return b.text