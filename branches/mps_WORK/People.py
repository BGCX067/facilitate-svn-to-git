#!/usr/bin/env python

from Cheetah.Template import Template
from model.Record import EntitySet

PeopleDatabase = EntitySet("people", "personid")

#
# Map web request to data layer
#

def make_person(stem="form", **argd):
    new_person = {
        "person" : argd.get(stem + ".person",""),
        "house" : argd.get(stem + ".house",""),
        "street" : argd.get(stem + ".street",""),
        "town": argd.get(stem + ".town",""),
        "county": argd.get(stem + ".county",""),
        "postcode": argd.get(stem + ".postcode",""),
        "phone" : argd.get(stem + ".phone",""),
    }
    new_person = PeopleDatabase.new_record(new_person)
    return new_person

#
# Map web request to data layer
#

def update_person(stem="form", **argd):
    the_person = {
        "personid" : argd.get(stem + ".personid",""),
        "person" : argd.get(stem + ".person",""),
        "house" : argd.get(stem + ".house",""),
        "street" : argd.get(stem + ".street",""),
        "town": argd.get(stem + ".town",""),
        "county": argd.get(stem + ".county",""),
        "postcode": argd.get(stem + ".postcode",""),
        "phone" : argd.get(stem + ".phone",""),
    }
    PeopleDatabase.store_record(the_person)
    return the_person



class RecordRender(object):
    record_listview_template = 'templates/People.View.tmpl'
    record_editget_template = 'templates/Person.Edit.tmpl'
    record_view_template = 'templates/Person.View.tmpl'
    record_editpost_template = 'templates/Form.tmpl'         # Actually to do with a configured form isn't it...
    page_template = 'templates/Page.tmpl'

    def __init__(self, environ):
        self.environ = environ

    def rendered_record_list(self, people):
        people = Template ( file = self.record_listview_template,
                            searchList = [self.environ, {"people": people}] )
        return people

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



#
# Actually _Person_ Life Cycle Logic
#

def page_render_html(json, **argd):
    action = argd.get("formtype","overview")
    R = RecordRender(argd["__environ__"])
    DB = PeopleDatabase

    if action == "overview":
        # Show the database & a few options
        records = DB.read_database()
        rendered_records = R.rendered_record_list(records)
        return R.render_page(content=rendered_records)

    if action == "view":
        # Show the database & a few options
        record = DB.get_record(argd["personid"])
        records = DB.read_database()
        rendered_records                = R.rendered_record_list(records)
        rendered_record = R.rendered_record(record)

        return R.render_page(content=rendered_records, dataentry=rendered_record)

    if action == "edit_new":
        # Show the database & a form for creating a new person
        records = DB.read_database()
        rendered_records           = R.rendered_record_list(records)
        empty_data_entry = R.rendered_record_entry_form({})
        configured_form  = R.render_configured_form(empty_data_entry)

        return R.render_page(content=rendered_records, dataentry=configured_form)

    if action == "create_new":
        # Take the data sent to us, and use that to fill out an edit form
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        new_record = make_person(stem="form", **argd) # This also stores them in the database

        records = DB.read_database()
        rendered_records                = R.rendered_record_list(records)
        pre_filled_data_entry = R.rendered_record_entry_form(new_record)
        configured_form       = R.render_configured_form(pre_filled_data_entry, nextstep="update")

        return R.render_page(content=rendered_records, dataentry=configured_form)

    if action == "edit":
        record = DB.get_record(argd["personid"])

        records = DB.read_database()
        rendered_records                = R.rendered_record_list(records)
        pre_filled_data_entry = R.rendered_record_entry_form(record)
        configured_form       = R.render_configured_form(pre_filled_data_entry, nextstep="update")

        return R.render_page(content=rendered_records, dataentry=configured_form)

    if action == "update":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        record = update_person(stem="form", **argd)

        records = DB.read_database()
        rendered_records                = R.rendered_record_list(records)
        pre_filled_data_entry = R.rendered_record_entry_form(record)
        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                                            nextstep="update",
                                                                            submitlabel="Update"
                                        )

        return R.render_page(content=rendered_records, dataentry=configured_form)

    if action == "delete":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        # Show the database & a few options
        person = DB.get_record(argd["personid"])
        people = DB.read_database()
        rendered_people                = R.rendered_record_list(people)
        rendered_person = R.rendered_record(person)
        rendered_person = "<h3> Are you sure you wish to delete this person?</h3><ul>" + str(rendered_person)

        delete_action = "<a href='/cgi-bin/app/people?formtype=confirm_delete&personid=%s'>%s</a>" % (person["personid"], "Delete this person")
        cancel_action = "<a href='/cgi-bin/app/people?formtype=view&personid=%s'>%s</a>" % (person["personid"], "Cancel deletion")
        rendered_person += "</ul><h3> %s | %s </h3>" % (delete_action, cancel_action)

        return R.render_page(content=rendered_people, dataentry=rendered_person)

    if action == "confirm_delete":
        # Show the database & a few options
        record = DB.get_record(argd["personid"])
        DB.delete_record(argd["personid"])

        records = DB.read_database()
        rendered_records          = R.rendered_record_list(records)
#        rendered_record = R.rendered_record(record)

        return R.render_page(content=rendered_records, dataentry="<h1> %s Deleted </h1>" % record["person"])


    return str(Template ( file = 'templates/Page.tmpl', 
                         searchList = [
                              argd["__environ__"],
                              {
                                "extra": "" ,
                                "content" : "Sorry, got no idea what you want!",
                                "dataentry" : "",
                                "banner" : "Not found", # should send back a 404 status then? Or similar?
                              }
                          ] ))

if __name__ == "__main__":

    print "Content-Type: text/html"
    print

    print page_render_html({})
