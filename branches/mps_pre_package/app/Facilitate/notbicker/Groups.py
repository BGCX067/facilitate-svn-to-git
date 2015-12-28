#!/usr/bin/env python
import os 
from Cheetah.Template import Template
from model.Record import EntitySet

CommentDatabase = EntitySet("groups",key="groupid")

def store_new_comment(the_comment): return CommentDatabase.new_record(the_comment)
def read_database(): return CommentDatabase.read_database()
def store_comment(comment): return CommentDatabase.store_record(comment)
def get_comment(comment): return CommentDatabase.get_record(comment)
def delete_comment(comment): return CommentDatabase.delete_record(comment)

# #
# # Map web request to data layer
# #



def make_comment(stem="form", **argd):
    new_comment = {
        "groupname" : argd.get(stem + ".groupname",""),
#         "house" : argd.get(stem + ".house",""),
#         "street" : argd.get(stem + ".street",""),
#         "town": argd.get(stem + ".town",""),
#         "county": argd.get(stem + ".county",""),
#         "postcode": argd.get(stem + ".postcode",""),
#         "phone" : argd.get(stem + ".phone",""),
    }
    new_comment = store_new_comment(new_comment)
    return new_comment

# #
# # Map web request to data layer
# #

def update_comment(stem="form", **argd):
    the_comment = {
        "groupid" : argd.get(stem + ".groupid",""),
        "groupname" : argd.get(stem + ".groupname",""),
#         "person" : argd.get(stem + ".person",""),
#         "house" : argd.get(stem + ".house",""),
#         "street" : argd.get(stem + ".street",""),
#         "town": argd.get(stem + ".town",""),
#         "county": argd.get(stem + ".county",""),
#         "postcode": argd.get(stem + ".postcode",""),
#         "phone" : argd.get(stem + ".phone",""),
    }
    store_comment(the_comment)
    return the_comment



class RecordRender(object):
    record_listview_template = 'templates/Groups.View.tmpl'
    record_editget_template = 'templates/Group.Edit.tmpl'
    record_view_template = 'templates/Group.View.tmpl'
    record_editpost_template = 'templates/Form.tmpl'         # Actually to do with a configured form isn't it...
    page_template = 'templates/Page.tmpl'

    def __init__(self, environ):
        self.environ = environ

    def rendered_record_list(self, groups):
        rendered_comments = Template ( file = self.record_listview_template,
		                            searchList = [self.environ, {"groups": groups} ])
        return rendered_comments

    def render_page(self, content="", extra="", dataentry=""):
         return str(Template ( file = self.page_template,
                  searchList = [
                        self.environ, {	"extra": extra,
                                         "content" : content, 
                                          "dataentry" : dataentry,}
								]))
								
    def rendered_record_entry_form(self, item):
        dataentry = Template ( file = self.record_editget_template,
                                searchList = [self.environ, item] )
        return dataentry

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
	
		                            


                



	
if 0:
     #
     # Presentation Layer - various aspects of complexity
     #

	def rendered_record_list(addresses):
		people = Template ( file = 'templates/People.View.tmpl',
                             searchList = [{"people" : addresses}] )
        return people

#     def rendered_record_entry_form(person):
#         dataentry = Template ( file = 'templates/Person.Edit.tmpl', searchList = [person] )
#         return dataentry

#     def rendered_person(person):
#         dataentry = Template ( file = 'templates/Person.View.tmpl', searchList = [person] )
#         return dataentry

#     def render_configured_form(pre_filled_data_entry,nextstep="create_new"):
#         configured_form = Template ( file = 'templates/Form.tmpl', 
#                                      searchList = [{
#                                            "formbody":pre_filled_data_entry,
#                                            "formtype":nextstep,
#                                                   }]
#                                    )
#         return configured_form
	
