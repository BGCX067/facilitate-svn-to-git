#!/usr/bin/python

from Cerenity.MimeDict import MimeDict
import os
import glob

def _getVersionFilename(pagename, version, docbase):
    if version is not None:
        return "%s/.versions/%s.%s.html" % (docbase, pagename, str(version))
    return "%s/%s.html" % (docbase, pagename)

def _getPage(docbase, pagename="FrontPage", version=None, checkdefault=0):
    if checkdefault:
        docbase = "Content.default"
    f = open(_getVersionFilename(pagename, version, docbase))
    content = f.read()
    f.close()
    return content

def _pageVersions(docbase, pagename="FrontPage"):
    base = "%s/.versions/%s.[0-9]*.html" % (docbase, pagename)
    glib = glob.glob(base)
    version = len(glib) + 1
    return version

def _pageEditor(pagename="FrontPage", version=None):
    return "Anonymous Coward"

def _writePage(docbase, pagename="FrontPage", version=None):
    f = open(_getVersionFilename(pagename, version, docbase), "wb")
    f.write(str(context["meta"]))
    f.close()



def getPage(context):
    docbase = context["docbase"]
    if context["pagename"][-5:] == ".html":
        context["pagename"] = context["pagename"][:-5]
    try:
        # First of all, just try to get the page with the given version.
        content = _getPage(docbase, context["pagename"],context["pageversion"])
    except IOError, e:
        try:
            # If that fails for some reason, try to get the current version.
            content = _getPage(docbase, context["pagename"])
        except IOError, e:
            # If that fails - no such file or directory....
            if e.errno == 2:
                # It's possible they're after the index for a subdirectory.
                # If the page name ends with "/" this is the case, so retry that instead,
                # after postpending the defaultpage name
                if context["pagename"][-1] == "/":
                   context["pagename"] += context["defaultpage"]
                   return getPage(context)
                
                # Otherwise the page doesn't exist.
                # In which case, let's see if it exists as a default page then!
                try:
                    content = _getPage(docbase, context["pagename"], checkdefault=1)
                except IOError, e:
                    # well, that failed too, let's just load the page we load when the
                    # page is missing then!
                    
                    # However, we give people the option to customise the NewPageTemplate as
                    # well, so we need to do that in try...except as well
                    try:
                        content = _getPage(docbase, context["missingpage"])
                    except IOError, e:
                        content = _getPage(docbase, context["missingpage"], checkdefault=1)
                # raise e
            else:
                raise IOError
    dictable = MimeDict.fromString(content)
    dictable["__BODY__"] = content
    return content, dictable

def getTemplate(context):
    mode = context["mode"]
    try:
       subtype = context["form"]["template"]
       try:
           subtype = "." +str(subtype.value)
       except AttributeError:
           subtype = ""
    except KeyError:
       subtype = ""

    try:
        # First of all, try page specific template
        f = open("templates/%s.%s.tmpl%s"% (context["pagename"],mode,subtype) )
    except IOError:
        # Failed for some reason, so look for a locally customised template
        try:
            f = open("templates/%s.tmpl%s"% (mode,subtype) )
        except IOError:
            # OK, no page specific, or site specific template. Use the default instead.
            f = open("templates/%s.tmpl.default%s" % (mode,subtype) )
    template = f.read()
    f.close()
    return template

def pageExists(docbase, pagename="FrontPage"):
    try:
        page = _getPage(docbase, pagename)
    except IOError, e:
        return -1
    return len(page)

def storePage(context):
    docbase = context["docbase"]
    current_version = _pageVersions(docbase, context["pagename"])
    try:
        os.renames("%s/%s.html" % (docbase, context["pagename"]),
                   "%s/.versions/%s.%s.html" % (docbase, context["pagename"], str(current_version)))
    except OSError,e:
        if e[0] == 2: # No such file or directory - means it's a new file!
            pass 
        else:
            raise e # Some other error
    try:
        f = open("%s/%s.html" % (docbase, context["pagename"]), "wb")
        f.write(str(context["meta"]))
        f.close()
    except IOError, e:
        if e.errno == 13:
            context["content"] += "<h1> WARNING : DID NOT SAVE !</h1>"
            context["content"] += "<h1> Permissions Wrong, please fix </h1>"
        else:
            if e.errno == 2:
                if "/" in context["pagename"]:
                    os.makedirs(docbase+"/"+os.path.dirname(context["pagename"]))
#                    raise "here"
                    f = open("%s/%s.html" % (docbase, context["pagename"]),"wb")
                    f.write(str(context["meta"]))
                    f.close()
                else:
                    raise "Here ("+str(context["pagename"])+")"
            else:
                raise e
