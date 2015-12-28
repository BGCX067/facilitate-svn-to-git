#!/usr/bin/env python

from Cheetah.Template import Template
from model.Record import EntitySet
import sys
import os

RelationSet = EntitySet

MissionStepsRelation = RelationSet("missionsteps_relation",key="missionstepid")
ItemsDatabase = EntitySet("missions",key="missionid")
PeopleDatabase = EntitySet("missions",key="missionid")

#
# This lot need dealing with more sensibly
#

def store_new_item(the_item): return MissionStepsRelation.new_record(the_item)
def read_database(): return MissionStepsRelation.read_database()
def store_item(item): return MissionStepsRelation.store_record(item)
def get_item(item): return MissionStepsRelation.get_record(item)
def delete_item(item): return MissionStepsRelation.delete_record(item)

#
# Map web request to data layer
#

def make_item(stem="form", **argd):
    new_item = {
#        ItemsDatabase.key() : argd.get(stem + "."+ItemsDatabase.key(),""),
#        PeopleDatabase.key() : argd.get(stem + "."+PeopleDatabase.key(),""),
        "leftid" : argd.get(stem + ".leftid",""),
        "rightid"  : argd.get(stem + ".rightid",""),
        "humancondition" : argd.get(stem + ".humancondition",""),
        "machinecondition"  : argd.get(stem + ".machinecondition",""),
    }
    new_item = store_new_item(new_item)
    return new_item

#
# Map web request to data layer
#

def update_item(stem="form", **argd):
    the_item = {
        "missionstepid" : argd.get(stem + ".missionstepid",""),
        "leftid" : argd.get(stem + ".leftid",""),
        "rightid"  : argd.get(stem + ".rightid",""),
        "humancondition" : argd.get(stem + ".humancondition",""),
        "machinecondition"  : argd.get(stem + ".machinecondition",""),
    }
    store_item(the_item)
    return the_item

#
# Presentation Layer - various aspects of complexity
#

class RelationRender(object):
    record_listview_template = 'templates/MissionSteps.View.tmpl'
    record_editget_template = 'templates/MissionStep.Edit.tmpl' # Used ?
    record_view_template = 'templates/MissionStep.View.tmpl'
    record_editpost_template = 'templates/Form.tmpl'         # Posting bulk content...
    page_template = 'templates/Page.tmpl'
    leftfields = ["mission", "shortdescription"]
    rightfields = ["mission", "shortdescription"]

    def __init__(self, environ):
        self.environ = environ

    def rendered_record_list(self, records, table_one, table_two):
        people = Template ( file = self.record_listview_template,
                            searchList = [self.environ, {
                                                         "tuples": records,
                                                         "tableone" : table_one,
                                                         "tabletwo" : table_two,
                                                         "leftfields" : self.leftfields,
                                                         "rightfields" : self.rightfields,
                                                        }
                                         ]
                          )
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
        X = Template ( file = 'templates/Page.tmpl', 
                             searchList = [
                                  self.environ,
                                  {
                                    "extra": extra ,
                                    "content" : content,
                                    "dataentry" : dataentry,
                                  }
                              ] )
        X = str(X)
        return X

def RenderedRelation(R, LeftDB, RightDB):
    addresses = read_database()
    Items = LeftDB.read_database()
    People = RightDB.read_database()
    X,Y = {}, {}
    for item in Items:
        X[item[LeftDB.key()]] = item
    for person in People:
        Y[person[RightDB.key()]] = person

#    return "people"+str(X)+str(Y)
    people                = R.rendered_record_list(addresses, X, Y)
    return people

def RenderedTuple(environ, relationkey, missionstepid, LeftDB, RightDB):
    missionstep = get_item(missionstepid)

    leftRecord= LeftDB.get_record(missionstep["leftid"])
    rightRecord = RightDB.get_record(missionstep["rightid"])
#    leftRecord= LeftDB.get_record(missionstep[LeftDB.key()])
#    rightRecord = RightDB.get_record(missionstep[RightDB.key()])

    left,right = {},{}

    for K in leftRecord: left["left_"+K] = leftRecord[K]
    for K in rightRecord: right["right_"+K] = rightRecord[K]

    dataentry = Template ( file = 'templates/MissionStep.View.tmpl',
                           searchList = [environ,
                                         left,
                                         right,
                                         {
                                              "relation" : "Mission Followed by",
                                              relationkey : missionstepid,
                                              "humancondition" :missionstep["humancondition"] ,
                                              "machinecondition" :missionstep["machinecondition"],

                                         }] )
    return dataentry

