#!/usr/bin/env python

from Cheetah.Template import Template
from model.Record import EntitySet
import sys
import os

RelationSet = EntitySet

TreesMembers = RelationSet("treesmembers",key="treememberid")
TreesDatabase = EntitySet("trees",key="treeid")
PeopleDatabase = EntitySet("people",key="personid")

#
# This lot need dealing with more sensibly
#

def store_new_item(the_item): return TreesMembers.new_record(the_item)
def read_database(): return TreesMembers.read_database()
def store_item(item): return TreesMembers.store_record(item)
def get_item(item): return TreesMembers.get_record(item)
def delete_item(item): return TreesMembers.delete_record(item)

#
# Map web request to data layer
#

def make_item(stem="form", **argd):
    new_item = {
        "treeid" : argd.get(stem + ".treeid",""),
        "treename": argd.get(stem + ".treename",""),
	"lhsdb_id"  : argd.get(stem + ".lhsdb_id",""),
        "lhsid"  : argd.get(stem + ".lhsid",""),
	"rhsdb_id"  : argd.get(stem + ".lhsdb_id",""),
	"rhsid"  : argd.get(stem + ".rhsid",""),
    }
    new_item = store_new_item(new_item)
    return new_item

#
# Map web request to data layer
#

def update_item(stem="form", **argd):
    the_item = {
        "treename": argd.get(stem + ".treename",""),
        "lhsdb_id"  : argd.get(stem + ".lhsdb_id",""),
        "lhsid"  : argd.get(stem + ".lhsid",""),
	"rhsdb_id"  : argd.get(stem + ".lhsdb_id",""),
	"rhsid"  : argd.get(stem + ".rhsid",""),			
    }
    store_item(the_item)
    return the_item

#
# Presentation Layer - various aspects of complexity
#

class RelationRender(object):
    record_listview_template = 'templates/TreesMembers.View.tmpl'
    record_editget_template = 'templates/TreeMembers.Edit.tmpl' # Used ?
    record_view_template = 'templates/TreeMembers.View.tmpl'
    record_editpost_template = 'templates/Form.tmpl'         # Posting bulk content...
    page_template = 'templates/Page.tmpl'
    rightfields = ["person","house","street"]    # 
    right_id    = ["personid"]
    leftfields = ["treename"]
    left_id    = ["treeid"]

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
        return str(Template ( file = 'templates/Page.tmpl', 
                             searchList = [
                                  self.environ,
                                  {
                                    "extra": extra ,
                                    "content" : content,
                                    "dataentry" : dataentry,
                                  }
                              ] ))


def RenderedRelation(R, LeftDB, RightDB):
    addresses = read_database()
    Items = LeftDB.read_database()
    People = RightDB.read_database()
    X,Y, Z = {}, {}, {}
    for item in Items:
        X[item[LeftDB.key()]] = item
    for person in People:
        Y[person[RightDB.key()]] = person

    for treemember in addresses:
        #os.sys.stderr.write(repr(treemember))
        if Z.has_key(treemember["treeid"]):
            
            Z[treemember["treeid"]].append(treemember)
        else:
            Z[treemember["treeid"]]= []
            Z[treemember["treeid"]].append(treemember)

    people                = R.rendered_record_list(addresses, X, Y)
    return people

def RenderedRelationOrig(R, LeftDB, RightDB):
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

    leftRecord= LeftDB.get_record(missionstep["treeid"])
    rightRecord = RightDB.get_record(missionstep["personid"])
#    leftRecord= LeftDB.get_record(missionstep[LeftDB.key()])
#    rightRecord = RightDB.get_record(missionstep[RightDB.key()])

    left,right = {},{}

    for K in leftRecord: left["left_"+K] = leftRecord[K]
    for K in rightRecord: right["right_"+K] = rightRecord[K]

    dataentry = Template ( file = 'templates/TreeMembers.View.tmpl',
                           searchList = [environ,
                                         left,
                                         right,
                                         {
                                              "relation" : "member number",
                                              relationkey : missionstepid,
                                              # "humancondition" :missionstep["humancondition"] ,
                                              # "machinecondition" :missionstep["machinecondition"],

                                         }] )
    return dataentry




