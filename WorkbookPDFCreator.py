# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 13:37:41 2016

@author: larry.jerome
"""


from urllib2 import Request, urlopen
#from pyPdf import PdfFileWriter, PdfFileReader
#from StringIO import StringIO
import os
#import datetime
#import pymssql
#import tkFileDialog


##server login details
#server_name = 
#db_user = 
#db_pass = 
#db_name = 
#
#
#def getRecords(query):
#    #connect to server with details above
#    conn = pymssql.connect(server_name, db_user, db_pass, db_name)
#    cur = conn.cursor()
#    cur.execute(query)
#    return cur
        



class PublishedWorkbook(object):
    '''
    descriptive text goes here
    '''
    
    def __init__(self,url,parameterNames,csv):
        '''
        workbook (str): name of the workbook you are accessing
        url (str): the full url up to the view name (do not include '#1')
        numberOfParamers (int): the number of URL parameters that will be used
        parameterNames (list): 
        csv (str): file path to csv file. Must be a csv file
        '''
        self.url = url
        self.parameterNames = parameterNames
        self.csv = csv
    
    def getURL(self):
        return self.url
        
    def getParameters(self):
        return self.parameterNames
        
    def getCSV(self):
        return self.csv
                
    def transformParameters(self):
        transformedParameters = []
        for parameter in self.getParameters():
            parameter=parameter.replace(" ","%20")
            transformedParameters.append(parameter)
        return transformedParameters
                   

    def records(self): #sometimes double quotes show up around strings and that is messing up the file naming
        '''
        returns a list of lists that are the records
        '''
        infile = open(self.getCSV())
        recordsList = []
        for line in infile:
            stripLine = line.rstrip('\n')
            splitStripLine =  stripLine.split(',')
            recordsList.append(splitStripLine)
        return recordsList

    def urlList(self):
        listOfURL = []
        parameterList=self.transformParameters()
        parameters=self.getParameters()
        records=self.records()
        for record in records[1:]:
            urlWithParameters = self.getURL()+'.pdf?'
            for parameter in parameters:
                if self.getParameters().index(parameter)==0:
                    urlWithParameters+=parameterList[parameters.index(parameter)]+'='+record[records[0].index(parameter)]
                else:
                    urlWithParameters+='&'+parameterList[parameters.index(parameter)]+'='+record[records[0].index(parameter)]
            listOfURL.append(urlWithParameters)
        return listOfURL
            
    def fileName(self,headers):
        '''
        Enter list of headers from the csv that you want to use to name the files
        List should be in the order in which you want the file to be named
        '''
        fileNameList = []
        recordsList = self.records()
        for row in recordsList:
            curFileName = ""
            for i in headers:
                field=self.records()[0].index(i)
                curFileName+=row[field]
            curFileName=curFileName.replace('"','')
            fileNameList.append(curFileName)
        return fileNameList[1:]
            
    def createPDF(self,filePath,headers):
        '''
        Enter the entire file path including the terminal folder name
        urls must be a list
        '''
        fileNameList=self.fileName(headers)
        urls = self.urlList()        
        for url in urls[1:]:
            print url
            response = urlopen(url)
            fileName=fileNameList[self.urlList().index(url)]+'.pdf'
            file = open(fileName, 'wb')
            file.write(response.read())
            file.close()
            os.chdir(filepath)


url = 'https://tableau.server.com'
parameters = ['Parameter1','Paramter2','Parameter3',...]
csv = r'C:\Users\...\filename.csv'
filepath = r'C:\Users\...'
headers = ['header1','header2','header3',..]

pdfSet = PublishedWorkbook(url,parameters,csv)
pdfSet.createPDF(filepath,headers)
