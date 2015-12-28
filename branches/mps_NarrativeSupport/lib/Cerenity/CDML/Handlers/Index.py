#!/usr/bin/env python

import os.path
import os
import time

stat_cache = {}

def file_last_modified(docbase, file, force=True):
   # Created so we can cache the results (!)
   if stat_cache == {}:
      try:
        f = open(os.path.join(docbase, ".statcache"), "rb")
        file_str = f.read()
        f.close()
        items = file_str.split("\xff")
        for item in items:
#            X = item.split("\0")
#            raise repr(X)
            try:
                (docbase, file, str_mtime ) = item.split("\0")
            except ValueError, e:
                continue
#                X = item.split("\0")
#                raise repr(X)
            stat_cache[(docbase, file)] = int(str_mtime)
      except IOError: # not yet cached :-)
         pass
   try:
      if not force:
         mtime = stat_cache[(docbase, file)]
      else:
         raise KeyError
   except KeyError:
      mtime = os.stat(os.path.join(docbase,file)).st_mtime
      stat_cache[(docbase, file)] = mtime
      stat_cache["dirty"] = True
   return mtime

def store_stat_cache(docbase):
    items = []
    for item in stat_cache:
        docbase, file = item
        mtime = stat_cache[item]
        encoded = "\0".join([docbase, file, str(mtime)])
        items.append(encoded)

    file_str = "\xff".join(items)
    f = open(os.path.join(docbase, ".statcache"), "wb")
    f.write(file_str)
    f.flush()
    f.close()
    

def FileListing(docbase, traverse):
    # ripe for caching!
    #
    # FIXME: This should be interated with the stat_cache to make it work properly...
    # 
    dir_last_mod = os.stat(docbase).st_mtime
    try:
        dir_last_cached = os.stat(os.path.join(docbase, ".filecache")).st_mtime
    except OSError:
        dir_last_cached = 0

    if dir_last_mod > dir_last_cached: # directory changed since cached
        # get file listing from directory
        x = os.listdir(docbase)
        file_str = os.path.sep.join(x)
        f = open(os.path.join(docbase, ".filecache"), "wb")
        f.write(file_str)
        f.flush()
        f.close()
    else:
        # retrieve file listing from file
        f = open(os.path.join(docbase, ".filecache"), "rb")
        Xs = f.read()
        f.close()
        x = [ z for z in Xs.split(os.path.sep) ]

    x = [ z for z in x if (z != ".filecache") and (z != ".statcache") 
          and ("CVS/" not in z) and (z != "CVS" ) ]
    X = []
    for a in x:
       if os.path.isdir(os.path.join(docbase, a)):
           if not os.path.islink(os.path.join(docbase, a)):
               if a != ".svn" and a != ".versions" :
                  R = FileListing(os.path.join(docbase, a), traverse)
                  X = X+ [ os.path.join(a, b) for b in R ]
       else:
           X.append(a)
    
    return X

def cropExtension(files, extension):
    result = []
    try:
       for fullpath, name in files:
           fullpath = fullpath[:fullpath.rfind(".")]
           name = name[:name.rfind(".")]
           result.append((fullpath,name))
    except ValueError: 
       for fullpath, name, date in files:
           fullpath = fullpath[:fullpath.rfind(".")]
           name = name[:name.rfind(".")]
           result.append((fullpath,name,date))
    
    return result

def doCompactForm(files, subdir, y):
    format = '<a href="%s"> %s</a>'
    if subdir is None:
        files = [(x[1],x[1]) for x in y]
    else:
        files = [("/" + subdir + "/" + x[1],x[1]) for x in y]
    return format, files

def doRegularOrderedForm(files, subdir, y):
    format = '<a href="%s"> %s</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(<i>%s</i>)'
    if subdir is None:
        files = [(x[1],x[1],
                  time.ctime(x[0])
                 ) for x in y]
    else:
        files = [("/"+subdir+"/"+x[1],x[1],
                  time.ctime(x[0])
                 ) for x in y]
    return format, files

class tagHandler(object):

      def doIndex(bunch, text, env):
         """[[index][cropextension=<bool>][nobullet=.][limit=][sub=][order=<ordering>][compact=<bool>] text ]
         Used for creating indexes on the site. 
         If you want to not show the extensions (recommended often), set cropextension to True
         If you just want a list with no bullets, set that to true.
         If you want to only traverse subdirectories, set sub to the subdirectory
         The only ordering supported (if supplying the order attribute) is "recent". Defaults to alphabetical otherwise
         Setting compact to true gives a more compact layout"""
         extension     = bunch.get("extension", ".html")
         cropextension = bunch.get("cropextension", False)
         nobullet      = bunch.get("nobullet", None)
         limit         = int(bunch.get("limit", 10))
         subdir        = bunch.get("sub", None) # WARNING: POTENT FOR HOLE(!)
         traverse      = bunch.get("traverse", None)

         if subdir and (".." in subdir):              # WARNING: HENCE WHY WE SCRUB THE VALUE HERE
                return "bad subdirectory"   # If /anything/ unwanted, just don't even try

         docbase = env["docbase"]
         if subdir is not None:
             docbase = os.path.join(docbase, subdir)
         
         files = FileListing(docbase, traverse)
         files.sort()

         # Get limit(num) of files by last modifcation time
         files_by_date = [ (file_last_modified(docbase,x),x) for x in files ]
         files_by_date.sort()
         files_by_date.reverse()
         files_by_date = files_by_date[:limit]

         # This format is used by Index, not by recentchanges
         format = '<a href="%s"> %s</a>'
         if subdir is None:
             files = [(x,x) for x in files]
         else:
             files = [("/"+subdir+"/"+x,x) for x in files]

         if bunch.get("order"):
             if bunch["order"] == "recent":
                if bunch.get("compact", None) is None:
                    format, files = doRegularOrderedForm(files, subdir, files_by_date)
                else:
                    format, files = doCompactForm(files, subdir, files_by_date)
         
         if cropextension:
             files = cropExtension(files, extension)

         if nobullet is None:
             fileString = "<ul>"
             for file in files:
                filelink = format % file
                fileString += "<li> %s </li>" % filelink
             fileString += "</ul>"
         else:
             links = [ (format % file) for file in files ]
             fileString = str(nobullet).join(links)

         result = """%s
         %s
         """ % (text, fileString)
         if stat_cache.get("dirty",False):
             del stat_cache["dirty"]
             store_stat_cache(docbase)
         
         return result

      mapping = {
                 "index": doIndex,
      }
      
mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   
