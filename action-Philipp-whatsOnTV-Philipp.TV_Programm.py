#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import urllib
import xmltodict
from snips_storeList import StoreList
import datetime

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
    if intentMessage.intent.intent_name == "Philipp:whatsOnTV":
        hermes.publish_end_session(intentMessage.session_id, whatsOnTV(hermes,intentMessage,conf))
    elif intentMessage.intent.intent_name == "Philipp:addFavouriteChannel":
        addFav(hermes,intentMessage,conf)
    elif intentMessage.intent.intent_name == "Philipp:deleteFavouriteChannel":
        delFav(hermes,intentMessage,conf)

def addFav(hermes, intentMessage, conf):
    if len(intentMessage.slots.channel) > 0:
        result_sentence = storage.add_item(intentMessage.slots.channel.all())
        hermes.publish_end_session(intentMessage.session_id, result_sentence)
    
def delFav(hermes, intentMessage, conf):
    if len(intentMessage.slots.channel) > 0:
        result_sentence = storage.remove_item(intentMessage.slots.channel.all())
        hermes.publish_end_session(intentMessage.session_id, result_sentence)

def whatsOnTV(hermes, intentMessage, conf):
    noChan = True
    if len(intentMessage.slots.channel) > 0:
        noChan = False
    if len(intentMessage.slots.timeslot) > 0:
        if intentMessage.slots.timeslot.first().value == "later":
            if datetime.datetime.now().strftime('%H%M%S') > "2015":
                when = "2200"
            elif datetime.datetime.now().strftime('%H%M%S') > "2200":
                when = "now"
                result_sentence = "Keine späteren Informationen verfügbar. "
            else:
                when = "2015"
        else:
            when = intentMessage.slots.timeslot.first().value
    else:
        when = "now"

    if when == "now":
        result_sentence += "Jetzt auf "
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
    if noChan:
        favs = storage.read_storeList()
        if len(favs) == 0:
            result_sentence = "Keine Favouriten definiert."
    for item in data['rss']['channel']['item']:
        if noChan:
            if any("| " + chan +" |" in item['title'] for chan in favs):
                result_sentence = result_sentence + item['title'][8:] + " . "
                count = count + 1   
        else:
            if any("| " + chan.value +" |" in item['title'] for chan in intentMessage.slots.channel.all()):
                result_sentence = result_sentence + item['title'][8:] + " . "
                count = count + 1
    
    if count > 0:
        result_sentence = result_sentence.replace(" |",":")
        result_sentence = result_sentence.replace("ServusTV Deutschland","Servus TV")
        result_sentence = result_sentence.replace("SAT.1","Sat 1")
        result_sentence = result_sentence.replace("DMAX","De Max")
    else:
        result_sentence = "Leider konnte ich keine Sendung finden."
    
    return result_sentence


if __name__ == "__main__":
    storage = StoreList(".favs","Favoriten")
    with Hermes("localhost:1883") as h:
        h.subscribe_intents(subscribe_intent_callback).start()
