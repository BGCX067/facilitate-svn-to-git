#!/usr/bin/env python

from Cheetah.Template import Template
from model.Record import EntitySet
import os,time

UsersDatabase = EntitySet("users",key="userid")des

def store_new_user(the_user): return UsersDatabase.new_record(the_user)
def read_database(): return UsersDatabase.read_database()
def store_user(user): return UsersDatabase.store_record(user)
def get_user(user): return UsersDatabase.get_record(user)
def delete_user(user): return UsersDatabase.delete_record(user)


#
# Map web request to data layer
#

def make_user_unique(fields = [], stem="form", **argd):
    if  fields==[]:
        make_user(stem="form", **argd)
    else:        
        new_vals = {}
        for field in fields:
            new_vals[field] = argd.get("form."+field) 
        users = read_database()
        if not users:
            os.sys.stderr.write("new user empty db+++++++++++++++++++++++++\n")
            return make_user(stem="form", **argd)
        for user in users:            
            for field in fields:
                if new_vals[field] == user[field]:
                    os.sys.stderr.write("no new user +++++++++++++++++++++++++\n")
                    return None
        os.sys.stderr.write("new user unique new+++++++++++++++++++++++++\n")
        return make_user(stem="form", **argd)

def make_user(stem="form", **argd):
    new_user = {
        "username"    : argd.get(stem + ".username",""),
        "loggedin"    : argd.get(stem + ".loggedin","pending"), # we create the user in the pending | loggedoff  state ?
        "useremail"   : argd.get(stem + ".useremail",""),
        "emailhash"   : argd.get(stem + ".useremail",""),
        "password"    : argd.get(stem + ".password",""),
        "duppassword" : argd.get(stem + ".duppassword",""),
        "triedlogin"  : argd.get(stem + ".triedlogin","0"),
        "personid"    : argd.get(stem + ".personid",""),        # a user is a person?
    }
    new_user = store_new_user(new_user)
    return new_user

#
# Map web request to data layer
#

def update_user(stem="form", **argd):
    the_user = {
        "userid"      : argd.get(stem + ".userid",""),
        "username"    : argd.get(stem + ".username",""),
        "loggedin"    : argd.get(stem + ".loggedin",""),      # state = "yes", "no", "pending"
        "useremail"   : argd.get(stem + ".useremail",""),
        "password"    : argd.get(stem + ".password",""),
        "duppassword" : argd.get(stem + ".duppassword",""),
        "triedlogin"  : argd.get(stem + ".triedlogin",""),
        "personid"    : argd.get(stem + ".personid",""),      # a user is a person?
    }
    store_user(the_user)
    return the_user

def dummy_user(stem="form", **argd):                       # a blank user to pass around
    the_user = {
        "username"    : argd.get(stem + ".username",""),
        "loggedin"    : argd.get(stem + ".loggedin","no"),    # state = "yes", "no", "pending"
        "password"    :  argd.get(stem + ".password",""),
        "duppassword" :  argd.get(stem + ".duppassword",""),
        "useremail"   :  argd.get(stem + ".useremail",""),
        "triedlogin"  :   argd.get(stem + ".triedlogin",""), 
        "personid"    : argd.get(stem + ".personid",""),      # a user is a person?
    }
    return the_user

def validate_email(address): #a rudimentary parse to check structure is name@somewhere.somedomain at least 
    return True

def indb(value,field,db):
    for item in db:
        if item[field] == value:
            return True

