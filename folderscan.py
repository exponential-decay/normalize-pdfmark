#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

new_file_prefix = "FIXED_"

def pre_folderscan(loc, ext):
   flist = []
   for dir_paths, dir_names, filenames in os.walk(loc):
      for f in filenames:
         if new_file_prefix not in f:
            if os.path.splitext(f)[1].lower() == ext:
               # check we have a dir separator and add if not...
               if dir_paths.rsplit()[0][-1:] != "/":	
                  flist.append(dir_paths + "/" + f)
               else:
                  flist.append(dir_paths + f)
         else:
            sys.stderr.write("Ignoring file (previously FIXED): " + str(f) + "\n")
   return flist

def post_folderscan(loc, ext):
   flist = []
   for dir_paths, dir_names, filenames in os.walk(loc):
      for f in filenames:
         if new_file_prefix in f:
            if os.path.splitext(f)[1].lower() == ext:
               # check we have a dir separator and add if not...
               if dir_paths.rsplit()[0][-1:] != "/":	
                  flist.append(dir_paths + "/" + f)
               else:
                  flist.append(dir_paths + f)
   return flist