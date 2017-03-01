#!/usr/bin/python
# -*- coding: utf-8 -*-

#Examples

#/CreationDate (Tue Jun 15 12:03:57 1999)
#/CreationDate (Thu Sep 17 14:19:15 1998)
#/CreationDate (Mon Nov 02 15:08:13 1998)
#/CreationDate (Fri Sep 18 13:56:59 1998)

#/CreationDate (D:20011113154838\000)
#/CreationDate (D:20120928200040+12'00')
#/CreationDate(D:20170221052217+13'00')
#/CreationDate(D:20161111151406+13'00')
#/ModDate(D:20080513135759+12'00')
#/ModDate (D:20120928200040+12'00')
#/ModDate (D:20011114110636)
#/ModDate(D:20071206114242+13'00')

class FixPDFMark:

   def normalizemark(self, m):
      mnew = m.replace(' (', '(')
      return mnew

   def convertdate(self, d1, d2):
      #test old date and convert to new date
      return

   def recordoriginaldates(self, f):
      #list: path + mod date + create date
      return

   def replaceoriginaldates(self, f):
      return
