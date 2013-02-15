'''
Created on Jan 25, 2013

@author: AKIN
'''

import glob
import os
import json
import logging

import difflib

from restclient.restful_lib import Connection

'''
----------------------------
            Steps
---------------------------- 
NOTE: In order to test ROS, we need to first 
make sure that we have the right data in our 
database. For this we need to clean the DB 
and populate the tables with the correct set 
of data.

1. Read request input from file
2. Read expected response from file
3. Send request to the server
4. Check the response   
'''


'''
    In this method we will read the list of 
    json files from the folder and return the 
    result in a list.
'''
def read_files(folderUrl):    
    if folderUrl.endswith('/'):
        pass
    else:
        folderUrl = folderUrl + '/'
        
    return glob.glob(folderUrl+"/*.json")

def readFileIntoString(fileUrl):
    strResult = ""
    with open(fileUrl) as infile:
        for line in infile:
            strResult += line
    
    return strResult

def readJsonFile(fileUrl):
    global logger
    
    fileContent = ''
    
    # read the file content
    if(os.path.isfile(fileUrl)):
        # this is a file, read
        fileContent = json.load(open(fileUrl))
        return fileContent
    else:
        # file does not exist, failed
        logger.debug('File does not exist, failed: ' + fileUrl)  
        return None 

if __name__ == '__main__':
#def run_rest_tester():
    
    logger = logging.getLogger('Rest Server Tester')
    hdlr = logging.FileHandler('test.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.DEBUG)
    
    requestFolderUrl = "requestFiles"
    responseFolderUrl = "responseFiles"
    #step 1
    listrequestFiles = read_files(requestFolderUrl)
    
    # step 2
    listresponseFiles = read_files(responseFolderUrl)
    
    logger.debug("Request Files: " + str(listrequestFiles))
    logger.debug("Response Files: " + str(listresponseFiles))
    
    # step 3: Send request to the server
    
    #base_url = "http://ec2-54-245-3-57.us-west-2.compute.amazonaws.com/api/types/"
    base_url = "http://localhost:8080/irdeto-jbpm-app/ws/rs/"

    conn = Connection(base_url)
    
    counterFile = 0
    
    for fileUrl in listrequestFiles:
        jsonRequest = readJsonFile(fileUrl)
        
        if jsonRequest == None:
            # TODO : this means we could not happen
            pass
        
        strRequestType = jsonRequest['requestType']
        strCommand = jsonRequest['command'] 
        dictResponseBody = jsonRequest['body']
        
        response = ""
    
        if strRequestType == "GET":
            #tmpRealResponse = conn.request_get(strCommand, headers={'Accept':'application/vnd.mediamanager.jbpm+json', 'Content-Type':'application/json'})
            tmpRealResponse = conn.request_get(strCommand)
            jsonRealResponse = {}
            for key in tmpRealResponse.keys():
                jsonRealResponse[key.encode('ascii','ignore')] = str(tmpRealResponse[key.encode('ascii','ignore')]).encode('ascii','ignore')
            logger.debug(str(jsonRealResponse['body']))
            pass
        elif strRequestType == "POST":
            pass
        elif strRequestType == "PUT":
            pass
        elif strRequestType == "DELETE":
            conn.request_delete('/items/11232344')
            pass
        
        # step 4
        strExpectedResponse = readFileIntoString(listresponseFiles[counterFile])
        logger.debug(strExpectedResponse)
        #jsonRealResponse = json.load(response)
        
        if strExpectedResponse == str(jsonRealResponse['body']):
            logger.debug("PASSED")
        else:
            logger.debug ("FAILED")
        
        # TODO : Maybe later we can do a better way for checking this
                    
        counterFile += 1        
        pass 

    # Step 4: Check the response
    print("Test Finished")
    pass 