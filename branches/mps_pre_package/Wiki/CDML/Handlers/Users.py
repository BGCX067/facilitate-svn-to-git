#!/usr/bin/env python

import anydbm
import smtplib
import time
import math
from CDML.Page import pageExists

# = EMAIL ===================

AUTHREQUIRED = 0 # if you need to use SMTP AUTH set to 1
smtpuser = ''  # for SMTP AUTH, set SMTP username here
smtppass = ''  # for SMTP AUTH, set SMTP password here

home = 0

if home:
    smtpserver = 'mail.cerenity.org'
    SENDER = 'ms@cerenity.org'
else:
    smtpserver = "127.0.0.1"
    SENDER = 'michael.sparks@bbc.co.uk'


tostring = 'ms@cerenity.org'

validation_plaintext = """\
Hi!

Someone has tried to validate the following details on our site[1],
hopefully this is you!

   [1] %(website)s

Name: %(valid_name)s
id: %(valid_id)s
email: %(valid_email)s

If this is you, please visit the following URL to confirm this:

%(validation_url)s

*REPLYING TO THIS EMAIL WILL NOT VALIDATE YOU*

Thanks!

%(admin)s
"""

validation_html = """
<html>
<body>
<P>Hi!

<P>Someone has tried to validate the following details on our 
<a href="%(website)s">site</a> (%(website)s) -- hopefully this <b>is</b> you!
<ul>
Name: %(valid_name)s <br>
email: %(valid_email)s <br>
id: %(valid_id)s <br>
</ul>
<P>If this is you, please visit the following URL to confirm this:
<ul>
<a href="%(validation_url)s">%(validation_url)s</a>
</ul>

<P><b>REPLYING TO THIS EMAIL WILL NOT VALIDATE YOU</b>

<P>Thanks!

<P>%(admin)s
</body>
</html>
"""

message_template = """\
Date: %(date)s
To: %(to)s
From: %(sender)s
Subject: %(subject)s
Content-type: multipart/alternative;
  boundary="***boundary***"

--***boundary***
Content-Type: text/plain;

%(plaintext_email)s
--***boundary***
Content-Type: text/html;

%(html_email)s
--***boundary***--

"""


def get_cookie(env, thecookie, default="NO DEFAULT VALUE"):
    try:
        value = env["context"]["cookies"][thecookie].value
    except KeyError:
        value = default
    return value

def get_formItem(env, someitem, default="NO DEFAULT VALUE"):
    try:
        value = env["context"]["form"][someitem].value
    except KeyError:
        value = default
    return value

def set_cookie(env, thecookie, value):
    env["context"]["newcookies"][thecookie] = value

def askForUsername(env, debug):
    debug("""<P>
<form method="get" action="%(cgipath)s%(pagename)s" enctype="application/x-www-form-urlencoded">
<input type="hidden" name="prefsmode" value="update" />
<table border="0">
<tr><td>Name </td><td> <input type="text" name="name" value="%(user)s" width="70"> </td></tr>
<tr><td>Email </td><td> <input type="text" name="email" value="%(user_email)s" width="70"> </td></tr>
<tr><td>Remember </td><td> <input type="checkbox" name="remember" checked="%(remember_preferences)s" > </td></tr>
<tr><td>Validate Email </td><td> <input type="checkbox" name="validate" checked="%(validate_email)s" > </td></tr>
<tr><td colpan="2"><input type="submit" value="&lt;&lt;submit&gt;&gt;"></td></tr>
</table>
</form>
</ul>
""" % env )

def get_next_id(env):
#    \
#raise str(env["context"]["userstatefile"])
    f = anydbm.open(env["context"]["userstatefile"],"c")
    try:
        f["highest_id"] = str( int(f["highest_id"]) + 1 )
    except KeyError:
        f["highest_id"] = "1"
    result = f["highest_id"]
    f.close()
    return str(result)

