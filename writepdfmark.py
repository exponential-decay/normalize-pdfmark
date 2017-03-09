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

#helper class to persist state
class PDFMark:
   writeme = False
   def __init__(self):
      self.title = False
      self.author = False
      self.subject = False
      self.keywords = False
      self.moddate = False
      self.creationdate = False 
      self.creator = False
      self.producer = False
      self.custom = False     #needs to be a dict object
      
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

   def __init__(self):
      self.writemark = False   
      self.title = False
      self.author = False
      self.subject = False
      self.keywords = False
      self.moddate = False
      self.creationdate = False
      self.creator = False
      self.producer = False

   def __init_from_string__(self, title=False, author=False, subject=False, keywords=False, moddate=False, creationdate=False, creator=False, producer=False):
      self.custom = False     #until set at a later date
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
         return self
      else:
         self.writemark = False
         return self

   def __init_from_object__(self, pdfmark):
      self.custom = False     #until set at a later date
      if isinstance(pdfmark, PDFMark) is True:
         if pdfmark.writeme != False:
            self.writemark = True   
         if pdfmark.title != False: 
            self.title = pdfmark.title
         if pdfmark.author != False:
            self.author = pdfmark.author
         if pdfmark.subject != False:
            self.subject = pdfmark.subject
         if pdfmark.keywords != False:
            self.keywords = pdfmark.keywords
         if pdfmark.moddate != False:
            self.moddate = pdfmark.moddate
         if pdfmark.creationdate != False:
            self.creationdate = pdfmark.creationdate
         if pdfmark.creator != False:
            self.creator = pdfmark.creator
         if pdfmark.producer != False:
            self.producer = pdfmark.producer
         if pdfmark.custom != False:
            self.add_custom(pdfmark.custom)
         return self
      else:
         self.writemark = None
         return self

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
         customlist.append("/" + self.__format_mark__(cm, self.customdict[cm]))
      return customlist

   def __format_mark__(self, key, value):
      if value.count("(") > 0 and (value.count(")") < value.count("(")):
         value = value + ")"
         self.__format_mark__(key,value)
      return key + " (" + value + ")" + "\n"

   def write_mark(self, fname=False):
      if fname != False:
         self.filename = fname
      if self.writemark is True:
         with open(self.__getpath__(), 'wb') as f:
            #beginning of pdfmark
            f.write('[ ')
            if self.title != False: 
               f.write(self.__format_mark__(self.TITLE, self.title))
            if self.author != False:
               f.write(self.__format_mark__(self.AUTHOR, self.author))
            if self.subject != False:
               f.write(self.__format_mark__(self.SUBJECT, self.subject))
            if self.keywords != False:
               f.write(self.__format_mark__(self.KEYWORDS, self.keywords))
            if self.moddate != False:
               f.write(self.__format_mark__(self.MODDATE, self.moddate))
            if self.creationdate != False:
               f.write(self.__format_mark__(self.CREATIONDATE, self.creationdate))
            if self.creator != False:
               f.write(self.__format_mark__(self.CREATOR, self.creator))
            if self.producer != False:
               f.write(self.__format_mark__(self.PRODUCER, self.producer))
            
            #add custome keys and values if True
            if self.custom is True:
               for cl in self.__custom_to_mark__():
                  f.write(cl)
               
            #Always write (end of pdfmark): 
            f.write(self.DOCINFO + "\n")   

   def write_mark_str(self):
      if self.writemark is True:
         #beginning of pdfmark
         sys.stdout.write('[ ')
         if self.title != False: 
            sys.stdout.write(self.__format_mark__(self.TITLE, self.title))
         if self.author != False:
            sys.stdout.write(self.__format_mark__(self.AUTHOR, self.author))
         if self.subject != False:
            sys.stdout.write(self.__format_mark__(self.SUBJECT, self.subject))
         if self.keywords != False:
            sys.stdout.write(self.__format_mark__(self.KEYWORDS, self.keywords))
         if self.moddate != False:
            sys.stdout.write(self.__format_mark__(self.MODDATE, self.moddate))
         if self.creationdate != False:
            sys.stdout.write(self.__format_mark__(self.CREATIONDATE, self.creationdate))
         if self.creator != False:
            sys.stdout.write(self.__format_mark__(self.CREATOR, self.creator))
         if self.producer != False:
            sys.stdout.write(self.__format_mark__(self.PRODUCER, self.producer))
         
         #add custome keys and values if True
         if self.custom is True:
            for cl in self.__custom_to_mark__():
               sys.stdout.write(cl)
            
         #Always write (end of pdfmark): 
         sys.stdout.write(self.DOCINFO + "\n")   

   def __getpath__(self):
      return os.getcwd() + os.path.sep + self.filename
      
   def __delpath__(self):
      return os.remove(self.__getpath__())
      
def main():

   pdfmark = PDFMark()
   pdfmark.title = "A title"
   pdfmark.custom = {'Provenance': 'This file used to be.', 'Comment': 'Processed by the tool [abc]'}
   b = WritePDFMark().__init_from_object__(pdfmark)
   b.write_mark_str()
   
   #write default pdf mark file
   a = WritePDFMark().__init_from_string__("Document title", "Author name", "Subject description", "comma, separated, keywords", \
                        "D:20061204092842", "D:20061204092842", "application name or creator note", "PDF producer name or note")
                        
   a.add_custom({'Provenance': 'This file used to be.', 'Comment': 'Processed by the tool [abc]'})
   a.write_mark()
   
   print "PDF mark writing complete."

if __name__ == "__main__":      
   main()
