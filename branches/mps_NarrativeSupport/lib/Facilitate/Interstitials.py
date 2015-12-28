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

thankyou_template = head + """
<h1> Thanks you, done!</h1>
<a href="/MyProfile"> click here to go to your profile! </a>
<P> You could of course also go back <a href="/Home">Home</a>.

<p>
Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer tincidunt
lobortis tortor. Vestibulum urna. In lorem. Phasellus ornare ornare risus.
Duis tristique semper urna. Integer a nisi aliquam purus gravida bibendum.
Morbi sit amet purus at risus mollis semper. Aliquam tempor orci sed urna.
Curabitur sit amet velit at lacus egestas aliquam. Aenean vel eros. Aliquam
erat volutpat. Integer tempus molestie purus.
</p>
<p>
In pulvinar neque sit amet diam. Integer ultrices, quam non egestas
pharetra, ipsum eros rhoncus diam, ac rutrum lectus erat sit amet sem.
Curabitur tempus dignissim leo. In vitae augue non quam aliquet
sollicitudin. Class aptent taciti sociosqu ad litora torquent per conubia
nostra, per inceptos himenaeos. Vivamus nec ante. Praesent mauris. Integer
at orci eu lorem laoreet tempus. Cum sociis natoque penatibus et magnis dis
parturient montes, nascetur ridiculus mus. Sed neque leo, luctus eu,
pulvinar vel, venenatis vitae, ipsum. Donec eget arcu vitae lorem porttitor
volutpat. Donec vel nulla. Nullam venenatis, ipsum non scelerisque egestas,
erat eros rutrum turpis, in egestas libero quam in enim. Mauris faucibus,
tellus sit amet pretium molestie, metus tortor congue arcu, non fermentum
ipsum metus at leo.
</p>
<p>
Nunc eleifend, nunc eu ultricies sodales, nunc dui aliquam massa, vel luctus
ligula ligula eu ipsum. Curabitur vulputate interdum justo. Ut urna mauris,
pharetra ut, posuere quis, sollicitudin ac, sapien. Nullam at tellus eget
erat malesuada posuere. Vestibulum aliquet nulla at enim. Quisque at diam.
Proin lectus velit, venenatis in, porta vitae, malesuada ut, dui. Sed et
felis. Nunc laoreet mauris tristique neque. Quisque adipiscing condimentum
diam. Nam enim nisi, condimentum vel, viverra at, congue id, felis. Aliquam
tincidunt neque at felis. Etiam eros turpis, convallis at, ultricies sed,
sagittis ac, turpis. Aenean sollicitudin dui id eros suscipit malesuada.
Mauris condimentum gravida massa. Vivamus eu odio id dolor congue dapibus.
Phasellus lobortis, neque nec porta feugiat, lectus sapien vulputate quam,
eget varius metus mauris et ipsum. Ut in nibh vel augue lacinia dignissim.
Integer mattis tortor quis massa lacinia aliquet.
</p>
<p>
Pellentesque enim velit, mattis et, tristique quis, vulputate quis, massa.
Vestibulum diam odio, malesuada vel, venenatis id, facilisis quis, nunc.
Vivamus ornare fringilla nisi. Pellentesque erat magna, lacinia vel, cursus
ut, suscipit sed, nibh. Quisque cursus dignissim risus. In in justo in pede
eleifend aliquet. Ut ultricies rhoncus tellus. In ullamcorper. Phasellus
iaculis tempus mauris. Praesent congue enim. Integer a orci in orci
scelerisque suscipit. Fusce rhoncus, dolor et mattis faucibus, tortor tortor
eleifend ipsum, in dapibus risus nisi vel mi. Nam odio erat, placerat id,
lacinia at, congue eu, odio. Integer at dui et urna congue tempus.
Pellentesque iaculis dictum dolor. Curabitur quis ante.
</p>
<p>
Vestibulum non massa et elit mollis accumsan. Praesent consequat lorem sit
amet urna. Nunc non nulla vitae libero vehicula adipiscing. Pellentesque est
risus, adipiscing non, imperdiet eget, fringilla sit amet, leo. Nullam
vulputate, justo a sollicitudin dapibus, dolor nisi elementum ante, eget
dignissim nulla quam in sem. Cras tempor. Pellentesque laoreet. Nulla vel
justo a pede rutrum posuere. Nunc eget lorem. Pellentesque habitant morbi
tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum
rhoncus magna. In ac purus. Donec ac arcu vitae turpis facilisis commodo.
Nam vitae ligula. In hac habitasse platea dictumst. Maecenas id sapien eu
magna posuere commodo.
</p>
<p>
Fusce consectetuer varius lectus. Integer porttitor. Maecenas eleifend
accumsan nisi. Aliquam dictum. Integer magna quam, tincidunt at, tincidunt
sed, dictum quis, nisi. Duis molestie justo at tellus. Nam eget enim ut quam
porttitor consectetuer. Duis porttitor ultricies augue. Curabitur auctor.
Aenean malesuada. Cras interdum pede euismod velit. Phasellus pharetra
ullamcorper lacus. Nunc volutpat sodales erat. Proin dignissim, turpis vitae
interdum suscipit, felis felis consequat lorem, pretium elementum tellus
ipsum a velit. Nullam ac lorem. Class aptent taciti sociosqu ad litora
torquent per conubia nostra, per inceptos himenaeos. Fusce nec orci nec enim
tristique mollis.
</p>
<p>
Etiam fringilla nisl ac nunc. Phasellus tempus tristique est. Nulla
facilisi. In hac habitasse platea dictumst. Proin suscipit. Praesent sed
ante. Aenean convallis. Nullam congue est sed massa. Phasellus leo diam,
pulvinar quis, condimentum vitae, suscipit vitae, tellus. Donec bibendum dui
non eros.
</p>
<p>
Suspendisse cursus augue id diam. Mauris in urna sit amet libero sodales
lobortis. Aliquam accumsan pretium mauris. Duis nec turpis vitae dolor
sollicitudin hendrerit. Nullam fringilla lobortis orci. Duis pellentesque
nibh sit amet enim. Integer lacinia posuere ipsum. Proin accumsan. Proin
risus dolor, venenatis quis, blandit ac, sodales at, erat. Phasellus
scelerisque tempor felis. Mauris ut leo vel risus vestibulum mattis. Etiam
urna.
</p>
<p>
Integer vitae elit interdum pede laoreet lacinia. Morbi varius euismod eros.
Suspendisse potenti. Cras viverra facilisis justo. Donec ut ipsum pharetra
odio tristique lobortis. In molestie. Donec vitae turpis. Nam eu orci sit
amet risus semper lobortis. Praesent cursus risus ac sem. Lorem ipsum dolor
sit amet, consectetuer adipiscing elit. Vestibulum posuere fringilla justo.
Pellentesque suscipit urna a justo. Duis vulputate massa ut odio. Duis
blandit nulla sed sapien.
</p>
<p>
Praesent id nibh sit amet neque vestibulum hendrerit. Sed a massa. Lorem
ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur tristique quam
quis libero. Mauris fermentum ullamcorper tellus. Praesent in turpis non dui
imperdiet bibendum. Nam orci. Aenean sed metus sed odio pulvinar faucibus.
Proin tortor. Mauris urna. Proin sit amet tellus. Class aptent taciti
sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nunc
tincidunt mi et metus. Aenean eget nisi. Suspendisse nec dolor quis nibh
laoreet semper. Quisque malesuada, orci consequat faucibus laoreet, nibh
diam accumsan dui, id mollis est lectus vitae nibh. Sed tristique est non
turpis.
</p>
""" + foot
