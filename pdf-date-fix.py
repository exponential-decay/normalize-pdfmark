#!/usr/bin/python
# -*- coding: utf-8 -*-

#calling a linux command...
#https://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/

import os
import sys
import time
import mmap
import math
import argparse
import subprocess
import pdfmarkings as mx
import runmodes as mod
import pdfdates as pd
import fixpdfmark as fixmx

class Version:
   def getversion(self):
      return "0.0.1"

#return bytes in megabytes
#http://stackoverflow.com/a/14822210
def convert_size(size_bytes):
   if (size_bytes == 0):
       return '0B'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes/p, 2)
   return '%s %s' % (s, size_name[i])

def getEarlyDate(datelist):
   new_list = []
   pdfdate = pd.PDFDates()
   dateval = ''
   for d in datelist:
      if "D:" in d:
         dateval = d.split('(D:', 1)[1].replace(')', '')
      else:
         dateval = d.split('(', 1)[1].replace(')', '')
      new_list.append(pdfdate.valid_to_dateobj(dateval))

   compr = new_list[0]
   for d in new_list:
      if d[0] < compr[0]:
         compr = d
         
   return compr

def getPDFMark(mm, mark, f, mode):

   fix = fixmx.FixPDFMark()

   mm.seek(0)

   read = True
   count = 0
   pdfdate = False

   #list to hold multiple values
   multival = []

   while read:   
      pos1 = mm.find(mark)
      if pos1 is -1:
         read = False
         break
      count = count + 1
      mm.seek(pos1)

      pos2 = mm.find(mx.endmarkone)

      if pos2 is -1 or pos2 - pos1 > mx.readlimit:
         pos2 = mm.find(mx.endmarktwo)
      if pos2 is -1 or pos2 - pos1 > mx.readlimit:
         pos2 = mm.find(mx.endmarkthree)
      if pos2 is -1 or pos2 - pos1 > mx.readlimit:
         pos2 = mm.find(mx.endmarkfour)
      if pos2 is -1 or pos2 - pos1 > mx.readlimit:
         pos2 = mm.find(mx.endmarkfive)

      if pos2 is -1:
         read = False
         count = count - 1		#Only increment a count if valid PDF Mark
         break

      if pos2-pos1 < mx.readlimit:
         pdfdate = mm.read(pos2+1-pos1)
         multival.append(fix.normalizemark(pdfdate))

      #let loop happen...
      mm.seek(pos2)

   if count < 1:
      #PDF Mark Not Found...
      #sys.stderr.write(f.name + ": " + str(mark) + " string not found.\n")
      return False
   elif count > 1: 
      if len(set(multival)) > 1:
         sys.stderr.write(f.name + ": too many " + str(mark) + " fields." + "\n")
         sys.stderr.write(str(count) + ": ")
         sys.stderr.write(str(multival) + "\n")
         
         #if we've a date, we can try and return the earliest
         if mx.allmarks[mark] == mx.PDFDATE:
            sys.stderr.write("Earliest date: " + str(getEarlyDate(multival)) + "\n")
         
         return True, "Count: " + str(len(set(multival)))
      else:      
         return True, multival[0].replace('\r', '').replace('\n', '')
   else:
      if mode is mod.MODDRY:
         return pdfdate
      if mode is mod.MODTEST and pdfdate is not False:
         return True, pdfdate.replace('\r', '').replace('\n', '')
      else:
         return False
      if mode is mod.MODFIX:
         return pdfdate

def normalize_eof(eof):
   return str(eof).strip().replace('%','').replace('\r', '').replace('\n', '')

def get_version(mm):
   mm.seek(0)
   return str(mm.read(8)).strip().replace('\r', '').replace('\n', '').replace('\00', 'NULL')
   
def check_eof(mm):
   mm.seek(-8, os.SEEK_END)
   eof = mm.read(8)
   
   #Check for EOF
   if "EOF" in eof:
      return str(True)
   else:
      #Hashes used to spot other data issues between returned value...
      return '#' + normalize_eof(eof) + '#'

def normalizepdf(loc, ext, mode):

   filelist = folderscan(args.loc, ext)

   sys.stderr.write("No. files discovered: " + str(len(filelist)) + "\n")

   sys.stdout.write('"filename","filesize","' + '","'.join(mx.allmarks) + '","version","eof"'  + '\n')

   for f in filelist:   
   
      fsize = convert_size(os.path.getsize(f))
   
      with open(f, "r+b") as f:
         row = '"' + f.name + '",'                    #CSV output name
         row = row + '"' + fsize + '",'               #CSV output size
         mm = mmap.mmap(f.fileno(), 0)
         
         #get pdf version
         version = get_version(mm)
         eof = check_eof(mm)
         
         for mark in mx.allmarks.keys():
            out = getPDFMark(mm, mark, f, mode)
            if mode is mod.MODTEST:
               if out != False:
                  row = row + '"' + str(out[0]) + ': ' + str(out[1]) + '",'
               else:
                  row = row + '"' + str(out) + '",'

         if mode is mod.MODTEST:
            row = row + '"' + str(version) + '",' + '"' + str(eof) + '"'  #hashes to indicate data gaps
            sys.stdout.write(row + "\n")

      #recorddates(f)

      #call pdf command here...
      #p = subprocess.Popen(["file", f], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      #output, err = p.communicate()
      #print output.strip()

      #replaceoriginaldates(f)

   sys.stderr.write("No. old files: " + str(len(filelist)) + "\n")
   sys.stderr.write("No. new files: " + str(len(filelist)) + "\n")

def folderscan(loc, ext):
   flist = []
   for dir_paths, dir_names, filenames in os.walk(loc):
      for f in filenames:
         if os.path.splitext(f)[1].lower() == ext:
            # check we have a dir separator and add if not...
            if dir_paths.rsplit()[0][-1:] != "/":	
               flist.append(dir_paths + "/" + f)
            else:
               flist.append(dir_paths + f)
   return flist

def getmode(dry, test, fix):
   if dry == True:
      sys.stderr.write("PDF-DATE-FIX: Performing dry-run analysis.\n")
      return mod.MODDRY
   if test == True:
      sys.stderr.write("PDF-DATE-FIX: Performing test-scan calibration analysis.\n")
      return mod.MODTEST
   if fix == True:
      sys.stderr.write("PDF-DATE-FIX: Performing production fix.\n")
      return mod.MODFIX

def main():

   #	Handle command line arguments for the script
   parser = argparse.ArgumentParser(description='Rewrite PDF with old dates. A normalization script.')
   parser.add_argument('--loc', help='Mandatory: Source folder of all the PDFs.', default=False)
   parser.add_argument("--test", "--test-scan", help="Test existence of PDF markings for calibration.", action="store_true")
   parser.add_argument("--dry", "--dry-run", help="Output dry-run stats, don't write.", action="store_true")

   start_time = time.time()
   #time script execution time roughly...
   t0 = time.clock()

   if len(sys.argv) < 3:
      parser.print_help()
      sys.exit(1)

   #	Parse arguments into namespace object to reference later in the script
   global args
   args = parser.parse_args()

   mode = getmode(args.dry, args.test, False)

   if args.loc:
      normalizepdf(args.loc, ".pdf", mode)
   else:
      parser.print_help()
      sys.exit(1)

   sys.stderr.write(str(time.clock() - t0) + " script execution time" + "\n")

if __name__ == "__main__":      
   main()
