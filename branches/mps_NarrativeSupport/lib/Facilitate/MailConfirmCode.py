#!/usr/bin/python


import smtplib

# ----------------------------------------------------------------------------------------
#
# Configuration. 
#
AUTHREQUIRED = 0 # if you need to use SMTP AUTH set to 1
smtpuser = ''  # for SMTP AUTH, set SMTP username here
smtppass = ''  # for SMTP AUTH, set SMTP password here

smtpserver = "127.0.0.1"
HOSTDOMAIN = "bicker.kamaelia.org"
SENDER = 'do_not_reply@' + HOSTDOMAIN

# ----------------------------------------------------------------------------------------
#
# args = screenname, email, validation_url, admin
validation_plaintext = """\
Hi!


We've received a request to create a user account on the "Bicker Manor"
website, using this email address for verification. Hopefully this is
you!
   [1] http://%(hostdomain)s/Home

They entered the following details:

    Screen name: %(screenname)s
    email: %(email)s

If this is you, please visit the following URL to confirm this:

    %(validation_url)s

If this isn't you, please ignore this email.

Also, please not: replying to this email will not validate you.

Thanks!

%(admin)s
"""

# ----------------------------------------------------------------------------------------
#
# args = screenname, email, validation_url, admin
validation_html = """\
<html>
<body>
<P>Hi!

<P>We've received a request to create a user account on the 
<a href="http://%(hostdomain)s/Home">"Bicker Manor"</a>
website, using this email address for verification. Hopefully this is
you!

<P>They entered the following details:
<ul>
    <li>Screen name: %(screenname)s
    <li>email: %(email)s
</ul>

<P> If this is you, please visit the following URL to confirm this:
<ul>
<a href="%(validation_url)s">%(validation_url)s</a>
</ul>

<P> If this isn't you, please ignore this email.

<P> Also, please not: replying to this email will not validate you.

<P>Thanks!

<P>%(admin)s
</body>
</html>
"""

# ----------------------------------------------------------------------------------------
#
# args = date, to, sender, subject, plaintext_email, html_email
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

import time

def sendMail(screenname, email, validation_url, admin, subject):
    bundle = {
        "screenname" : screenname,
        "email" : email,
        "validation_url" : validation_url,
        "admin" : admin,
        "hostdomain" : HOSTDOMAIN,
    }
    plainmail = validation_plaintext %  bundle
    htmlmail  = validation_html      % bundle

    mail = message_template % {
                 "date" : time.asctime(),
                 "to" : email,
                 "sender" : SENDER,
                 "subject" : subject,
                 "plaintext_email" : plainmail,
                 "html_email" : htmlmail,
                 "hostdomain" : HOSTDOMAIN,
           }
    mail = mail % {"hostdomain" : HOSTDOMAIN }
    session = smtplib.SMTP(smtpserver)
    if AUTHREQUIRED:
        session.login(smtpuser, smtppass)
    smtpresult = session.sendmail(SENDER, [ email ], mail)

    return mail

if __name__ == "__main__":

    print sendMail("Michael", 
               "ms@cerenity.org",
               "http://%(hostdomain)s/cgi-bin/app/register?action=confirmcode&regid=0&confirmationcode=c858dc05e905bacdb4fba0ca325ca1cd",
               "The Bicker Manor Team",
               "User registration confirmation for 'Bicker Manor'")

