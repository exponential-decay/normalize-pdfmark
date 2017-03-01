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
#/ModDate (D:20120928200040+12'00')
#/ModDate (D:20011114110636)
#/ModDate(D:20071206114242+13'00')

#recommended date from Adobe
#(D:YYYYMMDDHHmmSSOHH'mm') 

class FixPDFMarkTests(TestCase):

   fixme = fixmx.FixPDFMark()

   baddatemarks = {"/CreationDate (Tue Jun 15 12:03:57 1999)": "/CreationDate (D:19990615120357)", \
                     "/CreationDate (Thu Sep 17 14:19:15 1998)": "/CreationDate (D:19980917141915)", \
                     "/CreationDate(Mon Nov 02 15:08:13 1998)": "/CreationDate (D:19981102150813)", \
                     "/CreationDate(Fri Sep 18 13:56:59 1998)": "/CreationDate (D:19980918135659)",
                     "/ModDate(Fri Sep 18 13:56:59 1998)": "/ModDate (D:19980918135659)"}

   def test_bad_date_marks(self):
      print
      for d in self.baddatemarks.keys():
         val = self.fixme.fixdatemarks(d)
         if val != None:
            self.assertEqual(val, self.baddatemarks[d])
         else:
            print "Failed value: " + str(d)
            self.assertIsNotNone(val)
   
def main():
   suite = TestLoader().loadTestsFromTestCase(FixPDFMarkTests)
   TextTestRunner(verbosity=2).run(suite)
   
if __name__ == "__main__":
   main()
