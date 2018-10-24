#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import io
import sys
import paho.mqtt.publish as publish

# webView loads a html file and creates a single output line that can be transfered via MQTT
class webView:
    def __init__(self, htmlFile, appName, sideID='default'):
        self.appName = appName
        self.htmlFile = htmlFile
        self.html = ""
        self.topic = "Wilma/disp/"+self.sideID+"/"+appName
        # set encoding for umlauts...
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.read_file()

    def read_file(self):
        try:
            self.html = io.open(self.htmlFile, 'rb')
        except EOFError:
            return []

# <style type="text/css">
#//CSS goes here
#</style>
#<script type="text/javascript">
#//Javascript goes here
#</script>
    def insert_includes():
        self.html = self.html
        
    def insert_data(self, field, data):
        self.html = self.html.replace('{{'+field+'}}',data,1)
        
    def send_to_display():
        publish(self.topic, self.html, hostname="localhost", port=1883)
        
