#!/usr/bin/python
# -*- coding: utf-8 -*-

#For code below, if we want to find the earliest in a set
#of dates we can use the following function... along with a
#filter: if mx.allmarks[mark] == mx.PDFDATE:
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
   
   #loop around the file as many times as necessary to
   #retrieve our PDF Mark...
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

      #let loop continue...
      mm.seek(pos2)

   #IF Count less than one, we haven't data to work with
   if count < 1:
      #PDF Mark Not Found...
      #sys.stderr.write(f.name + ": " + str(mark) + " string not found.\n")
      return mx.PDFMARKNONE, False
      
   #IF count is greater than one, we have too much data to work with
   elif count > 1: 
      if len(set(multival)) > 1:
         #too many values in a set to not make a decision on
         if mode is mod.MODTEST:
            sys.stderr.write("Too many " + str(mark) + " fields: " + str(count) + " in File: " + f.name + "\n")
            sys.stderr.write("Values: " + ",".join(multival) + "\n")
         return mx.PDFMARKTOOMANY, "Count: " + str(len(set(multival)))
      else:   
         #we can divine a single value from the set
         return mx.PDFMARKSETOKAY, multival[0].replace('\r', '').replace('\n', '')
         
   #IF we're inbetween those states, everything is juuuust right!
   else:
      if mode is mod.MODTEST and pdfdate is not False:
         return mx.PDFMARKOKAY, pdfdate.replace('\r', '').replace('\n', '')
      if mode is mod.MODDRY and pdfdate is not False:
         return mx.PDFMARKOKAY, pdfdate         
      if mode is mod.MODFIX and pdfdate is not False:
         return mx.PDFMARKOKAY, pdfdate.replace('\r', '').replace('\n', '')
         
      return mx.PDFMARKNONE, False

def normalize_eof(eof):
   return str(eof).strip().replace('%','').replace('\r', '').replace('\n', '').replace('\00', 'NULL')

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

#Test mode: Output a CSV with all marks that we know about to understand
#what to migrate when converting via GhostScript...
def test_mode(filelist, mode):
   sys.stdout.write('"filename","filesize","' + '","'.join(mx.allmarks) + '","version","eof"'  + '\n')
   for f in filelist:   
      fsize = convert_size(os.path.getsize(f))
      with open(f, "r+b") as f:
         row = '"' + f.name + '",'
         row = row + '"' + fsize + '",'
         mm = mmap.mmap(f.fileno(), 0)
         
         #get pdf version
         version = get_version(mm)
         eof = check_eof(mm)
         
         for mark in mx.allmarks.keys():
            out = getPDFMark(mm, mark, f, mode)
            if out != mx.PDFMARKNONE:
               row = row + '"' + str(out[0]) + ': ' + str(out[1]) + '",'
            else:
               row = row + '"' + str(out[1]) + '",'

         row = row + '"' + str(version) + '",' + '"' + str(eof) + '"'  #hashes to indicate data gaps
         sys.stdout.write(row + "\n")

#add to provenance
def create_provenance(provenance, note, value):
   provenance = provenance + note + ": " + value + ". "
   return provenance

#Try and figure out the results of our inputs and whether they will work for us...
def process_output(f, out, mark, type, pdfmark, provenance, mode):
   fx = fixmx.FixPDFMark()
   if mode == mod.MODDRY:
      if type == mx.PDFDATE:
      
         #review datetype to fix...
         sys.stderr.write(os.path.basename(f.name) + " " + mark + " original: " + fx.getstrings(out[1]) + " becomes: " + fx.getstrings(fx.fixdatemarks(out[1])) + "\n")
         
         pdfmark.creationdate = fx.getstrings(fx.fixdatemarks(out[1]))
         pdfmark.writeme=True
      else:
         #Nothing else is a correction, just an extraction and movement...
         val = str(fx.getstrings(out[1]))
         if val != "":
            if mark == mx.producermark:
               provenance = create_provenance(provenance, "Original Producer was", val)
            elif mark == mx.creatormark:
               provenance = create_provenance(provenance, "Original Creator was", val)
            elif mark == mx.titlemark:
               provenance = create_provenance(provenance, "Original Title was", val)
            elif mark == mx.authormark:
               provenance = create_provenance(provenance, "Original Author was", val)
            elif mark == mx.subjectmark:
               provenance = create_provenance(provenance, "Original Subject was", val)
            elif mark == mx.keywordmark:
               provenance = create_provenance(provenance, "Original Keywords were", val)
      return provenance.strip() + " "
   elif mode == mod.MODFIX:   
      return 
 
#Process the files.
def dry_and_fix_mode(filelist, mode):

   for f in filelist:
     
      pdfmark = wx.PDFMark()
      provenance = ""
      with open(f, "r+b") as f:   
            
         sys.stderr.write("Processing: " + os.path.basename(f.name) + "\n")
      
         mm = mmap.mmap(f.fileno(), 0)        
         checkdate = getPDFMark(mm, mx.creationdate, f, mode)
         moddate = getPDFMark(mm, mx.modmark, f, mode)
         if checkdate is False and moddate is False:
            #NB. If both dates are missing from the file we ignore it because
            #We're not seeing the fields causing the validation issues. If one
            #date or the other are not there we still need to do a rewrite to fix
            #validation issues sent to us via JHOVE (and verified in PDFMark reference)
            sys.stderr.write(f.name + ": " + "creation and modification dates missing from file. Fix mode will ignore file." + "\n")
         else:
            for mark in mx.allmarks.keys():
               #we can ignore modified date because this will
               #be written as today's date during the rewrite
               if mark != mx.modmark:
                  out = getPDFMark(mm, mark, f, mode)
                  if out[0] is not mx.PDFMARKNONE and out[0] is not mx.PDFMARKTOOMANY:
                     #process data                   
                     provenance = process_output(f, out, mark, mx.allmarks[mark], pdfmark, provenance, mode)
                  elif out[0] is mx.PDFMARKTOOMANY:
                     sys.stderr.write("Too many " + str(mark) + " fields in file to work with. File: " + f.name + "\n")
                     sys.exit(1)

      b = wx.WritePDFMark().__init_from_object__(pdfmark)
      if len(provenance) != 0:
         pdfmark.writeme=True
         b.add_custom({"Provenance": provenance.strip(), "Comment": Version().getversion()})
      if pdfmark.writeme == True:
         b.title = os.path.basename(f.name)    
         b.creator = Version().getcreator()
         b.write_mark_str()
         b.write_mark()
         
         fix_subprocess(f.name, fs.new_file_prefix)
         
      else:
         sys.stderr.write("File not to be re-written: " + f.name + "\n")