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
        reload(sys)
        sys.setdefaultencoding('utf-8')

# add an item to the list and store the list back to hdd
# every item must only occure once
    def add_item(self, item_list):
        duplicates = []
        new_items = []
        str_temp = ""
        # filter duplicate items, but keep them for a return message
        # store new items in member list for saving
        for item in item_list:
            if item.value in self.storeList:
                duplicates.append(item.value)
            else:
                new_items.append(item.value)
                self.storeList.append(item.value)
        # Start response creation
        response = ""
        # X, Y und Z wurden hinzugef�gt....
        if new_items:
            # concatenate all but the last separated by ", "
            str_temp = "{}{},".format(str_temp, (item for item in new_items[:-1]))
            #str_temp = "".join(item + ", " for item in new_items[:-1])
            if len(new_items) >= 2:
                str_temp += "und {last} ".format(last=new_items[-1])
                word_pl_sg = "wurden"
            else:
                str_temp += "{} ".format(new_items[-1])
                word_pl_sg = "wurde"
            response = str_temp + random.choice(["{} hinzugefügt".format(word_pl_sg),
                                                   "{} auf die {listName}Liste gesetzt".format(word_pl_sg, listName=self.callName),
                                                   "{} auf die {listName}Liste geschrieben".format(word_pl_sg, listName=self.callName)])
            if not duplicates:
                response += "."
            else:
                response += ", aber "
        #, aber A, B und C waren bereits auf der Liste vorhanden
        if duplicates:
            str_temp = "".join(item + ", " for item in duplicates[:-1])
            if len(duplicates) >= 2:
                str_temp += "und {} ".format(duplicates[-1])
                word_pl_sg = "waren"
            else:
                str_temp += "{} ".format(duplicates[-1])
                word_pl_sg = "war"
            response += str_temp + random.choice(["{} schon auf der {listName}Liste.".format(word_pl_sg, listName=self.callName),
                                                    "{} auf der {listName}Liste schon vorhanden.".format(word_pl_sg, listName=self.callName),
                                                    "{} bereits auf der {listName}Liste vorhanden.".format(word_pl_sg, listName=self.callName)])
        
        #save modified list and return output
        self.write_storeList()
        return response

    def remove_item(self, item_list):
        notfound = []
        removed_items = []
        for item in item_list:
            if item.value in self.storeList:
                removed_items.append(item.value)
                self.storeList.remove(item.value)
            else:
                notfound.append(item.value)
        response = ""
        if removed_items:
            str_temp = "".join(item + ", " for item in removed_items[:-1])
            if len(removed_items) >= 2:
                str_temp += "und {} ".format(removed_items[-1])
                word_pl_sg = "wurden"
            else:
                str_temp += "{} ".format(removed_items[-1])
                word_pl_sg = "wurde"
            first_str = str_temp + random.choice(["{} entfernt".format(word_pl_sg),
                                                   "{} von der {listName}Liste entfernt".format(word_pl_sg, listName=self.callName),
                                                   "{} von der {listName}Liste gelöscht".format(word_pl_sg, listName=self.callName)])
            if not notfound:
                first_str += "."
            else:
                first_str += ", aber "
            response += first_str
        if notfound:
            str_temp = "".join(item + ", " for item in notfound[:-1])
            if len(notfound) >= 2:
                str_temp += "und {last} ".format(last=notfound[-1])
                word_pl_sg = "waren"
            else:
                str_temp += "{} ".format(notfound[-1])
                word_pl_sg = "war"
            second_str = str_temp + random.choice(["{} nicht auf der {listName}Liste.".format(word_pl_sg, listName=self.callName),
                                                    "{} noch nicht auf der {listName}Liste.".format(word_pl_sg, listName=self.callName),
                                                    "{} auf der {listName}Liste nicht vorhanden.".format(word_pl_sg, listName=self.callName)])
            response += second_str
        self.write_storeList()
        return response

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
            storeList_str = ""
            for item in self.storeList[:-1]:
                storeList_str = storeList_str + str(item) + ", "
            response = random.choice(["Deine {listName}Liste enthält {items} und {last}.".format(listName=self.callName, items=storeList_str, last=self.storeList[-1]),
                                      "Auf der {listName}Liste steht {items} und {last}.".format(listName=self.callName, items=storeList_str, last=self.storeList[-1]),
                                      "Du hast {items} sowie {last} auf der {listName}Liste.".format(listName=self.callName, items=storeList_str, last=self.storeList[-1]),
                                      "Die {listName}Liste enthält {items} und {last}.".format(listName=self.callName, items=storeList_str, last=self.storeList[-1])])
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
