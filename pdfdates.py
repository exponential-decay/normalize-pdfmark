#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

#TODO: Check for terminator before final bracket in PDFMark date

#PDF Broken Examples... %a %b %d %H:%M:%S %Y
#Thu Mar 18 11:03:07 1999
#Thu Sep 24 14:26:20 1998
#Wed Oct 07 15:13:24 1998
#Thu Jun 10 12:13:51 1999
#Thu Jun 10 12:05:43 1999

#Example of good date with timezone
#D:20120928200040+12'00'
#D:20160615140642+12'00'

#Correct Format, http://www.adobe.com/content/dam/Adobe/en/devnet/acrobat/pdfs/pdfmark_reference.pdf
#(D:YYYYMMDDHHmmSSOHH'mm') 
#%Y%m%d

#tests
#print invalid_to_pdfdate("Thu Mar 18 11:03:07 1999")
#print invalid_to_pdfdate("19990318110307")

class PDFDates:

   ERR = "ERROR"
   PDFFORMAT = "%Y%m%d%H%M%S"
   NORMFORMAT = "%a %b %d %H:%M:%S %Y"
   
   def split_timezone(self, old_date):
      if '+' in old_date:
         new_date = old_date.split('+', 1)
         return new_date[0], '+' + new_date[1].replace("'", "")      
      elif '-' in old_date:
         new_date = old_date.split('-', 1)      
         return new_date[0], '-' + new_date[1].replace("'", "")
      elif '\\' in old_date:
         new_date = old_date.split('\\', 1)
         if len(new_date[1]) == 3:
            new_date[1] = new_date[1] + "0"      
         return new_date[0], '+' + new_date[1].replace("'", "")
      else:
         return False, ''
   
   def convert_tz(self, tz):
      if "'" not in tz:
         return tz[0:3] + "'" + tz[3:5]
      else:
         return tz
   
   #Parse whatever format we receive into a date format, and then
   #spit it out again as something we can use...
   def invalid_to_pdfdate(self, old_date):
      
      #remove excess characters if we find any...
      old_date.strip()
      
      try:
         dt = datetime.strptime(old_date, self.PDFFORMAT)
         return dt.strftime(self.PDFFORMAT)
      except ValueError:
         None
      
      try:
         dt = datetime.strptime(old_date, self.NORMFORMAT)
         return dt.strftime(self.PDFFORMAT)
      except ValueError:
         None

      try:
         new_date = self.valid_tz_to_datestr(old_date)
         return new_date
      except ValueError:
         None
         
      return None
      
   def valid_tz_to_datestr(self, old_date):
      new_date, tz = self.split_timezone(old_date)
      if new_date is not False:
         dt = datetime.strptime(new_date, self.PDFFORMAT)
         tz = self.convert_tz(tz)
         return dt.strftime(self.PDFFORMAT) + tz
      return None
      
   def valid_to_dateobj(self, old_date):
      new_date, tz = self.split_timezone(old_date)
      if new_date is not False:
         return datetime.strptime(new_date, self.PDFFORMAT), tz
      return datetime.strptime(old_date, self.NORMFORMAT), '+0000'      
      