#	def render_page(content="", extra="", dataentry="", environ={}):
#		return str(Template ( file = 'templates/Page.tmpl',
#                             searchList = [
#                                  environ,
#                                  {
#                                    "extra": extra ,
#                                    "content" : content,
#                                    "dataentry" : dataentry,
#                                  }
#                              ] ))
#

#
# Actually _Person_ Life Cycle Logic
#

def page_render_html(json, **argd):
    action = argd.get("formtype","overview")
    R = RecordRender(argd["__environ__"])
    if action == "overview":
        # Show the database & a few options
        groups = read_database()
        rendered_groups = R.rendered_record_list(groups)
        return R.render_page(content=rendered_groups) 

        #os.sys.stderr.write(str(comments))
        #os.sys.stderr.write(str(comments_list))
        #txt=  R.render_page(content=comments)
        #os.sys.stderr.write(txt)

    if action == "edit_new":
        # Show the database & a form for creating a new person
        comments = read_database()
        rendered_comments = R.rendered_record_list(comments)
        empty_data_entry = R.rendered_record_entry_form({})
        configured_form  = R.render_configured_form(empty_data_entry)

        return R.render_page(content=rendered_comments, dataentry=configured_form)

    if action == "create_new":
        # Take the data sent to us, and use that to fill out an edit form
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        new_comment = make_comment(stem="form", **argd) # This also stores them in the database
        os.sys.stderr.write(argd.get("form.groupname"))
        comments = read_database()
        rendered_comments     = R.rendered_record_list(comments)
        pre_filled_data_entry = R.rendered_record_entry_form(new_comment)
        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="update_comment",
                                                       )
        return R.render_page(content=rendered_comments, dataentry=configured_form)

    if action == "view_comment":
        # Show the database & a few options
        comment = get_comment(argd["groupid"])
        comments = read_database()
        rendered_comments               = R.rendered_record_list(comments)
        rendered_comment = R.rendered_record(comment)

        return R.render_page(content=rendered_comments, dataentry=rendered_comment)

    if action == "edit_comment":
        comment = get_comment(argd["groupid"])

        comments = read_database()
        rendered_comments                = R.rendered_record_list(comments)
        pre_filled_data_entry = R.rendered_record_entry_form(comment)
        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="update_comment",
                                                       )
        return R.render_page(content=rendered_comments, dataentry=configured_form)

    if action == "update_comment":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        thecomment = update_comment(stem="form", **argd)

        comments = read_database()
        rendered_comments                = R.rendered_record_list(comments)
        pre_filled_data_entry = R.rendered_record_entry_form(thecomment)
        configured_form       = R.render_configured_form(pre_filled_data_entry,nextstep="update_comment")

        return R.render_page(content=rendered_comments, dataentry=configured_form)

    if action == "delete_comment":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        # Show the database & a few options
        comment = get_comment(argd["groupid"])
        comments = read_database()
        rendered_comments = R.rendered_record_list(comments)
        comment_rendered = R.rendered_record(comment)
        comment_rendered = "<h3> Are you sure you wish to delete this group?</h3><ul>" + str(comment_rendered)

        delete_action = "<a href='/cgi-bin/app/groups?formtype=confirm_delete_comment&groupid=%s'>%s</a>" % (comment["groupid"], "Delete this comment")
        cancel_action = "<a href='/cgi-bin/app/groups?formtype=view_comment&groupid=%s'>%s</a>" % (comment["groupid"], "Cancel deletion")
        comment_rendered += "</ul><h3> %s | %s </h3>" % (delete_action, cancel_action)

        return R.render_page(content=rendered_comments, dataentry=comment_rendered)

    if action == "confirm_delete_comment":
        # Show the database & a few options
        comment = get_comment(argd["groupid"])
        delete_comment(argd["groupid"])

        comments = read_database()
        rendered_comments          = R.rendered_record_list(comments)
        person_rendered = R.rendered_record(comment)

        return R.render_page(content=rendered_comments, dataentry="<h1> %s Deleted </h1>" % comment["groupid"])


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
