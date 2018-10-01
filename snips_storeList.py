# -*- coding: utf-8 -*-
import pickle
import random
import io
import os

class StoreList:
    def __init__(self, listName, callName):
        self.list_path = listName
        self.callName = callName
        try:
            with io.open(self.list_path, 'rb') as f:
                itemlist = pickle.load(f)
        except EOFError as e:  # if no list in file
            itemlist = []
        except IOError as e:
            io.open(self.list_path, 'a').close()  # Create file, if not available
        self.storeList = self.read_storeList()

    def add_item(self, item_list):
        dublicate_items = []
        added_items = []
        for item in item_list:
            if item.value in self.storeList:
                dublicate_items.append(item.value)
            else:
                added_items.append(item.value)
                self.storeList.append(item.value)
        response = ""
        if added_items:
            items_str = "".join(item + ", " for item in added_items[:-1])
            if len(added_items) >= 2:
                items_str += "und {} ".format(added_items[-1])
                word_pl_sg = "wurden"
            else:
                items_str += "{} ".format(added_items[-1])
                word_pl_sg = "wurde"
            first_str = items_str + random.choice(["{} hinzugefügt".format(word_pl_sg),
                                                   "{} auf die {listName}Liste geschrieben".format(word_pl_sg, listName=self.callName)])
            if not dublicate_items:
                first_str += "."
            else:
                first_str += ", aber "
            response += first_str
        if dublicate_items:
            items_str = "".join(item + ", " for item in dublicate_items[:-1])
            if len(dublicate_items) >= 2:
                items_str += "und {} ".format(dublicate_items[-1])
                word_pl_sg = "sind"
            else:
                items_str += "{} ".format(dublicate_items[-1])
                word_pl_sg = "ist"
            second_str = items_str + random.choice(["{} schon auf der {listName}Liste.".format(word_pl_sg, listName=self.callName),
                                                    "{} auf der {listName}Liste schon vorhanden.".format(word_pl_sg, listName=self.callName),
                                                    "{} bereits auf der {listName}Liste vorhanden.".format(word_pl_sg, listName=self.callName)])
            response += second_str
        self.save_storeList()
        return response

    def remove_item(self, item_list):
        item_list = intentMessage.slots.item.all()
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
                                                   "{} von der {listName}Liste entfernt".format(word_pl_sg, listName=self.callName)])
            if not notlist_items:
                first_str += "."
            else:
                first_str += ", aber "
            response += first_str
        if notlist_items:
            items_str = "".join(item + ", " for item in notlist_items[:-1])
            if len(notlist_items) >= 2:
                items_str += "und {} ".format(notlist_items[-1])
                word_pl_sg = "sind"
            else:
                items_str += "{} ".format(notlist_items[-1])
                word_pl_sg = "ist"
            second_str = items_str + random.choice(["{} nicht auf der Liste.".format(word_pl_sg),
                                                    "{} auf der {listName}Liste nicht vorhanden.".format(word_pl_sg, listName=self.callName)])
            response += second_str
        self.save_storeList()
        return response

    def is_item(self, intentMessage):
        item = intentMessage.slots.item.first().value
        if item in self.storeList:
            response = "Ja, {item} steht auf der {listName}Liste.".format(item=str(item), listName=self.callName)
        else:
            response = "Nein, {item} ist nicht auf der {]Liste.".format(item=str(item), listName=self.callName)
        return response

    def try_clear(self):
        if len(self.storeList) > 1:
            response = "Die {listName}Liste enthält noch {num} Elemente." \
                       " Bist du dir sicher?".format(listName=self.callName, num=len(self.storeList))
        elif len(self.storeList) == 1:
            response = "Die {listName}Liste enthält noch ein Element. Bist du dir sicher?".format(listName=self.callName)
        else:
            response = 1  # Error: storeList is already empty - no dialogue start
        return response

    def clear_confirmed(self, intentMessage):
        if intentMessage.slots.answer.first().value == "yes":
            self.storeList = []
            self.save_storeList()
            return "Die {listName}Liste wurde geleert.".fromat(listName=self.callName)
        else:
            return "Die {listName}Liste wurde nicht geleert.".format(listName=self.callName)

    def show(self):
        if len(self.storeList) > 1:
            storeList_str = ""
            for item in self.storeList[:-1]:
                storeList_str = storeList_str + str(item) + ", "
            response = "Die {listName}Liste enthält {items} und {last}.".format(listName=self.callName, items=storeList_str, last=self.storeList[-1])
        elif len(self.storeList) == 1:
            response = "Die {listName}Liste enthält nur {item}.".format(listName=self.callName, item=self.storeList[0])
        else:  # If storeList is empty
            response = "Die {listName}Liste ist leer.".format(listName=self.callName)
        return response

    def read_storeList(self):
        try:
            with io.open(self.list_path, 'rb') as f:
                itemlist = pickle.load(f)
            return itemlist
        except EOFError:  # if no list in file
            return []

    def save_storeList(self):
        with io.open(self.list_path, "wb") as f:
            pickle.dump(self.storeList, f)
