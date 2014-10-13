from __future__ import print_function
import logging
import urllib
import json
from xml.etree.ElementTree import parse
from xml.etree import ElementTree
import MySQLdb


#########################################################
# Data aggregation
#########################################################

class DataAggregator(object):
    ''' Data Aggregator
        Input : API objects list and output objects
        Run will call APIs and give the result to the output object
     '''
    def __init__(self, api_list, data_output):
        self.api_list = api_list
        self.data_output = data_output

    def run(self):
        logging.info('[START run] \n')
        data = self.prepare_output()
        logging.info(' - data extracted \n')
        logging.debug(' - extracted data - %s\n', data)
        self.data_output.output(data)
        logging.info('[END run] \n')

    def prepare_output(self):
        ''' Aux function that receive a list of APIS, run each and returns a string with all the output'''
        result=""
        for api in self.api_list:
            data = api.getData()
            name = api.getName()
            result += '<p class="fa2s_api">\n'
            result += '<div class="api_title">'+name+'</div>\n'
            for item in data:
                result +='<div class="api_item"><a href="'+item[1]+'">' +item[0]+ '</a></div>\n'
            result += '</p>\n'
        return result


#########################################################
# API classes
#########################################################

class DataAPI(object):
    ''' Data API base class
        All child classes must have an api_name and url vars.
    '''

    def __init__(self):
        self.url = ""
        self.api_name=""

    def getRawData(self):
        ''' Aux function - Gets data from the web'''
        data_url = urllib.urlopen(self.url)
        data_raw = data_url.read()
        return data_raw

    def getName(self):
        ''' returns the class name'''
        return self.api_name

    def loadJason(self, data_raw):
        ''' Aux function - Load data into Json object'''
        data = json.loads(data_raw)
        logging.debug(' -json data %s - %s\n', self.getName(), data)
        return data

    def loadXML(self, url):
        ''' Aux function - Load data into XML object'''
        tree = parse(urllib.urlopen(url))
        root = tree.getroot()
        logging.debug(' -XML data %s - %s\n', self.getName(), ElementTree.tostring(root, 'utf-8'))
        return root


class APIBioMedCentral(DataAPI):
    ''' API handler class for BioMedCentral
        Input: max_items - limits the number of return results
    '''
    api_name = "BioMed Central"

    def __init__(self, max_items):
        self.max_items = max_items
        self.url = "http://www.biomedcentral.com/webapi/1.0/latest_articles.json"
        logging.info('[Created] %s\n', self.api_name)

    def getData(self):
        ''' Gets data from Json, converts to list'''
        data_raw = self.getRawData()
        data = self.loadJason(data_raw)
        if not 'articles' in data:
            return None
        # Return [(title,url), (title,url), ...]
        return [(self.clearTitle(item['title']), "http://" + item['article_host']+item['article_url']) for item in data['articles']][:self.max_items]

    def clearTitle(self, data):
        ''' Aux function to clean data in getData '''
        data = data.replace("<p>", "")
        data = data.replace("</p>", "")
        return data


class APIEuropePMC(DataAPI):
    ''' API handler for Europe PubMed Central
        Input: max_items - limits the number of return results
    '''
    api_name = "Europe PubMed Central"

    def __init__(self, max_items):
        self.max_items = max_items
        self.url = "http://europepmc.org/Funders/RSS/AllFunders.xml"
        logging.info('[Created] %s\n', self.api_name)

    def getData(self):
        ''' Gets data from XML, converts to list'''
        root = self.loadXML(self.url)
        channel_root = root.find("channel")
        data = channel_root.findall("item")[:self.max_items]
        if not data:
            return []
        for item in data:
            logging.debug(' -XML data Europe PubMed Central ITEM - %s \n', ElementTree.tostring(item, 'utf-8'))
        # Return [(title,url), (title, url)...]
        return [(item.find('title').text, item.find('link').text) for item in data][:self.max_items]

#########################################################
# Data Output
#########################################################

class DataOutput(object):
    ''' Base output class'''
    def output(self, data):
        ''' All child classes must have this function defenition
            Input: data - List with values to print. [(title, url), ...]
        '''
        pass


class OutputFile(DataOutput):
    ''' Output class to an html static file
        Input: file_name - File where to write output
    '''
    def __init__(self, file_name):
        self.file_name = file_name

    def output(self, data):
        file_handler = open(self.file_name,'w')
        print(data, file=file_handler)
        file_handler.close()


class OutputJoomla(DataOutput):
    ''' Output to a joomla article
        Input: server - server address
               user -
               password -
               db - db from joomla
               id_value - id of article where data will override content
    '''
    def __init__(self, server, user, password, db, id_value):
        self.server = server
        self.user = user
        self.password = password
        self.db = db
        self.id = id_value

    def output(self, data):
        db = MySQLdb.connect(self.server, self.user, self.password, self.db )
        cursor = db.cursor()
        sql = "UPDATE jos_content SET introtext='%s' WHERE id = '%d'" % (data,self.id)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception,e:
            print("FAIL %s" % e)
            db.rollback()
        db.close()


#########################################################
# Main
#########################################################

def main():
    msg = (
            "\nThis script should be called from another python script. A simple example:\n\n"
            "import fa2s\n"
            "import sys\n"
            "api_bio_med_central = fa2s.APIBioMedCentral(3)\n"
            "api_europe_pmc = fa2s.APIEuropePMC(3)\n"
            "output_file = fa2s.OutputFile('result.html')\n"
            "output_joomla = fa2s.OutputJoomla('server','user','password','database_name', id_article)\n"
            " # OR aggregator = fa2s.DataAggregator([api_bio_med_central,api_europe_pmc], output_file)\n"
            "aggregator = fa2s.DataAggregator([api_bio_med_central,api_europe_pmc], output_joomla)\n"
            "aggregator.run()\n"
         )
    print(msg)

# Logging
logging.basicConfig(filename='fa2s.log',level=logging.DEBUG, format='%(asctime)s %(message)s')

# Call main if not imported
if __name__ == "__main__":
    main()
