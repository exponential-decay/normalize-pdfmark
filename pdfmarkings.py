#!/usr/bin/python
# -*- coding: utf-8 -*-

#TYPES
PDFDATE = "DATE"
PDFSTRING = "STRING"
PDFKEYS = "KEYWORDS"

#readlimit
readlimit = 50

#/CreationDate
creationdate = '\x2F\x43\x72\x65\x61\x74\x69\x6F\x6E\x44\x61\x74\x65'

#/Producer
producermark = '\x2F\x50\x72\x6F\x64\x75\x63\x65\x72'

#/Creator
creatormark = '\x2F\x43\x72\x65\x61\x74\x6F\x72'

#/ModDate
modmark = '\x2F\x4D\x6F\x64\x44\x61\x74\x65'

#/Title
titlemark = '\x2F\x54\x69\x74\x6C\x65'

#/Author
authormark = '\x2F\x41\x75\x74\x68\x6F\x72'

#/Subject
subjectmark = '\x2F\x53\x75\x62\x6A\x65\x63\x74'

#/Keywords
keywordmark = '\x2F\x4B\x65\x79\x77\x6F\x72\x64\x73'

#/Allmarks, for test flag
allmarks = {creationdate: PDFDATE, producermark: PDFSTRING, creatormark: PDFSTRING, modmark: PDFDATE, \
   titlemark: PDFSTRING, authormark: PDFSTRING, subjectmark: PDFSTRING, keywordmark: PDFKEYS}

#/fixmarks, for dry, and fix flags
fixmarks = [creationdate, producermark, creatormark, titlemark, authormark, subjectmark, keywordmark]

#Terminators for PDF Mark sections

#endmark )\n
endmarkone = '\x29\x0A'
#endmark )[space]
endmarktwo = '\x29\x20'
#endmark )>>
endmarkthree = '\x29\x3E\x3E'
#endmark )\n
endmarkfour = '\x29\x0D'
#endmark )\
endmarkfive = '\x29\x2F'
