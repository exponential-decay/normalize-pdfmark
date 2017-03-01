#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase, TestLoader, TextTestRunner
import fixpdfmark as fixmx

#Examples

#FullPDFMark:

'''[ /Title (Document title)
  /Author (Author name)
  /Subject (Subject description)
  /Keywords (comma, separated, keywords)
  /ModDate (D:20061204092842)
  /CreationDate (D:20061204092842)
  /Creator (application name or creator note)
  /Producer (PDF producer name or note)
  /DOCINFO pdfmark'''

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

#recommended date from Adobe
#(D:YYYYMMDDHHmmSSOHH'mm') 

class PDFDateTests(TestCase):

   pd = fixmx.FixPDFMark()

   baddates = {'Tue Jun 15 12:03:57 1999': "19990615120357", 'Thu Sep 17 14:19:15 1998': "19980917141915", \
      'Mon Nov 02 15:08:13 1998': "19981102150813",'Fri Sep 18 13:56:59 1998': "19980918135659"}

   betterdates = {"20011113154838\\000": "20011113154838+00'00", "20120928200040+12'00'": "20120928200040+12'00", \
                     "20170221052217+13'00'": "20170221052217+13'00", "20161111151406+13'00'": "20161111151406+13'00", \
                     "20080513135759+12'00'": "20080513135759+12'00", "20120928200040+12'00'": "20120928200040+12'00", \
                     "20071206114242+13'00'": "20071206114242+13'00"}

   gooddates = {"20011114110636": "20011114110636", "20011114110636+01'00": "20011114110636+01'00"}

   good_tz = {"+00'00": "+00'00", "+09'00": "+09'00"}
   bad_tz = {"+0000": "+00'00", "+0100": "+01'00"}

   def test_bad_dates(self):
      print
      for d in self.baddates.keys():
         val = self.pd.invalid_to_pdfdate(d)
         if val != None:
            self.assertEqual(val, self.baddates[d])
         else:
            print "Failed value: " + str(d)
            self.assertIsNotNone(val)
   
def main():
   suite = TestLoader().loadTestsFromTestCase(PDFDateTests)
   TextTestRunner(verbosity=2).run(suite)
   
if __name__ == "__main__":
   main()
