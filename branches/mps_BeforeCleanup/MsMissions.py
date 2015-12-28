#!/usr/bin/env python

from Cheetah.Template import Template
from model.Record import EntitySet

MsMissionsDatabase = EntitySet("msmissions",key="msmissionid")

def store_new_msmission(the_msmission): return MsMissionsDatabase.new_record(the_msmission)
def read_database(): return MsMissionsDatabase.read_database()
def store_msmission(msmission): return MsMissionsDatabase.store_record(msmission)
def get_msmission(msmission): return MsMissionsDatabase.get_record(msmission)
def delete_msmission(msmission): return MsMissionsDatabase.delete_record(msmission)

#
# Map web request to data layer
#

def make_msmission(stem="form", **argd):
    new_msmission = {
        "msmission" : argd.get(stem + ".msmission",""),
        "shortdescription" : argd.get(stem + ".shortdescription",""),
        "mediumdescription" : argd.get(stem + ".mediumdescription",""),
        "longdescription": argd.get(stem + ".longdescription",""),
        "basemsmission": argd.get(stem + ".basemsmission",""),
    }
    new_msmission = store_new_msmission(new_msmission)
    return new_msmission

#
# Map web request to data layer
#

def update_msmission(stem="form", **argd):
    the_msmission = {
        "msmissionid" : argd.get(stem + ".msmissionid",""),
        "msmission" : argd.get(stem + ".msmission",""),
        "shortdescription" : argd.get(stem + ".shortdescription",""),
        "mediumdescription" : argd.get(stem + ".mediumdescription",""),
        "longdescription": argd.get(stem + ".longdescription",""),
        "basemsmission": argd.get(stem + ".basemsmission",""),
    }
    store_msmission(the_msmission)
    return the_msmission



class RecordRender(object):
    record_listview_template = 'templates/MsMissions.View.tmpl'
    record_editget_template = 'templates/MsMission.Edit.tmpl'
    record_view_template = 'templates/MsMission.View.tmpl'
    record_editpost_template = 'templates/Form.tmpl'         # Actually to do with a configured form isn't it...
    page_template = 'templates/Page.tmpl'

    def __init__(self, environ,**argd):
        self.environ = environ
        self.__dict__.update(argd)

    def rendered_record_list(self, addresses):
        msmissions = Template ( file = self.record_listview_template,
                            searchList = [self.environ, {"msmissions": addresses}] )
        return msmissions

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
# Actually _MsMission_ Life Cycle Logic
#

def page_render_html(json, **argd):
    action = argd.get("formtype","overview")
    R = RecordRender(argd["__environ__"])
    if action == "overview":
        # Show the database & a few options
        addresses = read_database()
        msmissions                = R.rendered_record_list(addresses)
        return R.render_page(content=msmissions)

    if action == "edit_new":
        # Show the database & a form for creating a new msmission
        addresses = read_database()
        msmissions           = R.rendered_record_list(addresses)
        empty_data_entry = R.rendered_record_entry_form({})
        configured_form  = R.render_configured_form(empty_data_entry)

        return R.render_page(content=msmissions, dataentry=configured_form)

    if action == "create_new":
        # Take the data sent to us, and use that to fill out an edit form
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        new_msmission = make_msmission(stem="form", **argd) # This also stores them in the database

        addresses = read_database()
        msmissions                = R.rendered_record_list(addresses)
        pre_filled_data_entry = R.rendered_record_entry_form(new_msmission)
        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="update_msmission",
                                                       )
        return R.render_page(content=msmissions, dataentry=configured_form)

    if action == "view_msmission":
        # Show the database & a few options
        msmission = get_msmission(argd["msmissionid"])
        addresses = read_database()
        msmissions                = R.rendered_record_list(addresses)
        msmission_rendered = R.rendered_record(msmission)

        return R.render_page(content=msmissions, dataentry=msmission_rendered)

    if action == "edit_msmission":
        msmission = get_msmission(argd["msmissionid"])

        addresses = read_database()
        msmissions                = R.rendered_record_list(addresses)
        pre_filled_data_entry = R.rendered_record_entry_form(msmission)
        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="update_msmission",
                                                       )
        return R.render_page(content=msmissions, dataentry=configured_form)

    if action == "update_msmission":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        themsmission = update_msmission(stem="form", **argd)

        addresses = read_database()
        msmissions                = R.rendered_record_list(addresses)
        pre_filled_data_entry = R.rendered_record_entry_form(themsmission)
        configured_form       = R.render_configured_form(pre_filled_data_entry,nextstep="update_msmission")

        return R.render_page(content=msmissions, dataentry=configured_form)

    if action == "delete_msmission":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        # Show the database & a few options
        msmission = get_msmission(argd["msmissionid"])
        addresses = read_database()
        msmissions                = R.rendered_record_list(addresses)
        msmission_rendered = R.rendered_record(msmission)
        msmission_rendered = "<h3> Are you sure you wish to delete this msmission?</h3><ul>" + str(msmission_rendered)

        delete_action = "<a href='/cgi-bin/app/msmissions?formtype=confirm_delete_msmission&msmissionid=%s'>%s</a>" % (msmission["msmissionid"], "Delete this msmission")
        cancel_action = "<a href='/cgi-bin/app/msmissions?formtype=view_msmission&msmissionid=%s'>%s</a>" % (msmission["msmissionid"], "Cancel deletion")
        msmission_rendered += "</ul><h3> %s | %s </h3>" % (delete_action, cancel_action)

        return R.render_page(content=msmissions, dataentry=msmission_rendered)

    if action == "confirm_delete_msmission":
        # Show the database & a few options
        msmission = get_msmission(argd["msmissionid"])
        delete_msmission(argd["msmissionid"])

        addresses = read_database()
        msmissions          = R.rendered_record_list(addresses)
        msmission_rendered = R.rendered_record(msmission)

        return R.render_page(content=msmissions, dataentry="<h1> %s Deleted </h1>" % msmission["msmission"])


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
