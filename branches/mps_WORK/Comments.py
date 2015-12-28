#!/usr/bin/env python
import os 
from Cheetah.Template import Template
from model.Record import EntitySet

CommentDatabase = EntitySet("comments",key="commentid")

def store_new_comment(the_comment): return CommentDatabase.new_record(the_comment)
def read_database(): return CommentDatabase.read_database()
def store_comment(comment): return CommentDatabase.store_record(comment)
def get_comment(comment): return CommentDatabase.get_record(comment)
def delete_person(comment): return CommentDatabase.delete_record(comment)

# #
# # Map web request to data layer
# #

def make_comment(stem="form", **argd):
    new_comment = {
        "comment" : argd.get(stem + ".comment",""),
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
        "id" : argd.get(stem + ".commentid",""),
        "comment" : argd.get(stem + ".comment",""),
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
    record_listview_template = 'templates/Comments.View.tmpl'
    record_editget_template = 'templates/Comment.Edit.tmpl'
    record_view_template = 'templates/Comment.View.tmpl'
    record_editpost_template = 'templates/Form.tmpl'         # Actually to do with a configured form isn't it...
    page_template = 'templates/Page.tmpl'

    def __init__(self, environ):
        self.environ = environ

    def rendered_record_list(self, comments):
        rendered_comments = Template ( file = self.record_listview_template,
		                            searchList = [self.environ, {"comments": comments} ])
        return rendered_comments

    def render_page(self, content="", extra="", dataentry=""):
         return str(Template ( file = self.page_template,
                  searchList = [
                        self.environ, {
									"extra": extra,
									"content" :  content, # "",#
									"dataentry" : dataentry,
									}
								]
								))
								
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
        comments = read_database()
        rendered_comments = R.rendered_record_list(comments)
        return R.render_page(content=rendered_comments)

        #os.sys.stderr.write(str(comments))
        #os.sys.stderr.write(str(comments_list))
        #txt=  R.render_page(content=comments)
        #os.sys.stderr.write(txt)

    if action == "edit_new_comment":
        # Show the database & a form for creating a new person
        comments = read_database()
        redered_comments           = R.rendered_record_list(comments)
        empty_data_entry = R.rendered_record_entry_form({})
        configured_form  = R.render_configured_form(empty_data_entry)

        return R.render_page(content=redered_comments, dataentry=configured_form)

    if action == "create_new":
        # Take the data sent to us, and use that to fill out an edit form
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        new_comment = make_comment(stem="form", **argd) # This also stores them in the database

        comments = read_database()
        redered_comments                = R.rendered_record_list(comments)
        pre_filled_data_entry = R.rendered_record_entry_form(new_comment)
        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="update_comment",
                                                       )
        return R.render_page(content=redered_comments, dataentry=configured_form)

    if action == "view_comment":
        # Show the database & a few options
        comment = get_comment(argd["commentid"])
        comments = read_database()
        redered_commments                = R.rendered_record_list(comments)
        rendered_comment = R.rendered_record(comment)

        return R.render_page(content=rendered_comments, dataentry=rendered_comment)

#     if action == "edit_person":
#         person = get_person(argd["personid"])

#         addresses = read_database()
#         people                = R.rendered_record_list(addresses)
#         pre_filled_data_entry = R.rendered_record_entry_form(person)
#         configured_form       = R.render_configured_form(pre_filled_data_entry,
#                                                        nextstep="update_person",
#                                                        )
#         return R.render_page(content=people, dataentry=configured_form)

#     if action == "update_person":
#         # Take the data sent to us, and use that to fill out an edit form
#         #
#         # Note: This is actually filling in an *edit* form at that point, not a *new* user form
#         # If they submit the new form, the surely they should be viewed to be updating the form?
#         # yes...
#         #
#         theperson = update_person(stem="form", **argd)

#         addresses = read_database()
#         people                = R.rendered_record_list(addresses)
#         pre_filled_data_entry = R.rendered_record_entry_form(theperson)
#         configured_form       = R.render_configured_form(pre_filled_data_entry,nextstep="update_person")

#         return R.render_page(content=people, dataentry=configured_form)

#     if action == "delete_person":
#         # Take the data sent to us, and use that to fill out an edit form
#         #
#         # Note: This is actually filling in an *edit* form at that point, not a *new* user form
#         # If they submit the new form, the surely they should be viewed to be updating the form?
#         # yes...
#         #
#         # Show the database & a few options
#         person = get_person(argd["personid"])
#         addresses = read_database()
#         people                = R.rendered_record_list(addresses)
#         person_rendered = R.rendered_record(person)
#         person_rendered = "<h3> Are you sure you wish to delete this person?</h3><ul>" + str(person_rendered)

#         delete_action = "<a href='/cgi-bin/app/people?formtype=confirm_delete_person&personid=%s'>%s</a>" % (person["personid"], "Delete this person")
#         cancel_action = "<a href='/cgi-bin/app/people?formtype=view_person&personid=%s'>%s</a>" % (person["personid"], "Cancel deletion")
#         person_rendered += "</ul><h3> %s | %s </h3>" % (delete_action, cancel_action)

#         return R.render_page(content=people, dataentry=person_rendered)

#     if action == "confirm_delete_person":
#         # Show the database & a few options
#         person = get_person(argd["personid"])
#         delete_person(argd["personid"])

#         addresses = read_database()
#         people          = R.rendered_record_list(addresses)
#         person_rendered = R.rendered_record(person)

#         return R.render_page(content=people, dataentry="<h1> %s Deleted </h1>" % person["person"])


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
