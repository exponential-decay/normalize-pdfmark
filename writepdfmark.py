#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

'''[ /Title (Document title)
  /Author (Author name)
  /Subject (Subject description)
  /Keywords (comma, separated, keywords)
  /ModDate (D:20061204092842)
  /CreationDate (D:20061204092842)
  /Creator (application name or creator note)
  /Producer (PDF producer name or note)
  /DOCINFO pdfmark'''

#functions related to writing a PDF mark file
class WritePDFMark:

   filename = 'pdfmark'

   new_prefix = ''
   old_prefix = ''

   TITLE = "/Title"
   AUTHOR = "/Author"
   SUBJECT = "/Subject"
   KEYWORDS = "/Keywords"
   MODDATE = "/ModDate"
   CREATIONDATE = "/CreationDate" 
   CREATOR = "/Creator"
   PRODUCER = "/Producer"
   
   DOCINFO = "/DOCINFO pdfmark"

   def __init__(self, title=False, author=False, subject=False, keywords=False, moddate=False, creationdate=False, creator=False, producer=False):
      self.custom = False #until set at a later date
      if author != False or subject != False or keywords != False \
         or moddate != False or creationdate or creator != False \
            or producer != False:         
         self.writemark = True   
         self.title = self.__tostring__(title)
         self.author = self.__tostring__(author)
         self.subject = self.__tostring__(subject)
         self.keywords = self.__tostring__(keywords)
         self.moddate = self.__tostring__(moddate)
         self.creationdate = self.__tostring__(creationdate)
         self.creator = self.__tostring__(creator)
         self.producer = self.__tostring__(producer)      
      else:
         self.writemark = False

   def __tostring__(self, val):
      if val != False:
         return str(val)
      else:
         return val
      
   def add_custom(self, custom):
      if isinstance(custom, dict) is False:
         return False
      else:
         self.custom = True
         self.customdict = custom

   def __custom_to_mark__(self):
      customlist = []
      for cm in self.customdict.keys():
         customlist.append("/" + cm + "(" + self.customdict[cm] + ")")
      return customlist

   def write_mark(self):
      if self.writemark is True:
         with open(self.__getpath__(), 'wb') as f:
            #beginning of pdfmark
            f.write('[ ')
            if self.title != False: 
               f.write(self.TITLE + "(" + self.title + ")" + "\n")
            if self.author != False:
               f.write(self.AUTHOR + "(" + self.author + ")" + "\n")
            if self.subject != False:
               f.write(self.SUBJECT + "(" + self.subject + ")" + "\n") 
            if self.keywords != False:
               f.write(self.KEYWORDS + "(" + self.keywords + ")" + "\n") 
            if self.moddate != False:
               f.write(self.MODDATE + "(" + self.moddate + ")" + "\n") 
            if self.creationdate != False:
               f.write(self.CREATIONDATE + "(" + self.creationdate + ")" + "\n") 
            if self.creator != False:
               f.write(self.CREATOR + "(" + self.creator + ")" + "\n")
            if self.producer != False:
               f.write(self.PRODUCER + "(" + self.producer + ")" + "\n")
            
            #add custome keys and values if True
            if self.custom is True:
               for cl in self.__custom_to_mark__():
                  f.write(cl + "\n")
               
            #Always write (end of pdfmark): 
            f.write(self.DOCINFO + "\n")   
      return

   def __getpath__(self):
      return os.getcwd() + "\\" + self.filename
      
   def __delpath__(self):
      return os.remove(self.__getpath__())
      
def main():

   a = WritePDFMark(False, False, False, False, False, False, "ABC", False)
   a.add_custom({'Provenance': 'This file used to be.', 'Comment': 'Processed by the tool [abc]'})
   a.write_mark()
   print a.__getpath__()
   #print a.__delpath__()

if __name__ == "__main__":      
   main()