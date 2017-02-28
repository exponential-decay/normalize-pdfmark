#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase, TestLoader, TextTestRunner
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


class PDFDateTests(TestCase):

	pd = pd.PDFDates()

	baddates = ['Tue Jun 15 12:03:57 1999', 'Thu Sep 17 14:19:15 1998', \
		'Mon Nov 02 15:08:13 1998','Fri Sep 18 13:56:59 1998']

	betterdates = ["20011113154838\\000", "20120928200040+12'00'", "20170221052217+13'00'", \
		"20161111151406+13'00'", "20080513135759+12'00'", "20120928200040+12'00'", \
			"20071206114242+13'00'"]

	gooddates = ["20011114110636"]

	def test_bad_dates(self):
		print
		for d in self.baddates:
			print self.pd.invalid_to_pdfdate(d)
		self.assertEqual('A', 'A')

	def test_better_dates(self):
		print
		for d in self.betterdates:
			print self.pd.valid_to_dateobj(d)
		self.assertEqual('A', 'A')

def main():
	suite = TestLoader().loadTestsFromTestCase(PDFDateTests)
	TextTestRunner(verbosity=2).run(suite)
	
if __name__ == "__main__":
	main()