def mailValidationURL(env):
    
    f = anydbm.open(env["context"]["userstatefile"],"c")

    f["email_to_id"+str(env["context"]["user_email"])] = env["context"]["userid"]
    f["id2e:"+str(env["context"]["userid"])] = env["context"]["user_email"]
    f["id2n:"+str(env["context"]["userid"])] = env["context"]["user"]
    f["id:validated"+str(env["context"]["userid"])] = "0"
    import random
    found_unused_id = False
    while not found_unused_id:
        validation_code = str(random.randint(100000000000000,1000000000000000-1))
        try:
            f[validation_code]
        except KeyError:
            found_unused_id = True
    f[validation_code] = str(env["context"]["userid"])
    f.close()

    validation_params = {
        "valid_name" : env["context"]["user"],
        "valid_id" : env["context"]["userid"],
        "valid_email" : env["context"]["user_email"],
        "validation_url" : env["context"]["root"]+env["context"]["pagename"]+"?validation="+validation_code,
        "admin" : env["context"]["admin"],
        "website" : env["context"]["root"],
    }
    message = message_template % {
        "date" : time.asctime(),
        "sender" : SENDER,
        "to" : env["context"]["user_email"],
        "subject" : "Validation to use the wiki",
        "plaintext_email" : validation_plaintext  % validation_params,
        "html_email" : validation_html  % validation_params,
    }
    RECIPIENTS = [ env["context"]["user_email"] ]
    session = smtplib.SMTP(smtpserver)
    if AUTHREQUIRED:
        session.login(smtpuser, smtppass)
    smtpresult = session.sendmail(SENDER, RECIPIENTS, message)

    if smtpresult:
        errstr = ""
        for recip in smtpresult.keys():
            errstr = """Could not delivery mail to: %s

    Server said: %s
    %s

    %s""" % (recip, smtpresult[recip][0], smtpresult[recip][1], errstr)
        raise smtplib.SMTPException, errstr

    env["systemnote"] = ( "<P>Information Validation Email sent! ") #+
                          #(to:" + 
                          #repr(RECIPIENTS) + ")<p><pre>\n" + 
                          #message+"\n</pre>" +
                          #"<p>" + repr(smtpresult) + 
                          #"<p>" + smtpserver +
                          #"<p>" + SENDER  )


def ensureUsernameDefined(env):
    if env["context"]["username"] == "":
        name_from_form = get_formItem(env, "name", default=None)
        if name_from_form:
            env["context"]["user"] = name_from_form
            if get_formItem(env, "validate", default=False):
                email = get_formItem(env, "email", default="nobody@example.com")
                if email != "nobody@example.com":
                    set_cookie(env, "email", email)
                    env["context"]["user_email"] = email
                    mailValidationURL(env)

            remember = get_formItem(env, "remember", default=None)
            if remember:
                set_cookie(env, "name", name_from_form)
        elif env["context"]["user"] == "guest":
            username_from_cookie = get_cookie(env, "name", default=None)
            if username_from_cookie:
                env["context"]["user"] = username_from_cookie
            else:
                env["context"]["newuser"] = True
    env["context"]["username"] = env["context"]["user"]

def ensureUserIDDefined(env):
    if not env["context"]["userid"]:
        userid = get_cookie(env, "id", default=None)
        if userid == None:
            userid = get_next_id(env)
            set_cookie(env, "id", userid)
        env["context"]["userid"] = userid

def ensureEmailDefined(env):
    if not env["context"]["user_email"]:
        env["context"]["user_email"] = get_cookie(env, "email", default="nobody@example.com")

def handleUserValidation(env):
    if env["context"]["handled_validation"]:
        return
    env["context"]["handled_validation"] = True

    validation_code = get_formItem(env, "validation", default=None)
    if validation_code:
        import random
        f = anydbm.open(env["context"]["userstatefile"],"c")
        try:
            env["context"]["userid"] = f[validation_code]
            f["id:validated"+str(env["context"]["userid"])] = str( random.randint(1000000000,10000000000-1) )

            email = f["id2e:"+str(env["context"]["userid"])]
            name = f["id2n:"+str(env["context"]["userid"])]