def RenderedRelationEntryForm(environ, LeftRelationName, RightRelationName, LeftDB, RightDB, **extra_args):


    LeftTuples = LeftDB.read_database()
    RightTuples = RightDB.read_database()

    empty_data_entry = Template ( file = "templates/MissionStep.Edit.tmpl",
                                 searchList = [
                                     environ, {
                                       "Items":LeftTuples,
                                       "People":RightTuples,
                                     }, extra_args
                                 ]
                               )
    return empty_data_entry 


def page_render_html(json, **argd):
    action = argd.get("formtype","overview")
    R = RelationRender(argd["__environ__"])

    if action == "overview":
        people = str(RenderedRelation(R, ItemsDatabase, PeopleDatabase))

        X = R.render_page(content=people)
        return X

    if action == "view":

        people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)
        rendered_tuple = RenderedTuple(argd["__environ__"],"missionstepid", argd["missionstepid"], ItemsDatabase, PeopleDatabase)

        return R.render_page(content=people, dataentry=rendered_tuple)

    if action == "edit_new":
        people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)

        empty_data_entry = RenderedRelationEntryForm( argd["__environ__"], "Items", "People", ItemsDatabase, PeopleDatabase)
        configured_form  = R.render_configured_form(empty_data_entry,submitlabel="Add Item")

        return R.render_page(content=people, dataentry=configured_form)

    if action == "edit":
        item_person = get_item(argd["missionstepid"])

        people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)

        pre_filled_data_entry = RenderedRelationEntryForm( argd["__environ__"], "Items", "People", ItemsDatabase, PeopleDatabase,
                                               # This next bit prevents reuse...
                                                     missionstepid = item_person["missionstepid"],
                                                     leftselected = item_person["leftid"],
                                                     rightselected = item_person["rightid"]
                                                    )

        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="update",
                                                       submitlabel="Update Item",
                                                       )
        return R.render_page(content=people, dataentry=configured_form)

    if action == "create_new":

        new_item = make_item(stem="form", **argd) # This also stores them in the database

        people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)
        rendered_tuple = RenderedTuple(argd["__environ__"],"missionstepid", new_item["missionstepid"], ItemsDatabase, PeopleDatabase)
        rendered_tuple = "<B> Record Saved </B>. If you wish to update, please do" + str(rendered_tuple)

        return R.render_page(content=people, dataentry=rendered_tuple)

    if action == "update":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        theitem = update_item(stem="form", **argd)

        people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)
        rendered_tuple = RenderedTuple(argd["__environ__"],"missionstepid", theitem["missionstepid"], ItemsDatabase, PeopleDatabase)
        rendered_tuple = "<B> Record Saved </B>. If you wish to update, please do" + str(rendered_tuple)

        return R.render_page(content=people, dataentry=rendered_tuple)

    if action == "delete_item":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        # Show the database & a few options
        item = get_item(argd["missionstepid"])
        people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)

        item_rendered = RenderedTuple(argd["__environ__"],"missionstepid", item["missionstepid"], ItemsDatabase, PeopleDatabase)

        prebanner = "<h3> Are you sure you wish to delete this item</h3>"
        delete_action = "<a href='/cgi-bin/app/missionsteps?formtype=confirm_delete&missionstepid=%s'>%s</a>" % (item["missionstepid"], "Delete this item")
        cancel_action = "<a href='/cgi-bin/app/missionsteps?formtype=view&missionstepid=%s'>%s</a>" % (item["missionstepid"], "Cancel deletion")

        delete_message = "%s <ul> %s </ul><h3> %s | %s </h3>" % (prebanner, str(item_rendered), delete_action, cancel_action)

        return R.render_page(content=people, dataentry=delete_message)

    if action == "confirm_delete":
        # Show the database & a few options

        item = get_item(argd["missionstepid"])

        delete_item(argd["missionstepid"])

        people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)

        return R.render_page(content=people, dataentry="<h1> Record %s Deleted </h1>" % argd["missionstepid"])

    return str(Template ( file = 'templates/Page.tmpl', 
                         searchList = [
                             argd["__environ__"],
                              {
                                "extra": "" ,
                                "content" : "Sorry, got no idea what you want! (%s)" % str(action),
                                "dataentry" : "",
                                "banner" : "Not found", # XXXX should send back a 404 status
                              }
                          ] ))

if __name__ == "__main__":

    print "Content-Type: text/html"
    print

    print page_render_html({})