def RenderedRelationEntryForm(environ, LeftRelationName, RightRelationName, LeftDB, RightDB, **extra_args):


    LeftTuples = LeftDB.read_database()
    RightTuples = RightDB.read_database()

    empty_data_entry = Template ( file = "templates/TreeMembers.Edit.tmpl",
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
        treesmembers = str(RenderedRelation(R, TreesDatabase, PeopleDatabase))

        X = R.render_page(content=treesmembers)
        return X

    if action == "view":

        treesmembers = RenderedRelation(R, TreesDatabase, PeopleDatabase)
        rendered_tuple = RenderedTuple(argd["__environ__"],"treememberid", argd["treememberid"], TreesDatabase, PeopleDatabase)

        return R.render_page(content=treesmembers, dataentry=rendered_tuple)

    if action == "edit_new":
        treesmembers = RenderedRelation(R, TreesDatabase, PeopleDatabase)

        empty_data_entry = RenderedRelationEntryForm( argd["__environ__"], "Trees", "People",TreesDatabase, PeopleDatabase)
        configured_form  = R.render_configured_form(empty_data_entry,submitlabel="Add Item")

        return R.render_page(content=treesmembers, dataentry=configured_form)

    if action == "edit":
        item_person = get_item(argd["treememberid"])

        people = RenderedRelation(R, TreesDatabase, PeopleDatabase)

        pre_filled_data_entry = RenderedRelationEntryForm( argd["__environ__"], "Items", "People", TreesDatabase, PeopleDatabase,
                                               # This next bit prevents reuse...
                                                     treememberid = item_person["treememberid"], # N.B. treememberid: etc. 
                                                     leftselected = item_person["treeid"],
                                                     rightselected = item_person["personid"]
                                                    )

        configured_form       = R.render_configured_form(pre_filled_data_entry,
                                                       nextstep="update",
                                                       submitlabel="Update Item",
                                                       )
        return R.render_page(content=people, dataentry=configured_form)

    if action == "create_new":
        if argd.get("form.treename")=="":
            argd["form.treename"]=Treesdatabase[argd.get("form.treeid")]["treename"]
            os.stderr.write(argd.get("form.treename"))
        new_item = make_item(stem="form", **argd) # This also stores them in the database

        people = RenderedRelation(R, TreesDatabase, PeopleDatabase)
        rendered_tuple = RenderedTuple(argd["__environ__"],"treememberid", new_item["treememberid"], TreesDatabase, PeopleDatabase)
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

        people = RenderedRelation(R,TreesDatabase , PeopleDatabase)
        rendered_tuple = RenderedTuple(argd["__environ__"],"treememberid", theitem["treememberid"], TreesDatabase, PeopleDatabase)
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
        item = get_item(argd["treememberid"])
        people = RenderedRelation(R, TreesDatabase, PeopleDatabase)

        item_rendered = RenderedTuple(argd["__environ__"],"treememberid", item["treememberid"], TreesDatabase, PeopleDatabase)

        prebanner = "<h3> Are you sure you wish to delete this item</h3>"
        delete_action = "<a href='/cgi-bin/app/treesmembers?formtype=confirm_delete&treememberid=%s'>%s</a>" % (item["treememberid"], "Delete this item")
        cancel_action = "<a href='/cgi-bin/app/treemembers?formtype=view&treememberid=%s'>%s</a>" % (item["treememberid"], "Cancel deletion")

        delete_message = "%s <ul> %s </ul><h3> %s | %s </h3>" % (prebanner, str(item_rendered), delete_action, cancel_action)

        return R.render_page(content=people, dataentry=delete_message)

    if action == "confirm_delete":
        # Show the database & a few options

        item = get_item(argd["treememberid"])

        delete_item(argd["treememberid"])

        people = RenderedRelation(R, TreesDatabase, PeopleDatabase)

        return R.render_page(content=people, dataentry="<h1> Record %s Deleted </h1>" % argd["treememberid"])

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