class RecordRender(object):
    record_listview_template = 'templates/Users.View.tmpl'
    record_editget_template = 'templates/User.Edit.tmpl'
    record_userpending_template = 'templates/User.Pending.tmpl'
    record_view_template = 'templates/User.View.tmpl'
    record_user_login_template = 'templates/User.Login.tmpl'
    record_editpost_template = 'templates/Form.tmpl'         # Actually to do with a configured form isn't it...
    record_forgotpw_template = 'templates/User.ForgotPW.tmpl'
    page_template = 'templates/UserPage.tmpl'

    def __init__(self, environ,**argd):
        self.environ = environ
        self.__dict__.update(argd)

    def rendered_record_list(self, addresses):
        users = Template ( file = self.record_listview_template,
                            searchList = [self.environ, {"users": addresses}] )
        return users

    def rendered_record_entry_form(self, item):
        dataentry = Template ( file = self.record_editget_template,
                               searchList = [self.environ, item] )
        return dataentry

    def rendered_record_userpending_form(self,item):
        dataentry = Template ( file = self.record_userpending_template,
                               searchList = [self.environ, item] )
        return dataentry


    def rendered_record_userforgotpw_form(self,item):
        dataentry = Template ( file = self.record_forgotpw_template,
                               searchList = [self.environ, item] )
        return dataentry


    def rendered_user_login_form(self, item):
        dataentry = Template ( file = self.record_user_login_template,
                               searchList = [self.environ, item] )
        return dataentry
#   may not be required we'll see
#    def render_configred_user_login_form(self, pre_filled_data_entry,
#                               nextstep="user_verify",
#                               submitlabel="Login"):
#
#        configured_form = Template ( file = self.record_editpost_template,
#                                     searchList = [
#                                         self.environ, {
#                                           "formbody":pre_filled_data_entry,
#                                           "formtype":nextstep,
#                                           "submitlabel": submitlabel,
#                                                  }]
#                                   )
#        return configured_form



    def rendered_record(self, item):
        dataentry = Template ( file = self.record_view_template,
                               searchList = [self.environ, item] )
        return dataentry

    def render_configured_form(self, pre_filled_data_entry,
                               nextstep="create_new",
                               submitlabel="Add Item"):

        configured_form = Template ( file = self.record_editpost_template,
                                     searchList = [
                                         self.environ, {
                                           "formbody":pre_filled_data_entry,
                                           "formtype":nextstep,
                                           "submitlabel": submitlabel,
                                                  }]
                                   )
        return configured_form

    def render_page(self, content="", extra="", dataentry=""):
        return str(Template ( file = self.page_template,
                             searchList = [
                                  self.environ,
                                  {
                                    "extra": extra ,
                                    "content" : content,
                                    "dataentry" : dataentry,
                                  }
                              ] ))

    def user_exists(self,username,password):
        users = read_database()
        if users:
            os.sys.stderr.write(" got userdb verifying+++++++++++++++++++++++++\n")
            for user in users:
                if password == user["password"]:
                    if username == user["username"]:
                        return user, True
                    else:
                        return None, True
                if username  == user["username"]:
                        return user, False
            return None, False
        else:
             return None, False

    def user_email_tx(self,emailaddress):
        time = time.time()
        emailhash=None
        return emailhash
                        
    def user_email_rx(self,emailhash,emailddress):
        return False
    

#
# Actually User Life Cycle Logic
#