#            set_cookie(env, "id", env["context"]["userid"])
            set_cookie(env, "name", name)
            set_cookie(env, "email", email)
            set_cookie(env, "VVC", f["id:validated"+str(env["context"]["userid"])])
            env["context"]["name_validation"] = "(validated)"
            env["context"]["email_validation"] = "(validated)"

            env["systemnote"] = "<P><b>VALIDATION SUCCEEDED </b> "
        except KeyError:
            env["systemnote"] = "<P><b>VALIDATION FAILED !</b> "
            f["id:validated"+str(env["context"]["userid"])] = "0"
        f.close()
    else:
        f = anydbm.open(env["context"]["userstatefile"],"c")
        try:
            VVC = f["id:validated"+str(env["context"]["userid"])]
            if VVC == "0":
                pass
            else:
                VVC_cookie = get_cookie(env, "VVC", None)
                if VVC_cookie == VVC:
                    env["context"]["name_validation"] = "(validated)"
                    env["context"]["email_validation"] = "(validated)"
        except KeyError:
            pass
        f.close()


class tagHandler(object):
    def doUser(bunch, text, env):
        """[[user] ] - FIXME"""
        ensureUserIDDefined(env)
        handleUserValidation(env)
        ensureEmailDefined(env)
        ensureUsernameDefined(env)


        userid = env["context"]["userid"]
        tag = " " + env["context"]["name_validation"]
        if env["context"]["user"] == "guest":
            tag = userid

        if bunch.get("notag",None) == None:
            return env["context"]["user"]+tag
        else:
            return env["context"]["user"]

    def doPrefs(bunch, text, env):
        """[[prefs] ] - FIXME"""
        result = []
        ensureUserIDDefined(env)
        ensureEmailDefined(env)
        ensureUsernameDefined(env)
        askForUsername(env["context"], result.append)

        return text + "<br>".join(result)

    def doUserTags(bunch, text, env):
        """[[user_tags] ] - FIXME"""

        prenote = ""
        if env["context"]["email_validation"] == "(validated)":
            usertags = get_formItem(env, "tags", default=None)
            if usertags != None:
                f = anydbm.open(env["context"]["userstatefile"],"c")
                f[str(env["context"]["userid"]) + ":tags:" + env["context"]["pagename"] ] = usertags
                tags = usertags
                prenote = "<b>User tags saved</b> <br>"
                f.close()

            f = anydbm.open(env["context"]["userstatefile"],"c")
            try:
                tags = f[str(env["context"]["userid"]) + ":tags:" + env["context"]["pagename"] ]
            except KeyError:
                tags = "( no tags defined - tags are comma seperated 1-3 word phrases)"
            f.close()
            tagbox = """%(prenote)s
<form method="post" action="%(cgipath)s%(pagename)s" enctype="application/x-www-form-urlencoded">
<input type="hidden" name="usertagsmode" value="update" />
<input type="text" name="tags" value="%(tags)s" style="width: 85%%">
<input type="submit" value="save"></td></tr>
</table>
</form>""" % { "prenote" : prenote,
               "cgipath": "/cgi-bin/Wiki/edit/", #env["context"]["cgipath"],
               "pagename":env["context"]["pagename"],
               "tags": tags }

            return tagbox
        else:
            return "<font size='-1'>If you had set <a href='%s'>UserPreferences</a> (name & email) and validated them (simple single click in your email), you would be able to define personal tags </font>" % (env["context"]["cgipath"]+"UserPreferences",)

    def doAllUserTagsThisPage(bunch, text, env):
        """[[all_user_tags_this_page] ] Shows all the user tags for the
        currently viewed page."""
        f = anydbm.open(env["context"]["userstatefile"],"c")
        tagsets = [ (f[x]) for x in f.keys() if ":tags:"+ env["context"]["pagename"] in x ]
        f.close()
        tags = {}
        for tagset in tagsets:
            for tag in [ x.rstrip().strip() for x in tagset.split(",") ]:
                # make a wiki word for linking
                wikiTag = "".join([ y.capitalize() for y in tag.split(" ") if y != ''])
                tag = tag.replace(" ", "&nbsp;")
                tag = ("<a href='%s'>" + tag + "</a>") % ( env["context"]["cgipath"]+wikiTag, )
                tags[tag] = tags.get(tag,0) + 1
        if tags.keys() == []:
            return "No tags are defined for this page yet - how would you classify/think of this page? <a href= '#usertags'>Add your notes below!</a>"
        else:
            return "All tags for this page<p align='centre'>"+ "&nbsp;&nbsp; ".join(tags.keys())+ "</p>"

    def doAllUserTagsAllPages(bunch, text, env):
        """[[all_user_tags_all_pages] ] - outputs all the tags added by users for all pages"""
        f = anydbm.open(env["context"]["userstatefile"],"c")
        tagsets = [ (f[x]) for x in f.keys() if ":tags:" in x ]
        f.close()
        tags = {}
        for tagset in tagsets:
            for tag in [ x.rstrip().strip() for x in tagset.split(",") ]:
                # make a wiki word for linking
                wikiTag = "".join([ y.capitalize() for y in tag.split(" ") if y != ''])
                tag = tag.replace(" ", "&nbsp;")
                tag = ("<a href='%s'>" + tag + "</a>") % ( env["context"]["cgipath"]+wikiTag, )
                tags[tag] = tags.get(tag,0) + 1
        return "All tags for all pages<p align='centre'>"+ "&nbsp;&nbsp; ".join(tags.keys())+ "</p>"

    def doTagLinkCloud(bunch, text, env):
        """[[taglinkcloud] <text>] Splits text into phrases. Phrases are
        comma seperated. These made into a cloud of (wikiword) links to
        pages of those names. (experimental). Tag sizes reflect file size."""
        tags = text.split(",")
        result = [""]
        for tag in tags:
            wikiTag = "".join([ y.capitalize() for y in tag.split(" ") if y != ''])
            tag = tag.replace(" ", "&nbsp;")
            tag = ("<a href='%s'>" + tag + "</a>") % ( env["context"]["cgipath"]+wikiTag, )
            size = pageExists(env["docbase"], wikiTag)
            if size != -1:
                fontsize = (math.log(size)/5.5)**2
                if fontsize <1.2:
                    fontsize = 1.2
                tag = "<span style='font-weight: bolder; font-size: "+str(fontsize) + "em'>" + tag +"</span>"
            result.append(tag)
        return "&nbsp;&nbsp; ".join(result)

    mapping = {
               "prefs" : doPrefs,
               "user" : doUser,
               "user_tags" : doUserTags,
               "all_user_tags_this_page" : doAllUserTagsThisPage,
               "all_user_tags_all_pages" : doAllUserTagsAllPages,
               "taglinkcloud" : doTagLinkCloud,
    }

mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping


"""

# Basic trust level.

username = guest
-------------------------------------------------
# Basic authentication - call then what they ask us to call them

username = guest

if name from form:
    username_form = name from form
    if remember == 1
       set_cookie "name" = username_form

if username == guest
   username = get_cookie("name", None)


----------------------------------------------------------------------------
# Next level - allow them to have some preference associated with their name.
#
# For this we need to distinguish users.
# No private preferences at this stage, because any user can spoof any other.
# To distinguish users we need an id as well.
#

username = guest

if name from form:
    username_form = name from form
    if remember == 1
        set_cookie "name" = username_form

if username == guest
   username = get_cookie("name", None)

userid = get_cookie("userid", None)
if userid == None:
    ID = get_next_id()
    set_cookie "id" = ID


"""
