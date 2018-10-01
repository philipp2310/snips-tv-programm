#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# abstraction of coding by https://github.com/MrJohnZoidberg/Snips-Einkaufsliste

import random
import io
import pickle
# A class for universal storage of data
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

    def add_item(self, item_list):
        duplicates = []
        added_items = []
        # filter duplicate items, but keep them for a return message
        # store new items in member list for saving
        for item in item_list:
            if item.value in self.storeList:
                duplicates.append(item.value)
            else:
                added_items.append(item.value)
                self.storeList.append(item.value)
        # Start response creation
        response = ""
        # X, Y und Z wurden hinzugefügt....
        if added_items:
            items_str = "".join(item + ", " for item in added_items[:-1])
            if len(added_items) >= 2:
                items_str += "und {} ".format(added_items[-1])
                word_pl_sg = "wurden"
            else:
                items_str += "{} ".format(added_items[-1])
                word_pl_sg = "wurde"
            first_str = items_str + random.choice(["{} hinzugefügt".format(word_pl_sg),
                                                   "{} auf die {listName}Liste gesetzt".format(word_pl_sg, listName=self.callName),
                                                   "{} auf die {listName}Liste geschrieben".format(word_pl_sg, listName=self.callName)])
            if not duplicates:
                first_str += "."
            else:
                first_str += ", aber "
            response += first_str
        #, aber A, B und C waren bereits auf der Liste vorhanden
        if duplicates:
            items_str = "".join(item + ", " for item in duplicates[:-1])
            if len(duplicates) >= 2:
                items_str += "und {} ".format(duplicates[-1])
                word_pl_sg = "waren"
            else:
                items_str += "{} ".format(duplicates[-1])
                word_pl_sg = "war"
            second_str = items_str + random.choice(["{} schon auf der {listName}Liste.".format(word_pl_sg, listName=self.callName),
                                                    "{} auf der {listName}Liste schon vorhanden.".format(word_pl_sg, listName=self.callName),
                                                    "{} bereits auf der {listName}Liste vorhanden.".format(word_pl_sg, listName=self.callName)])
            response += second_str
        
        #save modified list and return output
        self.save_storeList()
        return response

    def remove_item(self, item_list):
        notlist_items = []
        removed_items = []
        for item in item_list:
            if item.value in self.storeList:
                removed_items.append(item.value)
                self.storeList.remove(item.value)
            else:
                notlist_items.append(item.value)
        response = ""
        if removed_items:
            items_str = "".join(item + ", " for item in removed_items[:-1])
            if len(removed_items) >= 2:
                items_str += "und {} ".format(removed_items[-1])
                word_pl_sg = "wurden"
            else:
                items_str += "{} ".format(removed_items[-1])
                word_pl_sg = "wurde"
            first_str = items_str + random.choice(["{} entfernt".format(word_pl_sg),
                                                   "{} von der {listName}Liste entfernt".format(word_pl_sg, listName=self.callName),
                                                   "{} von der {listName}Liste gelöscht".format(word_pl_sg, listName=self.callName)])
            if not notlist_items:
                first_str += "."
            else:
                first_str += ", aber "
            response += first_str
        if notlist_items:
            items_str = "".join(item + ", " for item in notlist_items[:-1])
            if len(notlist_items) >= 2:
                items_str += "und {} ".format(notlist_items[-1])
                word_pl_sg = "waren"
            else:
                items_str += "{} ".format(notlist_items[-1])
                word_pl_sg = "war"
            second_str = items_str + random.choice(["{} nicht auf der {listName}Liste.".format(word_pl_sg, listName=self.callName),
                                                    "{} noch nicht auf der {listName}Liste.".format(word_pl_sg, listName=self.callName),
                                                    "{} auf der {listName}Liste nicht vorhanden.".format(word_pl_sg, listName=self.callName)])
            response += second_str
        self.save_storeList()
        return response

    def is_item(self, intentMessage):
        item = intentMessage.slots.item.first().value
        if item in self.storeList:
            response = random.choice(["Ja, {item} steht auf der {listName}Liste.".format(item=str(item), listName=self.callName),
                                      "Ja, {item} befindet sich auf der {listName}Liste.".format(item=str(item), listName=self.callName),
                                      "Ja, {item} habe ich auf der {listName}Liste.".format(item=str(item), listName=self.callName),
                                      "Ja, {item} ist auf deiner {listName}Liste.".format(item=str(item), listName=self.callName)])
        else:
            response = random.choice(["Nein, {item} ist nicht auf deiner {]Liste.".format(item=str(item), listName=self.callName),
                                      "Nein, {item} ist nicht auf der {]Liste.".format(item=str(item), listName=self.callName),
                                      "Nein, {item} habe ich nicht auf der {]Liste.".format(item=str(item), listName=self.callName),
                                      "Nein, {item} fehlt noch auf deiner {]Liste.".format(item=str(item), listName=self.callName)])
        return response

    def clear_list(self, intentMessage):
        self.storeList = []
        self.save_storeList()
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
            with io.open(self.list_path, 'rb') as f:
                itemlist = pickle.load(f)
            return itemlist
        except EOFError:
            return []

    def save_storeList(self):
        with io.open(self.list_path, "wb") as f:
            pickle.dump(self.storeList, f)
