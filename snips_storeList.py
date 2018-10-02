#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import random
import io
import pickle
import sys
# A class for universal storage of data with randomized response messages
# a file with listName has to be created manually and the corresponding rights have to be added to setup.sh
#eg: (.fav)
#if [ ! -f ./.favs ]; then
#    touch .favs
#    sudo chown _snips-skills .favs
#fi
#callName will always be put in front of "Liste"
# - Einkaufs{Liste}
# - Favouriten{Liste}
# - Zutaten{Liste}
# - Städte{Liste}

class StoreList:
    def __init__(self, listName, callName):
        self.list_path = listName
        self.callName  = callName
        self.storeList = self.read_storeList()
        # set encoding for umlauts...
        reload(sys)
        sys.setdefaultencoding('utf-8')

# add an item to the list and store the list back to hdd
# every item must only occure once
    def add_item(self, item_list):
        duplicates = []
        added = []
        str_temp = ""
        response = ""
        # filter duplicate items, but keep them for a return message
        # store new items in member list for saving
        for item in item_list:
            if item.value in self.storeList:
                duplicates.append(item.value)
            else:
                added.append(item.value)
                self.storeList.append(item.value)
        # Start response creation
        # X, Y und Z wurden hinzugef�gt....
        if added:
            # concatenate all but the last separated by ", "
            if len(added) > 1:
                str_temp = "{first} und {last} wurden".format(first=", ".join(added[:-1]), last=added[-1])
            else:
                str_temp = "{} wurde".format(added[0])
            response = str_temp + random.choice([" hinzugefügt",
                                                 " auf die {listName}Liste gesetzt".format(listName=self.callName),
                                                 " auf die {listName}Liste geschrieben".format(listName=self.callName)])
            response += ", aber " if duplicates else "."
                
        #, aber A, B und C waren bereits auf der Liste vorhanden
        if duplicates:
            if len(duplicates) > 1:
                str_temp = "{first} und {last} waren ".format(first=", ".join(duplicates[:-1]), last=duplicates[-1])
            else:
                str_temp = "{} war ".format(duplicates[0])
            response += str_temp + random.choice(["schon auf der {listName}Liste.".format(listName=self.callName),
                                                  "auf der {listName}Liste schon vorhanden.".format(listName=self.callName),
                                                  "bereits auf der {listName}Liste vorhanden.".format(listName=self.callName)])
        
        #save modified list and return output
        self.write_storeList()
        return response
    
# remove an item from the list
# prepare message for output
    def remove_item(self, item_list):
        notfound = []
        removed = []
        str_temp = ""
        response = ""
        # sort items between notfound and removed
        for item in item_list:
            if item.value in self.storeList:
                removed.append(item.value)
                self.storeList.remove(item.value)
            else:
                notfound.append(item.value)
        
        # build response for removed items
        if removed:
            if len(removed) >= 2:
                str_temp = "{first} und {last} wurden ".format(first=", ".join(removed[:-1]), last=removed[-1])
            else:
                str_temp = "{} wurde ".format(removed[0])
            response = str_temp + random.choice(["{} entfernt".format(word_pl_sg),
                                                  "{} von der {listName}Liste entfernt".format(word_pl_sg, listName=self.callName),
                                                  "{} von der {listName}Liste gelöscht".format(word_pl_sg, listName=self.callName)])

            response += ", aber " if notfound else "."
        
        # build response for not removed items
        if notfound:
            str_temp = "".join(item + ", " for item in notfound[:-1])
            if len(notfound) >= 2:
                str_temp = "{first} und {last} waren ".format(first=", ".join(notfound[:-1]), last=notfound[-1])
            else:
                str_temp = "{} war ".format(notfound[0])
            response += str_temp + random.choice(["nicht auf der {listName}Liste.".format(listName=self.callName),
                                                  "noch nicht auf der {listName}Liste.".format(listName=self.callName),
                                                  "auf der {listName}Liste nicht vorhanden.".format(listName=self.callName)])
            
        self.write_storeList()
        return response

# Check if an item is on the list(for enduser)
    def contains(self, item):
        if item in self.storeList:
            response = random.choice(["Ja, {item} steht auf der {listName}Liste.".format(item=str(item), listName=self.callName),
                                      "Ja, {item} befindet sich auf der {listName}Liste.".format(item=str(item), listName=self.callName),
                                      "Ja, {item} habe ich auf der {listName}Liste.".format(item=str(item), listName=self.callName),
                                      "Ja, {item} ist auf deiner {listName}Liste.".format(item=str(item), listName=self.callName)])
        else:
            response = random.choice(["Nein, {item} ist nicht auf deiner {listName}Liste.".format(item=str(item), listName=self.callName),
                                      "Nein, {item} ist nicht auf der {listName}Liste.".format(item=str(item), listName=self.callName),
                                      "Nein, {item} habe ich nicht auf der {listName}Liste.".format(item=str(item), listName=self.callName),
                                      "Nein, {item} fehlt noch auf deiner {listName}Liste.".format(item=str(item), listName=self.callName)])
        return response

    def clear_list(self):
        self.storeList = []
        self.write_storeList()
        return random.choice(["Die {listName}Liste wurde gelöscht.".fromat(listName=self.callName),
                              "Deine {listName}Liste wurde gelöscht.".fromat(listName=self.callName),
                              "Die {listName}Liste wurde geleert.".fromat(listName=self.callName),
                              "Alle Einträge wurden von der {listName}Liste gelöscht.".fromat(listName=self.callName)])
  
    def show(self):
        if len(self.storeList) > 1:
            response = random.choice(["Deine {listName}Liste enthält {items} und {last}.".format(listName=self.callName, items=", ".join(self.storeList[:-1]), last=self.storeList[-1]),
                                      "Auf der {listName}Liste steht {items} und {last}.".format(listName=self.callName, items=", ".join(self.storeList[:-1]), last=self.storeList[-1]),
                                      "Du hast {items} sowie {last} auf der {listName}Liste.".format(listName=self.callName, items=", ".join(self.storeList[:-1]), last=self.storeList[-1]),
                                      "Die {listName}Liste enthält {items} und {last}.".format(listName=self.callName, items=", ".join(self.storeList[:-1]), last=self.storeList[-1])])
        elif len(self.storeList) == 1:
            response = random.choice(["Deine {listName}Liste enthält nur {item}.".format(listName=self.callName, item=self.storeList[0]),
                                      "{item}. Mehr steht nicht auf der {listName}Liste.".format(listName=self.callName, item=self.storeList[0]),
                                      "Die {listName}Liste besteht nur aus {item}.".format(listName=self.callName, item=self.storeList[0]),
                                      "Die {listName}Liste enthält nur {item}.".format(listName=self.callName, item=self.storeList[0])])
        else:
            response = random.choice(["Deine {listName}Liste ist leer.".format(listName=self.callName),
                                      "Die {listName}Liste enthält keine Einträge.".format(listName=self.callName),
                                      "Die {listName}Liste ist leer.".format(listName=self.callName),
                                      "Die {listName}Liste nicht gefüllt.".format(listName=self.callName)])
        return response

    def read_storeList(self):
        try:
            file = io.open(self.list_path, 'rb')
            itemlist = pickle.load(file)
            return itemlist
        except EOFError:
            return []

    def write_storeList(self):
        file = io.open(self.list_path, "wb")
        pickle.dump(self.storeList, file)
