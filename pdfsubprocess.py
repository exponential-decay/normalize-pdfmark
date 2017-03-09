#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
import getsize as gs

#Piece everything we've done together by calling ghostscript and 
#adding the PDFMark to the file we're processing...     
def fix_subprocess(fname, prefix):
   dirname = os.path.dirname(fname)
   newf = prefix + os.path.basename(fname)
   newname = os.path.join(dirname + os.path.sep + newf)

   #example command
   #gs -o newname.pdf -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress -dFastWebView fname.pdf "pdfmark"
   
   p = subprocess.Popen(["gs", "-o", newname, "-sDEVICE=pdfwrite", "-dPDFSETTINGS=/default", "-dFastWebView", "-dNumRenderingThreads=4", fname, "pdfmark"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   output, err = p.communicate()
   sys.stderr.write("Original fsize: " + gs.convert_size(os.path.getsize(fname)) + " New fsize: " + gs.convert_size(os.path.getsize(newname)) + "\n\n")
   time.sleep(2)
