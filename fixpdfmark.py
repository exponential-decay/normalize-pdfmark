#!/usr/bin/python
# -*- coding: utf-8 -*-

import pdfmarkings as mx
import pdfdates as pd

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
      newmark = m.replace(' (', '(')
      newmark = newmark.replace('\r', '').replace('\n', '')
      newmark = newmark.replace(' )', ')')
      return newmark

   def fixdatemarks(self, dm):
      dm = self.normalizemark(dm)
      if mx.creationdate in dm:
         d = self.__stripall__(mx.creationdate, dm)
         return mx.creationdate + " (D:" + self.__fixdate__(d) + ")"
      elif mx.modmark in dm:
         d = self.__stripall__(mx.modmark, dm)
         return mx.modmark + " (D:" + self.__fixdate__(d) + ")"

   def __stripall__(self, str, d):
      return d.replace(str, '').replace('(', '').replace(')','').replace('D:','').strip()

   def __fixdate__(self, d):
      datefix = pd.PDFDates()   
      d = datefix.invalid_to_pdfdate(d)
      return d