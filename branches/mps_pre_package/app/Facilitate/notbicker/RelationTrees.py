#!/usr/bin/env python

from Cheetah.Template import Template
from model.Record import EntitySet
import cjson
import sys
import os

RelationSet = EntitySet

MissionStepsRelation = RelationSet("relationtrees",key="relationid")
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
def get_itemtypes(dirlist = ["relationtrees","items","comments"]):               # Prolly should get moved to Record.py
    itemtype_list=[]
    id = 0 
    for dir in dirlist:
        if (dir[0] !=  ".") : #so we don't link to ourself or .meta etc.
            itemtype_list.append({'itemid':id,'item':dir}) #% (str(id), dir))
            id+=1
    return itemtype_list

def get_itemtype_key(item_type):    # Prolly should get moved to Record.py
    try:                            # can have empty data_item directory
        F = open("data/"+item_type+"/.meta")  
        item_type_key = cjson.decode(F.read())["key"]
        F.close()
    except:
        item_type_key = None 
    return item_type_key

def get_item_record(db_id,item_id):  # Prolly should get moved to Record.py
    try:                             # in case file goes away?
        F = open("data/"+db_id+"/"+item_id) 
        item_record = cjson.decode(F.read())
        F.close()
    except:
        item_record = None
    return item_record

def get_item_type_keys(db_id,item_id): # Prolly should get moved to Record.py, if used - template expansion may obviate
    try:                               # keys added to .meta? can't rely on a record being present?
        F=open('data/'+db_id+'/'+item_id)
        item_type_keys = cjson.decode(F.read()).keys()
        F.close()
    except:
        item_type_keys = None
    return item_type_keys


def get_item_values(db_id,item_id,record): # Prolly should get moved to Record.py
    try: 
        F = open('data/'+db_id+'/'+item_id)
        record_values = cjson.decode(F.read())
        F.close()
    except:
        record_values = None
    return record_values
        

def get_item_record_pair(relation):   # Prolly should get moved to Record.py
    left_dbid = relation['left_dbid']
    right_dbid = relation['right_dbid']
    left_itemid = relation['left_itemid']
    right_itemid = relation['right_itemid']
    left_item_record = get_item_record(left_dbid,left_itemid)
    right_item_record = get_item_record(right_dbid,right_itemid)
    return [left_item_record, right_item_record]

def make_item(stem="form", **argd):
    new_item = {
        "left_dbid" : argd.get(stem + ".left_dbid",""),
        "left_itemid" : argd.get(stem + ".left_itemid",""),
        "right_dbid"  : argd.get(stem + ".right_dbid",""),
        "right_itemid"  : argd.get(stem + ".right_itemid",""),
        "root_dbid": argd.get(stem + ".root_dbid",""),    # used ?
        "root_id" : argd.get(stem + ".root_id",""),
    }
    new_item = store_new_item(new_item)
    return new_item

#
# Map web request to data layer
#

def update_item(stem="form", **argd):
    the_item = {
        "relationid" : argd.get(stem + ".relationid",""),
        "left_dbid" : argd.get(stem + ".left_dbid",""),
        "left_itemid" : argd.get(stem + ".left_itemid",""),
        "right_dbid"  : argd.get(stem + ".right_dbid",""),
        "right_itemid"  : argd.get(stem + ".right_itemid",""),
        "root_dbid": argd.get(stem + ".root_dbid",""),             # used ?
        "root_id" : argd.get(stem + ".root_id",""),			
    }
    store_item(the_item)
    return the_item

#
# Presentation Layer - various aspects of complexity
#

