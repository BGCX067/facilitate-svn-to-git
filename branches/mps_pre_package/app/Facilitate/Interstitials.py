#!/usr/bin/python


head = """<html>
<head>
<title> </title>
<link rel=stylesheet type="text/css" href="/newcss.css">
</head>
<body style="font-size: 10pt; font-family:
verdana,arial,helvetica,sans-serif; line-height: 1.8;">
</div>
</span></p>
<div id="centreinbrowser">
    <table><tr><td>
        <div id="contentwrapper">
            <div id="contentpanel">
"""

foot = """
            </div>
        </div>
    </td></tr></table>
</div>
</body>
</html>
"""


failback = head + """
<P>Should never ever see this...
<pre>
%(body)s
</pre>
<P> Go back <a href="/Home">Home </a>?
""" + foot

# ----------------------------------------------------------------------------

error = head + """
<P><B>ERROR: %(message)s
<P> Record
<pre>
%(record)s
</pre>

<P> Go back <a href="/Home">Home </a>?
""" + foot

# ----------------------------------------------------------------------------

notdirect = head + """
<P><B>This script is not supposed to be called directly, please go back and try again.</b>
""" + foot

# ----------------------------------------------------------------------------

manual_frag = """
<!-- <P> Alternatively you may enter your confirmation code here:
<ul>
<form method="get" action="/cgi-bin/app/register">
    <P><input type="text" name="action"       value="confirmcode">
    <P><input type="text" name="regid"       value="%(regid)s">
    <P><input type="text" name="confirmationcode" value="%(confirmationcode)s">
    <input type="submit" value="submit confirm code">
</form>
</ul>
-->
"""

registration_success = head + """
<P><B> Thank you!</b>
<P> You are <b>nearly</b> registered!
<P> You will receive an email shortly with a link and confirmation code in. You will need
    to click on the link to confirm your identity.
<P>You entered the following information:
<ul>
<li> email: %(email)s (this is what you will use to login)
<li> Screen Name: %(screenname)s
<li> Date of Birth: %(dob.day)s %(dob.month)s %(dob.year)s
<li> Side chosen: %(side)s
</ul>
<p> We're obviously not displaying your password!
<P> Go back <a href="/Home">Home </a> whilst you wait for your mail?
""" + foot

# ----------------------------------------------------------------------------

confirmed_template = head + """
<P> Many thanks for confirming your identity.
<P> Next step should be a redirect, or similar - for now,
<a href="/MyProfile"> click here to go to your profile! </a>
<P> You could of course also go back <a href="/Home">Home</a>.
""" + foot

# ----------------------------------------------------------------------------

loggedin_template = head + """
<P>Thanks for logging in!
<P> Next step should be a redirect, or similar - for now,
<a href="/MyProfile"> click here to go to your profile </a>
<P> You could of course also go back <a href="/Home">Home</a>.
""" + foot

contact_added = head + """
<h3>Contact Added!</h3>
<P> <a href="/BrowseParticipants">Browse more contacts</a> to add
<P> Got to <a href="/MyFriends">your friends page</a>
<P> <a href="/MyProfile"> Go back to your profile </a>
<P> You could of course also go back <a href="/Home">Home</a>.
""" + foot


uploadok = head + """\
<h3>Image Uploaded OK!</h3>
<P> <a href="/MyMedia">Back to your media</a>  to view & add more
<P> <a href="/MyProfile"> Go back to your profile </a>
<P> You could of course also go back <a href="/Home">Home</a>.
""" + foot

video_uploadok = head + """\
<h3>Video Uploaded OK!</h3>
<P> <a href="/MyMedia">Back to your media</a>  to view & add more
<P> <a href="/MyProfile"> Go back to your profile </a>
<P> You could of course also go back <a href="/Home">Home</a>.
""" + foot