def page_render_html(json, **argd):
    action = argd.get("formtype","overview")
    R = RecordRender(argd["__environ__"])
    if action == "overview":
        # Show the default page template and any other content 
        overview_content = "<B>  User Landing  </B>.  display some real content here  "
        return R.render_page(content=overview_content,extra={"user":"None"})

    if action == "user_login":
        this_user = dummy_user(stem="form", **argd) # may need to set userid and password before next if we get some persistence
        dummy_content = "<B> User Login Page </B>. get login details next state is user_verify "  # Real content is new template to get username and password
        pre_filled_data_entry = R.rendered_user_login_form(this_user)
                             
        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                        nextstep="user_verify",
                               submitlabel="Login"
                                                       )
        
        return R.render_page(content=dummy_content, dataentry=configured_form, extra={"user":"None"})

    if action == "user_verify":
        argh = argd.get("__environ__")
        os.sys.stderr.write(repr(argh))
        username = argd.get("form.username")
        password = argd.get("form.password")
        user, valid_password = R.user_exists(username, password)
        os.sys.stderr.write(repr(user)+repr(valid_password))  
        if user and valid_password==True:
            if user["loggedin"]=="pending":            # ***** tested       # test for registration email rx
                if R.user_email_rx(user["emailhash"],user["useremail"]):  
                    user["loggedin"] = "yes"
                    store_user(user)
                    verified_user_content = "<B>  User Verify  </B>. valid user update user record state,<p> user view to become restricted <p>This is UserPage.tmpl at present no restrictions"
                    return R.render_page(content=verified_user_content,extra={"user":"Good"})
                else:     
                    verified_user_content="<B>  User Verify  </B>. valid user verification email sent waiting response,<p> user view is restricted <p>This is  UserPage.tmpl at present no view at all"    
                    return R.render_page(content=verified_user_content,extra={"user":"Pending"})
            else:  # ***** tested  
                user["loggedin"] = "yes"
                store_user(user)
                verified_user_content = "<B>  User Verify  </B>.  valid user updated user record state,<p> user view to become restricted <p>This is  UserPage.tmpl at present no restrictions"
                return R.render_page(content=verified_user_content,extra={"user":"Good"})
        elif user:  # ***** tested 
           # if cnt < 2  # if valid user name + bad password two tries then throw to resend password
             verified_user_content = "<B>  User Verify  </B>.  valid user name wrong password next state is forgot password render User.ForgotPW.tmpl"
             pre_filled_data_entry = R.rendered_record_userforgotpw_form(user)
             configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="user_verify",
                                                       )
             return R.render_page(content=verified_user_content,extra={"user":"Bad"})
           # else bad password
        else:       # ***** tested 
             overview_content = "<B> Bad User and Password    </B>.  display some real content here  "
             return R.render_page(content=overview_content,extra={"user":"None"})

    if action == "user_register":           # c.f. create new_item 
        # Take the data sent to us, and use that to fill out an edit form
        # Note: We create the user here in state pending the next state validates
        # The user cannot edit the page yet
        dummy_content = "<B> User Create New</B>. Create new  user in state pending "
        #new_user = make_user(stem="form", **argd) # create the new user here and also store them in the database then this or
        #the_user = {"username":new_user["username"],"useremail":new_user["useremail"],"password":"","duppassword":""}# new_user["useremail"]}
        the_user = dummy_user() # create a dummy here and spin on next state if not password match or valid email        
        pre_filled_data_entry = R.rendered_record_userpending_form(the_user)
        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="user_validate",
                                                       submitlabel="Register",
                                                       )
        return R.render_page(content=configured_form  ,extra={"user":"None"})

    if action == "user_validate":
        users = read_database()
         #new_user = make_user_unique(fields=["username",],stem="form", **argd)
         #os.sys.stderr.write(str(new_user)+"****************************new_user\n")
        if not indb(argd.get("form.username"),"username",users): # spin here untill passwords match and valid email represent the pending form 
           if argd.get("form.password") != argd.get("form.duppassword") or not validate_email(argd.get("form.useremail")):
               # cf empty_data_entry = R.rendered_record_entry_form({})
               # cf configured_form  = R.render_configured_form(empty_data_entry)
               empty_data_entry = R.rendered_record_userpending_form({"user":"pending"})
               configured_form       = R.render_configured_form(empty_data_entry,
                                                       nextstep="user_validate",
                                                       submitlabel="Register",
                                                       )
               #dummy_content = "<B> Validate New  </B>.  user_pending re-submit passwords" 
               return R.render_page(content=configured_form  ,extra={"user":"None"})
           else:  # New user pending reciept of email 
               new_user = make_user_unique(fields=["username",],stem="form", **argd)
    
           pre_filled_data_entry = R.rendered_record_userpending_form({"user":"pending"})                        
               configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="user_verify",
                                                       submitlabel="Register",
                                                       )
               dummy_content = "<B> Validate New  </B>.  user_pending email sent" 
               #return R.render_page(content=dummy_content, extra={"user":"Pending"})
               #return R.render_page(content=configured_form  ,extra={"user":"Pending"}) # fix this
               return R.render_page(content=pre_filled_data_entry ,extra={"user":"Pending"})
          
        else:      # No new user need valid user name
            dummy_content = "<B> Invalid Username </B>. please try again "           
           # next step is registration page with 
            return R.render_page(content=dummy_content,extra={"user":"None"})

    if action == "user_logout":
        dummy_content = "<B> Logout Page </B> if logout update user record  next state is user greet"
        return R.render_page(content=dummy_content,extra={"user":"None"})

    if action == "user_lostpassword":
        dummy_content = "<B> User lost password  </B>. user enters email ddress if valid send login else register new "
        return R.render_page(content=dummy_content)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #   
    if action == "user_challenge":        # This and the one above identical?
        dummy_content = "<B> User Challenge </B>. if lost password/username  next state is user_lost_password else user_create_new else bog off"  
        return R.render_page(content=dummy_content)

    if action == "user_view":             # prollu not needed same as overview keep hanging around for now 
        dummy_content = "<B> User View </B>. whatever this user can view or edit determined by owns and can view relations"
        return R.render_page(content=dummy_content)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  
    
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 #                     original ms users below here                       #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    if action == "edit_new":
        # Show the database & a form for creating a new user
        addresses = read_database()
        users           = R.rendered_record_list(addresses)
        empty_data_entry = R.rendered_record_entry_form({})
        configured_form  = R.render_configured_form(empty_data_entry)

        return R.render_page(content=users, dataentry=configured_form)

    if action == "create_new":
        # Take the data sent to us, and use that to fill out an edit form
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        new_user = make_user(stem="form", **argd) # This also stores them in the database

        addresses = read_database()
        users                = R.rendered_record_list(addresses)
        pre_filled_data_entry = R.rendered_record_entry_form(new_user)
        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="update_user",
                                                       )
        return R.render_page(content=users, dataentry=configured_form)

    if action == "view_user":
        # Show the database & a few options
        user = get_user(argd["userid"])
        addresses = read_database()
        users                = R.rendered_record_list(addresses)
        user_rendered = R.rendered_record(user)

        return R.render_page(content=users, dataentry=user_rendered)

    if action == "edit_user":
        user = get_user(argd["userid"])

        addresses = read_database()
        users                = R.rendered_record_list(addresses)
        pre_filled_data_entry = R.rendered_record_entry_form(user)
        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="update_user",
                                                       )
        return R.render_page(content=users, dataentry=configured_form)

    if action == "update_user":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        theuser = update_user(stem="form", **argd)

        addresses = read_database()
        users                = R.rendered_record_list(addresses)
        pre_filled_data_entry = R.rendered_record_entry_form(theuser)
        configured_form       = R.render_configured_form(pre_filled_data_entry,nextstep="update_user")

        return R.render_page(content=users, dataentry=configured_form)

    if action == "delete_user":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        # Show the database & a few options
        user = get_user(argd["userid"])
        addresses = read_database()
        users                = R.rendered_record_list(addresses)
        user_rendered = R.rendered_record(user)
        user_rendered = "<h3> Are you sure you wish to delete this user?</h3><ul>" + str(user_rendered)

        delete_action = "<a href='/cgi-bin/app/users?formtype=confirm_delete_user&userid=%s'>%s</a>" % (user["userid"], "Delete this user")
        cancel_action = "<a href='/cgi-bin/app/users?formtype=view_user&userid=%s'>%s</a>" % (user["userid"], "Cancel deletion")
        user_rendered += "</ul><h3> %s | %s </h3>" % (delete_action, cancel_action)

        return R.render_page(content=users, dataentry=user_rendered)

    if action == "confirm_delete_user":
        # Show the database & a few options
        user = get_user(argd["userid"])
        delete_user(argd["userid"])

        addresses = read_database()
        users          = R.rendered_record_list(addresses)
        user_rendered = R.rendered_record(user)

        return R.render_page(content=users, dataentry="<h1> %s Deleted </h1>" % user["user"])


    return str(Template ( file = 'templates/Page.tmpl', 
                         searchList = [
                            argd["__environ__"],
                              {
                                "extra": "" ,
                                "content" : "Sorry, got no idea what you're on!",
                                "dataentry" : "",
                                "banner" : "Not found", # should send back a 404 status then? Or similar?
                              }
                          ] ))

if __name__ == "__main__":

    print "Content-Type: text/html"
    print

    print page_render_html({})
