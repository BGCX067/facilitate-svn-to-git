#!/usr/bin/env python

from Cheetah.Template import Template
from model.Record import EntitySet
import sys
import os

ItemsDatabase = EntitySet("items",key="itemid")

#
# Map web request to data layer
#

def make_item(stem="form", **argd):
    new_item = {
        "item" : argd.get(stem + ".item",""),
        "__filename" : argd.get(stem + ".upload.1.__filename",""),
        "tags" : argd.get(stem + ".tags",""),
    }
    new_item = ItemsDatabase.new_record(new_item)
    return new_item

#
# Map web request to data layer
#

def update_item(stem="form", **argd):
    sys.stderr.write("__FILENAME?" + argd.get(stem + ".upload.1.__filename","NOPE, NOTHING")+"\n")
    the_item = {
        "itemid" : argd.get(stem + ".itemid",""),
        "item" : argd.get(stem + ".item",""),
        "__filename" : argd.get(stem + ".upload.1.__filename",""),
        "tags" : argd.get(stem + ".tags",""),
    }
    ItemsDatabase.store_record(the_item)
    return the_item

#
# Presentation Layer - various aspects of complexity
#

class RecordRender(object):
    record_listview_template = 'templates/Items.View.tmpl'
    record_editget_template = 'templates/Item.Edit.tmpl'
    record_view_template = 'templates/Item.View.tmpl'
    record_editpost_template = 'templates/Form.Post.tmpl'         # Posting bulk content...
    page_template = 'templates/Page.tmpl'

    def __init__(self, environ):
        self.environ = environ

    def rendered_record_list(self, items):
        rendered_items = Template ( file = self.record_listview_template,
                            searchList = [self.environ, {"Items": items}] )
        return rendered_items

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
    DB = ItemsDatabase

    if action == "overview":
        #
        # Basic view
        #
        # Currently dumps all items - non-selected, unrestricted view
        #
        records = DB.read_database()
        rendered_records  = R.rendered_record_list(records)
        return R.render_page(content=rendered_records)

    if action == "view":
        # Show the database & a few options
        record = DB.get_record(argd["itemid"])
        records = DB.read_database()
        rendered_records                = R.rendered_record_list(records)
        rendered_record = R.rendered_record(record)

        return R.render_page(content=rendered_records, dataentry=rendered_record)

    if action == "edit_new":
        #
        # Same as basic view but also:
        #    Present a form that the user will use to create/upload a new blob item
        #    If the user hits "Add Item", then the user will upload their data and
        #    create a new item. Next view: create_new
        #
        records = DB.read_database()
        rendered_records           = R.rendered_record_list(records)
        empty_data_entry = R.rendered_record_entry_form({})
        configured_form  = R.render_configured_form(empty_data_entry,submitlabel="Add Item")

        return R.render_page(content=rendered_records, dataentry=configured_form)

    if action == "create_new":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        new_record = make_item(stem="form", **argd) # This also stores them in the database

        records = DB.read_database()
        rendered_records                = R.rendered_record_list(records)
        pre_filled_data_entry = R.rendered_record_entry_form(new_record)
        configured_form       = R.render_configured_form(pre_filled_data_entry, nextstep="update")

        return R.render_page(content=rendered_records, dataentry=configured_form)

    if action == "edit":
        record = DB.get_record(argd["itemid"])

        records = DB.read_database()
        rendered_records                = R.rendered_record_list(records)
        pre_filled_data_entry = R.rendered_record_entry_form(record)
        configured_form       = R.render_configured_form(pre_filled_data_entry, nextstep="update")

        return R.render_page(content=rendered_records, dataentry=configured_form)

    if action == "update":
        #
        # User is creating a new item - they've just sent us data from edit_new
        #
        # Theoretically, this shouldn't be called via update....
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        try:
            record = DB.get_record(argd["itemid"])
            old_filename = item["__filename"]
        except KeyError:
            old_filename = None

        new_record = update_item(stem="form", **argd)
        if new_record["__filename"]:
            new_filename = new_record["__filename"]
            if old_filename  and (old_filename != new_filename):
                os.unlink(old_filename)

        records = DB.read_database()
        rendered_records                = R.rendered_record_list(records)
        pre_filled_data_entry = R.rendered_record_entry_form(new_record)
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
        item = DB.get_record(argd["itemid"])
        items = DB.read_database()
        rendered_items                = R.rendered_record_list(items)
        item_rendered = R.rendered_record(item)

        item_rendered = "<h3> Are you sure you wish to delete this item?</h3><ul>" + str(item_rendered)

        delete_action = "<a href='/cgi-bin/app/items?formtype=confirm_delete&itemid=%s'>%s</a>" % (item["itemid"], "Delete this item")
        cancel_action = "<a href='/cgi-bin/app/items?formtype=view&itemid=%s'>%s</a>" % (item["itemid"], "Cancel deletion")
        item_rendered += "</ul><h3> %s | %s </h3>" % (delete_action, cancel_action)

        return R.render_page(content=rendered_items, dataentry=item_rendered)

    if action == "confirm_delete":
        # Show the database & a few options
        record = DB.get_record(argd["itemid"])
        sys.stderr.write(str(record)+"\n")
        os.unlink(record["__filename"])
        DB.delete_record(argd["itemid"])

        records = DB.read_database()
        rendered_records          = R.rendered_record_list(records)
#        record_rendered = R.rendered_record(record)

        return R.render_page(content=rendered_records, dataentry="<h1> %s Deleted </h1>" % record["item"])


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
