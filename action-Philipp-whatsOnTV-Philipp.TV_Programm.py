#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import urllib
import xmltodict

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    """ Write the body of the function that will be executed once the intent is recognized. 
    In your scope, you have the following objects : 
    - intentMessage : an object that represents the recognized intent
    - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol. 
    - conf : a dictionary that holds the skills parameters you defined. 
      To access global parameters use conf['global']['parameterName']. For end-user parameters use conf['secret']['parameterName'] 
     
    Refer to the documentation for further details. 
    """ 
    if len(intentMessage.slots.channel) > 0:
        channel = "| " + intentMessage.slots.channel.first().value + " |"
    if len(intentMessage.slots.timeslot) > 0:
        if intentMessage.slots.timeslot.first().value == "later":
            when = "2015" # todo: always later than current time!
        else:
            when = intentMessage.slots.timeslot.first().value

    if when == "now":
        result_sentence = "Jetzt auf "
        file = urllib.urlopen('http://www.tvspielfilm.de/tv-programm/rss/jetzt.xml')
    
    elif when == "2015":
        result_sentence = "Heute Abend auf "
        file = urllib.urlopen('http://www.tvspielfilm.de/tv-programm/rss/heute2015.xml')
        
    elif when == "2200":
        result_sentence = "Heute Nacht auf "
        file = urllib.urlopen('http://www.tvspielfilm.de/tv-programm/rss/heute2200.xml')
        
    else:
        result_sentence = "Jetzt auf "
        file = urllib.urlopen('http://www.tvspielfilm.de/tv-programm/rss/jetzt.xml')

    data = file.read()
    file.close()
    data = xmltodict.parse(data)
    
    count = 0
    for item in data['rss']['channel']['item']:
        if channel in item['title']:
            result_sentence = result_sentence + item['title'][8:]
            count = count + 1
    
    if count > 0:
        result_sentence = result_sentence.replace(" |",":")
        result_sentence = result_sentence.replace("ServusTV Deutschland","Servus TV")
        result_sentence = result_sentence.replace("SAT.1","Sat 1")
        result_sentence = result_sentence.replace("DMAX","De Max")
    else:
        result_sentence = "Leider konnte ich keine Sendung finden."
        
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)
    


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("Philipp:whatsOnTV", subscribe_intent_callback) \
         .start()
