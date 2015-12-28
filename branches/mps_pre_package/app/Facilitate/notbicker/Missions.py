#!/usr/bin/env python

from Cheetah.Template import Template
from model.Record import EntitySet

MissionsDatabase = EntitySet("missions",key="missionid")

def store_new_mission(the_mission): return MissionsDatabase.new_record(the_mission)
def read_database(): return MissionsDatabase.read_database()
def store_mission(mission): return MissionsDatabase.store_record(mission)
def get_mission(mission): return MissionsDatabase.get_record(mission)
def delete_mission(mission): return MissionsDatabase.delete_record(mission)

#
# Map web request to data layer
#

def make_mission(stem="form", **argd):
    new_mission = {
        "mission" : argd.get(stem + ".mission",""),
        "shortdescription" : argd.get(stem + ".shortdescription",""),
        "mediumdescription" : argd.get(stem + ".mediumdescription",""),
        "longdescription": argd.get(stem + ".longdescription",""),
        "basemission": argd.get(stem + ".basemission",""),
    }
    new_mission = store_new_mission(new_mission)
    return new_mission

#
# Map web request to data layer
#

def update_mission(stem="form", **argd):
    the_mission = {
        "missionid" : argd.get(stem + ".missionid",""),
        "mission" : argd.get(stem + ".mission",""),
        "shortdescription" : argd.get(stem + ".shortdescription",""),
        "mediumdescription" : argd.get(stem + ".mediumdescription",""),
        "longdescription": argd.get(stem + ".longdescription",""),
        "basemission": argd.get(stem + ".basemission",""),
    }
    store_mission(the_mission)
    return the_mission



class RecordRender(object):
    record_listview_template = 'templates/Missions.View.tmpl'
    record_editget_template = 'templates/Mission.Edit.tmpl'
    record_view_template = 'templates/Mission.View.tmpl'
    record_editpost_template = 'templates/Form.tmpl'         # Actually to do with a configured form isn't it...
    page_template = 'templates/Page.tmpl'

    def __init__(self, environ,**argd):
        self.environ = environ
        self.__dict__.update(argd)

    def rendered_record_list(self, addresses):
        missions = Template ( file = self.record_listview_template,
                            searchList = [self.environ, {"missions": addresses}] )
        return missions

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
# Actually _Mission_ Life Cycle Logic
#

def page_render_html(json, **argd):
    action = argd.get("formtype","overview")
    R = RecordRender(argd["__environ__"])
    if action == "overview":
        # Show the database & a few options
        addresses = read_database()
        missions                = R.rendered_record_list(addresses)
        return R.render_page(content=missions)

    if action == "edit_new":
        # Show the database & a form for creating a new mission
        addresses = read_database()
        missions           = R.rendered_record_list(addresses)
        empty_data_entry = R.rendered_record_entry_form({})
        configured_form  = R.render_configured_form(empty_data_entry)

        return R.render_page(content=missions, dataentry=configured_form)

    if action == "create_new":
        # Take the data sent to us, and use that to fill out an edit form
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        new_mission = make_mission(stem="form", **argd) # This also stores them in the database

        addresses = read_database()
        missions                = R.rendered_record_list(addresses)
        pre_filled_data_entry = R.rendered_record_entry_form(new_mission)
        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="update_mission",
                                                       )
        return R.render_page(content=missions, dataentry=configured_form)

    if action == "view_mission":
        # Show the database & a few options
        mission = get_mission(argd["missionid"])
        addresses = read_database()
        missions                = R.rendered_record_list(addresses)
        mission_rendered = R.rendered_record(mission)

        return R.render_page(content=missions, dataentry=mission_rendered)

    if action == "edit_mission":
        mission = get_mission(argd["missionid"])

        addresses = read_database()
        missions                = R.rendered_record_list(addresses)
        pre_filled_data_entry = R.rendered_record_entry_form(mission)
        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="update_mission",
                                                       )
        return R.render_page(content=missions, dataentry=configured_form)

    if action == "update_mission":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        themission = update_mission(stem="form", **argd)

        addresses = read_database()
        missions                = R.rendered_record_list(addresses)
        pre_filled_data_entry = R.rendered_record_entry_form(themission)
        configured_form       = R.render_configured_form(pre_filled_data_entry,nextstep="update_mission")

        return R.render_page(content=missions, dataentry=configured_form)

    if action == "delete_mission":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        # Show the database & a few options
        mission = get_mission(argd["missionid"])
        addresses = read_database()
        missions                = R.rendered_record_list(addresses)
        mission_rendered = R.rendered_record(mission)
        mission_rendered = "<h3> Are you sure you wish to delete this mission?</h3><ul>" + str(mission_rendered)

        delete_action = "<a href='/cgi-bin/app/missions?formtype=confirm_delete_mission&missionid=%s'>%s</a>" % (mission["missionid"], "Delete this mission")
        cancel_action = "<a href='/cgi-bin/app/missions?formtype=view_mission&missionid=%s'>%s</a>" % (mission["missionid"], "Cancel deletion")
        mission_rendered += "</ul><h3> %s | %s </h3>" % (delete_action, cancel_action)

        return R.render_page(content=missions, dataentry=mission_rendered)

    if action == "confirm_delete_mission":
        # Show the database & a few options
        mission = get_mission(argd["missionid"])
        delete_mission(argd["missionid"])

        addresses = read_database()
        missions          = R.rendered_record_list(addresses)
        mission_rendered = R.rendered_record(mission)

        return R.render_page(content=missions, dataentry="<h1> %s Deleted </h1>" % mission["mission"])


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
