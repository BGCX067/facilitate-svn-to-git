#!/usr/bin/env python

from Cheetah.Template import Template
from model.Record import EntitySet
import sys
import os

RelationSet = EntitySet

ItemsPeopleRelation = RelationSet("itemspeople_relation",key="itempersonid")
ItemsDatabase = EntitySet("items",key="itemid")
PeopleDatabase = EntitySet("people")

#
# This lot need dealing with more sensibly
#

def store_new_item(the_item): return ItemsPeopleRelation.new_record(the_item)
def read_database(): return ItemsPeopleRelation.read_database()
def store_item(item): return ItemsPeopleRelation.store_record(item)
def get_item(item): return ItemsPeopleRelation.get_record(item)
def delete_item(item): return ItemsPeopleRelation.delete_record(item)

#
# Map web request to data layer
#

def make_item(stem="form", **argd):
    new_item = {
        ItemsDatabase.key() : argd.get(stem + "."+ItemsDatabase.key(),""),
        PeopleDatabase.key() : argd.get(stem + "."+PeopleDatabase.key(),""),
    }
    new_item = store_new_item(new_item)
    return new_item

#
# Map web request to data layer
#

def update_item(stem="form", **argd):
    the_item = {
        "itempersonid" : argd.get(stem + ".itempersonid",""),
        ItemsDatabase.key() : argd.get(stem + "."+ItemsDatabase.key(),""),
        PeopleDatabase.key() : argd.get(stem + "." + PeopleDatabase.key(),""),
    }
    store_item(the_item)
    return the_item

#
# Presentation Layer - various aspects of complexity
#

class RelationRender(object):
    record_listview_template = 'templates/Items_People.View.tmpl'
    record_editget_template = 'templates/Item_Person.Edit.tmpl' # Used ?
    record_view_template = 'templates/Item_Person.View.tmpl'
    record_editpost_template = 'templates/Form.tmpl'         # Posting bulk content...
    page_template = 'templates/Page.tmpl'
    leftfields = ["item", "tags"]
    rightfields = ["person", "house", "street", "town", "county", "postcode", "phone"]

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

    people                = R.rendered_record_list(addresses, X, Y)
    return people

def RenderedTuple(environ, relationkey, itempersonid, LeftDB, RightDB):
    itemperson = get_item(itempersonid)

    leftRecord= LeftDB.get_record(itemperson[LeftDB.key()])
    rightRecord = RightDB.get_record(itemperson[RightDB.key()])

    left,right = {},{}

    for K in leftRecord: left["left_"+K] = leftRecord[K]
    for K in rightRecord: right["right_"+K] = rightRecord[K]

    dataentry = Template ( file = 'templates/Item_Person.View.tmpl',
                           searchList = [environ,
                                         left,
                                         right,
                                         {
                                              "relation" : "Item owned by",
                                              relationkey : itempersonid,
                                         }] )
    return dataentry

def RenderedRelationEntryForm(environ, LeftRelationName, RightRelationName, LeftDB, RightDB, **extra_args):


    LeftTuples = LeftDB.read_database()
    RightTuples = RightDB.read_database()

    empty_data_entry = Template ( file = "templates/ItemsPeople.Test.tmpl",
                                 searchList = [
                                     environ, {
                                       LeftRelationName:LeftTuples,
                                       RightRelationName:RightTuples,
                                     }, extra_args
                                 ]
                               )
    return empty_data_entry 


def page_render_html(json, **argd):
    action = argd.get("formtype","overview")
    R = RelationRender(argd["__environ__"])

    if action == "overview":
        rendered_items_people = str(RenderedRelation(R, ItemsDatabase, PeopleDatabase))

        X = R.render_page(content=rendered_items_people)
        return X

    if action == "view":

        rendered_items_people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)
        rendered_tuple = RenderedTuple(argd["__environ__"],"itempersonid", argd["itempersonid"], ItemsDatabase, PeopleDatabase)

        return R.render_page(content=rendered_items_people, dataentry=rendered_tuple)

    if action == "edit_new":
        rendered_items_people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)

        empty_data_entry = RenderedRelationEntryForm( argd["__environ__"], "Items", "People", ItemsDatabase, PeopleDatabase)
        configured_form  = R.render_configured_form(empty_data_entry,submitlabel="Add Item")

        return R.render_page(content=rendered_items_people, dataentry=configured_form)

    if action == "edit":
        item_person = get_item(argd["itempersonid"])

        rendered_items_people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)

        pre_filled_data_entry = RenderedRelationEntryForm( argd["__environ__"], "Items", "People", ItemsDatabase, PeopleDatabase,
                                               # This next bit prevents reuse...
                                                     itempersonid = item_person["itempersonid"],
                                                     itemselected = item_person[ItemsDatabase.key()],
                                                     personselected = item_person[PeopleDatabase.key()]
                                                    )

        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="update",
                                                       submitlabel="Update Item",
                                                       )
        return R.render_page(content=rendered_items_people, dataentry=configured_form)

    if action == "create_new":

        new_item = make_item(stem="form", **argd) # This also stores them in the database

        rendered_items_people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)
        rendered_tuple = RenderedTuple(argd["__environ__"],"itempersonid", new_item["itempersonid"], ItemsDatabase, PeopleDatabase)
        rendered_tuple = "<B> Record Saved </B>. If you wish to update, please do" + str(rendered_tuple)

        return R.render_page(content=rendered_items_people, dataentry=rendered_tuple)

    if action == "update":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        theitem = update_item(stem="form", **argd)

        rendered_items_people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)
        rendered_tuple = RenderedTuple(argd["__environ__"],"itempersonid", theitem["itempersonid"], ItemsDatabase, PeopleDatabase)
        rendered_tuple = "<B> Record Saved </B>. If you wish to update, please do" + str(rendered_tuple)

        return R.render_page(content=rendered_items_people, dataentry=rendered_tuple)

    if action == "delete_item":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        # Show the database & a few options
        item = get_item(argd["itempersonid"])
        rendered_items_people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)

        item_rendered = RenderedTuple(argd["__environ__"],"itempersonid", item["itempersonid"], ItemsDatabase, PeopleDatabase)

        prebanner = "<h3> Are you sure you wish to delete this item</h3>"
        delete_action = "<a href='/cgi-bin/app/items_people?formtype=confirm_delete&itempersonid=%s'>%s</a>" % (item["itempersonid"], "Delete this item")
        cancel_action = "<a href='/cgi-bin/app/items_people?formtype=view&itempersonid=%s'>%s</a>" % (item["itempersonid"], "Cancel deletion")

        delete_message = "%s <ul> %s </ul><h3> %s | %s </h3>" % (prebanner, str(item_rendered), delete_action, cancel_action)

        return R.render_page(content=rendered_items_people, dataentry=delete_message)

    if action == "confirm_delete":
        # Show the database & a few options

        item = get_item(argd["itempersonid"])

        delete_item(argd["itempersonid"])

        rendered_items_people = RenderedRelation(R, ItemsDatabase, PeopleDatabase)

        return R.render_page(content=rendered_items_people, dataentry="<h1> Record %s Deleted </h1>" % argd["itempersonid"])

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
