#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import io
import sys
# 
class webView:
    def __init__(self, listName, callName):
        self.list_path = listName
        self.callName  = callName
        self.storeList = self.read_storeList()
        # set encoding for umlauts...
        reload(sys)
        sys.setdefaultencoding('utf-8')

        return response

    def read_file(self):
        try:
            file = io.open(self.list_path, 'rb')
        except EOFError:
            return []
