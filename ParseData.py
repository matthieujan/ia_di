from lxml import etree
import hashlib
import time
import os
import json
import requests
import sys
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def parse_file(path):
    """From a specific path, parse the file"""
    from io import StringIO, BytesIO
    print("Parsing file : " + path)
    tree = etree.parse(path)

    flowDict = {}

    for element in tree.getroot():
        item_dict = {}
        flow_key_raw = ''
        for subElement in element:
            item_dict[subElement.tag] = subElement.text
            if isinstance(subElement.text, str):
                flow_key_raw += subElement.text

        flow_key_raw += str(time.clock())
        flow_key = hashlib.sha224(flow_key_raw.encode('utf8')).hexdigest()

        if flowDict.get(flow_key) is not None:
            raise Exception("Lol collision : " + flow_key + " " + flow_key_raw)


        flowDict[flow_key] = item_dict

    return flowDict


def parse_folder(path):
    list_file = os.listdir(path)

    folder_dict = {}

    for file in list_file:
        file_dict = parse_file(path+file)
        folder_dict = {**file_dict, **file_dict}

    return file_dict


def index_dict(dict):
    for element in dict:
        index_entry(element, dict.get(element))


def index_entry(idx, data):
    response = requests.get('http://localhost:9200')
    if response.status_code != 200:
        print("C'est de la merde")
    else:
        es.index(index='iscx', doc_type='component', id=idx, body=json.dumps(data))
        print(idx)





if __name__ == "__main__":
    dict = parse_folder("data/")
    index_dict(dict)

