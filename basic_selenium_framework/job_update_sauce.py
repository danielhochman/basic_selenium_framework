#!/usr/bin/python

from xml.etree.ElementTree import parse
import os
import re
import sys
import urllib2
import base64
import simplejson as json

with open('config.json') as f:
    config = json.load(f)

rest_auth = base64.b64encode("%s:%s" % (config['sauce_username'], config['sauce_access_key']))
opener = urllib2.build_opener(urllib2.HTTPHandler)

result_root = parse(open('nosetests.xml', 'r')).getroot()
testcaseList = result_root.findall("testcase")

for testcase in testcaseList:
    fullclassname = testcase.attrib['classname'].replace('"','')
    testname = testcase.attrib['name'].replace('"','')
    
    sysout = testcase.find('system-out')
    if sysout is not None:
        for result in re.findall('### testinfo(.*?)###', sysout.text, re.S):
            testinfo = json.loads(result, use_decimal=True)
            
        request_url = "https://saucelabs.com/rest/v1/%s/jobs/%s" % (config['sauce_username'], testinfo['job_id'])
        
        request_data = {}
        request_data['name'] = "%s.%s" % (fullclassname, testname)
        
        if testcase.find('failure') is None and testcase.find('error') is None:
            request_data['passed'] = True
        else:
            request_data['passed'] = False
        
        request = urllib2.Request(request_url, data = json.dumps(request_data))
        request.add_header('Content-Type', 'application/json')
        request.add_header('Authorization', "Basic %s" % rest_auth)
        request.get_method = lambda: 'PUT'
        
        print "Updating Sauce Job..."
        print "Job ID: %s" % testinfo['job_id']
        print "Parameters: %s" % request_data
        
        try:
            opener.open(request)
        except urllib2.HTTPError as e:
            print "WARNING: Could not update test"
            print " %s" % e
        print

if result_root.find('.//failure') is None and result_root.find('.//error') is None:
    print "No failures found"
    sys.exit(0)
else:
    print "Failures found in test report"
    sys.exit(1)
