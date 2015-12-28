#!/usr/bin/python

from Cheetah.Template import Template
from model.Record import EntitySet

# NOTE: You would rename "Missions" here to match your entity set's name
MissionsDatabase = EntitySet("missions",key="missionid")

# NOTE: Likewise, rather than MissionsDatabase, this would be your entity's name
def store_new_mission(the_mission): return MissionsDatabase.new_record(the_mission)
def read_database(): return MissionsDatabase.read_database()
def store_mission(mission): return MissionsDatabase.store_record(mission)
def get_mission(mission): return MissionsDatabase.get_record(mission)
def delete_mission(mission): return MissionsDatabase.delete_record(mission)

#
# Map web request to data layer
#

# NOTE: This is our constructor for new entities.
# NOTE: You can create an "empty" mission by doing this, and customise
# NOTE: it this way:
# NOTE:    aMission = make_mission()
# NOTE:    aMission["mission"] = "..."
# NOTE:    aMission["shortdescription"] = "invade a planet"
# NOTE:    aMission["mediumdescription"] = "..."
#
# NOTE: However the changes to "aMission" above are NOT persistent.
#
# NOTE: In order to store updates to disk you would need to do this:
#
# NOTE: store_mission(aMission)
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
# NOTE: update_mission is used grab a record from a form (in argd)
# NOTE: and then to write this to disk.
#
# NOTE: This, along with make_mission are candidate locationss for
# NOTE: *using* data validation. 
#
# Other: Ideally this stuff should really be
# Other: enforced, located inside Record which gets subclassed for
# Other: configuration.
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


# NOTE: You have to customise the template names here

class RecordRender(object):
    record_listview_template = 'templates/Missions.View.tmpl'
    record_editget_template = 'templates/Mission.Edit.tmpl'
    record_view_template = 'templates/Mission.View.tmpl'

    record_editpost_template = 'templates/Form.tmpl' # NOTE: Generally does not need changing
    page_template = 'templates/Page.tmpl'            # NOTE: Generally does not need changing

    def __init__(self, environ,**argd):
        self.environ = environ
        self.__dict__.update(argd)


# NOTE: the key here "missions" refers to a value in Missions.View.tmpl
# NOTE: So they *at present* need keeping in step. This will be simplified.

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
# Actually _Entity_ Life Cycle Logic
#

# NOTE: How you customise this depends on your entities. Ideally you will
# NOTE: at present just update this by changing entity & entity set names.
#
# NOTE: Yes, this is intended to be configurable.
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
