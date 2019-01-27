#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import io
import sys
import paho.mqtt.publish as publish

# webView loads a html file and creates a single output line that can be transfered via MQTT
class webView:
    def __init__(self, htmlFile, appName, siteID='default'):
        self.appName = appName
        self.htmlFile = htmlFile
        self.html = ""
        self.topic = "wilma/"+siteID+"/"+appName
        self.read_file()

    def read_file(self):
        try:
            with io.open(self.htmlFile, 'r') as myfile:
                self.html = myfile.read().replace('\n', '')
        except EOFError:
            return []

# <style type="text/css">
#//CSS goes here
#</style>
#<script type="text/javascript">
#//Javascript goes here
#</script>
    def insert_includes(self):
        self.html = self.html
        
    def insert_data(self, field, data):
        self.html = self.html.replace('{{'+field+'}}',data,1)
        
    def send_to_display(self):
        print(self.html)
        publish.single(self.topic, self.html, hostname="localhost", port=1883)
        
