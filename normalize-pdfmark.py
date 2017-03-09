#!/usr/bin/python
# -*- coding: utf-8 -*-

#calling a linux command...
#https://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/

import os
import sys
import time
import argparse
import getsize as gs
import pdfdates as pd
import runmodes as mod
import folderscan as fs
import writepdfmark as wx
import pdfmarkfunctions as pfm

#routing mechanism depending on user choices.   
def normalizepdf(loc, ext, mode):

   filelist = fs.pre_folderscan(args.loc, ext)
   sys.stderr.write("No. files discovered: " + str(len(filelist)) + "\n\n")

   if mode == mod.MODTEST:
      pfm.test_mode(filelist, mode)

   elif mode == mod.MODDRY:
      pfm.dry_and_fix_mode(filelist, mode)
   
   elif mode == mod.MODFIX:
      pfm.dry_and_fix_mode(filelist, mode)

   fixedlist = fs.post_folderscan(args.loc, ext)

   sys.stderr.write("No. old files: " + str(len(filelist)) + "\n")
   sys.stderr.write("No. new files: " + str(len(fixedlist)) + "\n")

#return a constant to help us route our code.
def getmode(dry, test, fix):
   if dry == True:
      sys.stderr.write("MODE: PDF-DATE-FIX: Performing dry-run analysis.\n")
      return mod.MODDRY
   if test == True:
      sys.stderr.write("MODE: PDF-DATE-FIX: Performing test-scan calibration analysis.\n")
      return mod.MODTEST
   if fix == True:
      sys.stderr.write("MODE: PDF-DATE-FIX: Performing production fix.\n")
      return mod.MODFIX

def main():

   #	Handle command line arguments for the script
   parser = argparse.ArgumentParser(description='Rewrite PDF with old dates. A normalization script.')
   parser.add_argument('--loc', help='Mandatory: Source folder of all the PDFs.', default=False)
   parser.add_argument("--test", "--test-scan", help="Test existence of PDF markings for calibration.", action="store_true")
   parser.add_argument("--dry", "--dry-run", help="Output dry-run stats, don't write.", action="store_true")
   parser.add_argument("--fix", "--fix-run", help="Fix files and write.", action="store_true")   

   start_time = time.time()
   #time script execution time roughly...
   t0 = time.clock()

   if len(sys.argv) < 3:
      parser.print_help()
      sys.exit(1)

   #	Parse arguments into namespace object to reference later in the script
   global args
   args = parser.parse_args()

   mode = getmode(args.dry, args.test, args.fix)

   if args.loc:
      normalizepdf(args.loc, ".pdf", mode)
   else:
      parser.print_help()
      sys.exit(1)

   sys.stderr.write(str(time.clock() - t0) + " script execution time" + "\n")

if __name__ == "__main__":      
   main()