class RelationRender(object):
    record_listview_template = 'templates/RelationTrees.View.tmpl'
    record_editget_template = 'templates/RelationTree.Edit.tmpl' # Used ?
    record_editget_items_template = 'templates/RelationTrees.Items.Edit.tmpl'
    record_view_template = 'templates/RelationTree.View.tmpl'
    record_editpost_template = 'templates/Form.tmpl'         # Posting bulk content...
    page_template = 'templates/Page.tmpl'
    itemtypes_view_template = 'templates/TreesTypes.View.tmpl'#template to view data item types
    display_dbs = ["relations","items","comments"]
    itemtype_list = [{'itemid':0,'item':'relations'}, 
                     {'itemid':1,'item':'data'},
                     {'itemid':2,'item':'items'}] 
    leftfields = ["mission", "shortdescription"]
    rightfields = ["mission", "shortdescription"]

    def __init__(self, environ):
        self.environ = environ

    def rendered_record_list(self,relations):
        rendered_relations = Template ( file = self.record_listview_template,
                            searchList = [self.environ, {"relations": relations}] )
        return rendered_relations

    def rendered_relations_list(self,relations):
        rendered_relations = []
        for relation in relations:
            rendered_relations.append(get_item_record_pair(relation))    
        return rendered_relations


    def rendered_itemtypes(self, relationid,relations, itemtypes):
         rendered_itemtypes = Template( file = self.itemtypes_view_template,
				      searchList = [self.environ,
                                                    {"relationid":relationid},{"relations":relations}, {"itemtypes":itemtypes}])
         return rendered_itemtypes

    def rendered_relation_list(self, records, table_one, table_two):
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

    def rendered_record_item_entry_form(self, item):      # so we can edit the items in the relation from arbitary dbs 
        dataentry = Template ( file = self.record_editget_items_template,
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

    def render_configured_item_form(self, pre_filled_data_entry,
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

    def render_databases(self, content="", extra="",dataentry=""):
        X = Template( file='templates/Page.tmpl'
                  )
    
    def get_itemtypes(self):               # Prolly should get moved to Record.py
        itemtype_list=[]
        id = 0 
        for dir in os.listdir("data"):
            if (dir[0] !=  ".") and (dir !="relations") : #so we don't link to ourself or .meta etc.
                itemtype_list.append({'itemid':id,'item':dir}) #% (str(id), dir))
                id+=1
        return itemtype_list                       

def RenderedRelation(R, LeftDB, RightDB):
    os.sys.stderr.write(repr(dir(R))+"*******dict********\n")
    os.sys.stderr.write(repr(R.environ)+"********environ*******\n")
    os.sys.stderr.write(repr(R.environ["bbc.args"]["__environ__"])+"***************\n")
    os.sys.stderr.write(R.environ["bbc.args"]["form.leftid"]+"+++++form leftid \n") # # # # # # # # 
    addresses = read_database()
    Left_Items = LeftDB.read_database()
    Right_Items = RightDB.read_database()
    X,Y = {}, {}
    for item in Left_Items:
        X[item[LeftDB.key()]] = item
    for item in Right_Items:
        Y[item[RightDB.key()]] = item

   # return "people"+str(X)+str(Y)
   # people                = R.rendered_record_list(addresses, X, Y)
    return None #people

def RenderedTuple(environ, relationkey, relationid, LeftDB, RightDB):
    relation = get_item(relationid)

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

def RenderedRelationPair(environ,relation, relationpair):
    leftRecord = relationpair[0]
    rightRecord = relationpair[1]
    left_dbid = relation['left_dbid']
    right_dbid = relation['right_dbid']
    leftid = relation['left_itemid']
    rightid = relation['right_itemid']
    #os.sys.stderr.write("here  "+relation["relationid"]+"\n") 
    left_vals = get_item_values( left_dbid,leftid,leftRecord)
    if left_vals ==None:
        os.sys.stderr.write("****************lhs none*********\n")
        left_vals = "None"     
    #os.sys.stderr.write(repr(left_vals))
    right_vals = get_item_values( right_dbid ,rightid,rightRecord)
     #left_keys = get_item_type_keys(relation['left_dbid'],relation['left_itemid'R])
     #right_keys = get_item_type_keys(relation['right_dbid'],relation['right_itemid'])
    dataentry = Template ( file = 'templates/RelationPair.View.tmpl',
                           searchList = [environ,
                                         environ.environ,
                                         {
                                              "relation" : "This relates",
                                               "relationid":relation["relationid"],
                                               "LeftVals":left_vals,
                                               "RightVals":right_vals,
                                               "Leftdbid" : left_dbid,
                                               "Rightdbid" : right_dbid, 
                                               "Leftid": leftid,
                                               "Rightid":rightid, 
                                         }] )
    return dataentry

def RenderedRelationEntryForm(realtionid, LeftRelationName, RightRelationName, leftkey,rightkey, LeftDB, RightDB, **extra_args):

    
    LeftTuples = LeftDB.read_database()
    RightTuples = RightDB.read_database()
    os.sys.stderr.write(str(RightTuples)+"\n")
    os.sys.stderr.write(str(LeftRelationName)+"\n")
    empty_data_entry = Template ( file = "templates/RelationTrees.Items.Edit.tmpl",
                                 searchList = [
                                      
                                     {
                                       "relationid":realtionid,
                                       "left_dbid" : LeftRelationName,
                                       "right_dbid": RightRelationName,
                                       "leftkey":leftkey,
                                       "rightkey":rightkey,
                                       "LeftItems" : LeftTuples,
                                       "RightItems" : RightTuples,
                                       "left_itemkeys":LeftTuples[0].keys,
                                       "right_itemkeys":RightTuples[0].keys
                                     }, extra_args
                                 ]
                               )
    return empty_data_entry 


def find_children(this_root,this_tree,current_tree):         # tree as dictionary of lists c.f. http://www.python.org/doc/essays/graphs.html
    for item in current_tree:                               
        if item["left_dbid"] == "relationtrees" and item["left_itemid"]==this_root:
            child_id = item["relationid"]
            this_tree[this_root].append(child_id)
            current_tree.remove(item)            
    for id in this_tree[this_root]:
        this_tree[id] = []
        find_children(id,this_tree,current_tree)

def render_subtree(level,child,keys,relation_list,this_tree):
     level+=1
     for key in keys:
         child+=1
         subtree_keys = this_tree[key]
         strlevel = str(level)
         strchild = str(child)
         list = repr(subtree_keys)
         relation_list.append({"level":strlevel,"child":strchild,"subtree":list,"root_id":-99,"relationid":"-1"})
         relation_list.append(get_item(key))
          #relation_list.append({"level":strlevel,"child":strchild,"subtree":list,"root_id":-99,"relationid":"-1"})
         for key in subtree_keys:
             render_subtree(level,child,subtree_keys,relation_list,this_tree)
     return relation_list
     
     
def render_relation_tree(key,relation_list,this_tree):
    subtree_keys = this_tree[key]
    list = repr(subtree_keys)
    relation_list.append({"level":"0","child":"0","subtree":list,"root_id":-99,"relationid":"-1"}) 
    relation_list.append(get_item(key))
    level = 0
    child = 0
    render_subtree(level,child,subtree_keys,relation_list,this_tree)
    return relation_list
    
        
         
    
                

def page_render_html(json, **argd):
    action = argd.get("formtype","overview")
    R = RelationRender(argd["__environ__"])

    if action == "overview":
        relations = read_database()
        rendered_relations = R.rendered_record_list(relations)  # generalised Rendered Relation
        return R.render_page(content=rendered_relations) #str(R.environ)) #


    if action == "edit_new":
        relations = read_database()
        os.sys.stderr.write(repr(relations)+"***************empty db *****\n")
        if relations == []:
            leftitemtypes = get_itemtypes(dirlist= ["items","comments"])
        else:
            leftitemtypes = get_itemtypes()
        rendered_relations = R.rendered_record_list(relations)  #generalised Rendered Realtion 
         #leftitemtypes = get_itemtypes()    #return the list of top level data items 
        relations = read_database()
        rendered_relations                = R.rendered_record_list(relations)
        empty_data_entry = R.rendered_itemtypes(-1,relations,leftitemtypes)
        configured_form = R.render_configured_form(empty_data_entry, nextstep="edit_items")
        return R.render_page(content=rendered_relations, dataentry=configured_form) 
                                                   
        
    if action == "edit_items":
        relations = read_database()
        #rendered_relations  = R.rendered_record_list(relations)  # need generalised RenderedRealtion here
        #os.sys.stderr.write(argd.get("form.leftid")+"\n")
        #os.sys.stderr.write(argd.get("form.rightid")+"\n")
        
        leftdbid = argd.get("form.leftid")
        rightdbid= argd.get("form.rightid")
        leftdb_key  = get_itemtype_key(leftdbid)
        rightdb_key = get_itemtype_key(rightdbid)
        relationid = -1
        #os.sys.stderr.write(leftdb_key+" "+rightdb_key+ "\n")
        leftdb = EntitySet(leftdbid,key=leftdb_key)
        rightdb = EntitySet(rightdbid,key=rightdb_key)
        #relation = RenderedRelation(R,leftdb, rightdb )
        available_relations = RenderedRelation(R, leftdb, rightdb)
        empty_data_entry = RenderedRelationEntryForm(relationid, leftdbid, rightdbid,leftdb_key,rightdb_key, leftdb, rightdb)
        #os.sys.stderr.write("empty data entry returned \n")
        #os.sys.stderr.write(repr(empty_data_entry))
        configured_form  = R.render_configured_item_form(empty_data_entry ,nextstep="create_new",submitlabel="Add Item")

        return R.render_page(content=available_relations, dataentry=configured_form)

    if action == "view_relation":
        relations = read_database()
        rendered_relations   = R.rendered_record_list(relations)
        relation = get_item(argd["relationid"])
        relation_pair = get_item_record_pair(relation)        
        rendered_relation_pair = RenderedRelationPair(R,relation, relation_pair)
        return R.render_page(content=rendered_relations, dataentry=rendered_relation_pair) 

   
    if action == "edit_relation":
        relations = read_database()
        rendered_relations   = R.rendered_record_list(relations)
        relation = get_item(argd["relationid"])
        relation_pair = get_item_record_pair(relation)
        rendered_relation_pair = RenderedRelationPair(R,relation, relation_pair)
        leftitemtypes = get_itemtypes() 
        empty_data_entry = R.rendered_itemtypes(argd["relationid"],relations, leftitemtypes)
        configured_form = R.render_configured_form(empty_data_entry, nextstep="update_items", submitlabel="Update Item", )
        return R.render_page(extra=rendered_relations ,content = rendered_relation_pair,  dataentry=configured_form) # rendered_relations , "pop") 

    if action == "create_new":
         #os.sys.stderr.write(argd.get("form.left_dbid")+"\n")
         #os.sys.stderr.write(argd.get("form.right_dbid")+"\n")
        rootid = None
        if argd.get("form.left_dbid")=="relationtrees": # now we handle building the tree
            parent_record = get_item_record("relationtrees", argd.get("form.left_itemid"))
            if  parent_record["left_dbid"]!="relationtrees":  # We are at the root node 
                 argd["form.root_id"] = parent_record["relationid"]
            else:                                             # child node
                 argd["form.root_id"] = parent_record["root_id"]
        else:
            argd["form.root_id"]=-1
 # Don't need to track back to root node just look at parent   
 # This will be handy for displaying the trees later.  
 #           while parent_record["left_dbid"]!=None and parent_record["left_dbid"]=="relationtrees": # find the root node
 #                       rootid=parent_record["root_id"] # set rootid to current root node
 #                       parent_record = get_item_record("relationtrees", parent_record["left_itemid"])                   
#                        if parent_record == None:      # root node has been deleted 
#                             argd["form.root_id"]=rootid
#                             break
#            if parent_record != None:           # this is the root 
#                        argd["form.root_id"]=parent_record["relationid"]
#            else:                               # use child root
#                        argd["form.root_id"]=rootid
#        else:
#            argd["form.root_id"]=-1
        new_relation = make_item(stem="form", **argd) # Also stores them in the database
        relations = read_database()
        rendered_relations   = R.rendered_record_list(relations)
        relation_pair = get_item_record_pair(new_relation)
        rendered_relation_pair = RenderedRelationPair(R,new_relation, relation_pair)
        #rendered_tuple = RenderedTuple(argd["__environ__"],"missionstepid", new_item["missionstepid"], ItemsDatabase, PeopleDatabase)
        rendered_relation_pair = "<B> Record Saved </B>. If you wish to update, please do" + str(rendered_relation_pair)
        #rendered_tuple = "<B> Record Saved </B>. If you wish to update, please do" + str(rendered_tuple)
        #relation = get_item(argd["relationid"])
        return R.render_page(content=rendered_relations, dataentry=rendered_relation_pair)

    
    if action == "delete_relation":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        # Show the database & a few options
        relations = read_database()
        rendered_relations   = R.rendered_record_list(relations)  # generalised Rendered Relation
        relation = get_item(argd["relationid"])
        relation_pair = get_item_record_pair(relation)
        rendered_relation_pair = RenderedRelationPair(R,relation, relation_pair)
        prebanner = "<h3> Are you sure you wish to delete this item</h3>"
        delete_action = "<a href='/cgi-bin/app/relationtrees?formtype=confirm_delete&relationid=%s'>%s</a>" % (relation["relationid"], "Delete this item")
        cancel_action = "<a href='/cgi-bin/app/relationtrees?formtype=view_relation&relationid=%s'>%s</a>" % (relation["relationid"], "Cancel deletion")

        delete_message = "%s <ul> %s </ul><h3> %s | %s </h3>" % (prebanner, str(rendered_relation_pair), delete_action, cancel_action)
        return R.render_page(content=rendered_relations, dataentry=delete_message)
        

    if action == "confirm_delete":
        relation = get_item(argd["relationid"])
        delete_item(argd["relationid"])
        relations = read_database()      # Show the database & a few options
        rendered_relations = R.rendered_record_list(relations)  # generalised Rendered Relation
        return R.render_page(content=rendered_relations,dataentry="<h1> Record %s Deleted </h1>" % argd["relationid"])


    if action == "update_items":
        relationid = argd.get("form.relationid")     
        relation = get_item(relationid)
        relation_pair = get_item_record_pair(relation)
        rendered_relation_pair = RenderedRelationPair(R,relation, relation_pair)
        relations = read_database()
        
        leftdbid = argd.get("form.leftid")
        rightdbid= argd.get("form.rightid")
        leftdb_key  = get_itemtype_key(leftdbid)
        rightdb_key = get_itemtype_key(rightdbid)
       
        #os.sys.stderr.write(leftdb_key+" "+rightdb_key+ "\n")
        leftdb = EntitySet(leftdbid,key=leftdb_key)
        rightdb = EntitySet(rightdbid,key=rightdb_key)
        available_relations = RenderedRelation(R, leftdb, rightdb)
        empty_ata_entry = RenderedRelationEntryForm(relationid, leftdbid, rightdbid,leftdb_key,rightdb_key, leftdb, rightdb)
        configured_form  = R.render_configured_item_form(empty_data_entry ,nextstep="update",submitlabel="Update Item")
        return R.render_page(content=available_relations, dataentry=configured_form)
         

    if action == "update":
        # Take the data sent to us, and use that to fill out an edit form
        #
        # Note: This is actually filling in an *edit* form at that point, not a *new* user form
        # If they submit the new form, the surely they should be viewed to be updating the form?
        # yes...
        #
        relation = get_item(argd.get("form.relationid"))
        #the_relation = update_relationt(stem="form", **argd)
        theitem = update_item(stem="form", **argd)
        relations = read_database()
        rendered_relations   = R.rendered_record_list(relations)  # generalised Rendered Relation
        
        relation_pair = get_item_record_pair(relation)
        rendered_relation_pair = RenderedRelationPair(R,theitem, relation_pair)
        rendered_tuple = "<B> Record Saved </B>. If you wish to update, please do" + str(rendered_relation_pair)

        return R.render_page(content=rendered_relations, dataentry= rendered_tuple)

    if action == "view_tree":
        relations = read_database()
        root_relation = get_item(argd["relationid"])
        current_tree = []
        for relation in relations:          #   only look at nodes in this tree
            if relation["root_id"]==root_relation["relationid"]:
                current_tree.append(relation) 
        this_tree = {}
        root_key = root_relation["relationid"]
        this_tree[root_key]=[]
        find_children(root_key,this_tree,current_tree)
        # os.sys.stderr.write(repr(this_tree)+"\n")
        render_tree = render_relation_tree(root_key,[],this_tree)
        # os.sys.stderr.write(repr(render_tree)+"\n")
        rendered_tree = R.rendered_record_list(render_tree)
        return R.render_page(content=rendered_tree)



#        tree.append(find_children(root_relation))        
#        while this_tree != []:
#            if these_roots != []:
#                for this_root in these_roots:
#                    for relation in this_tree:
#                        if relation["left_dbid"] == "relationtrees" and relation["left_itemid"] == this_root["relationid"]:
#                            os.sys.stderr.write(repr(relation)+"\n")
#                            
#                            this_tree.remove(relation)
#                level+=1
                 
            

                    
             
        



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
