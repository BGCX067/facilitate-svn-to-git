#!/usr/bin/env python

import Facilitate.model.Record as Record

import sys

import unittest

class Test_Record_new_record(unittest.TestCase):
    def setUp(self):
        self.key = "personid"

        Record.EntitySet.Zap(name="People", key=self.key)
        self.X = Record.EntitySet(name="People", key=self.key)

    # --------------------------------------------------------------

    def test_new_record(self):
        "Record.new_record - Adding a record should result in us being given the record back, preserving our values and with an id added "
        newrec = self.X.new_record({"name": "bob", "age": 30})
        self.assertEqual(newrec["name"], "bob")
        self.assertEqual(newrec["age"], 30)

    def test_new_record_personid_startsZero(self):
        "Record.new_record - records returned contain key values that start at 0 upwards - keys returned are strings"
        newrec = self.X.new_record({"name": "bob", "age": 30})
        self.assertEqual(newrec["personid"], "0")

    def test_new_record_personid_DuplicatesAllowedStoredSeperately(self):
        "Record.new_record - creating new records, even duplicating existing content, creates a new record"
        newrec1 = self.X.new_record({"name": "John Smith", "age": 30})
        newrec2 = self.X.new_record({"name": "John Smith", "age": 30}) # Because there can easily be two John Smiths aged 30
        self.assertNotEqual(newrec1["personid"], newrec2["personid"])

    def test_new_record_personid_startZeroIncreasing(self):
        "Record.new_record - keys returned increase numerically from 0 upwards"
        newrec = self.X.new_record({"name": "bob", "age": 1})
        self.assertEqual(newrec["personid"], "0")
        newrec = self.X.new_record({"name": "bob", "age": 1})
        self.assertEqual(newrec["personid"], "1")
        newrec = self.X.new_record({"name": "bob", "age": 1})
        self.assertEqual(newrec["personid"], "2")
        newrec = self.X.new_record({"name": "bob", "age": 1})
        self.assertEqual(newrec["personid"], "3")

    def test_new_record_DifferingRecordsDiffer(self):
        "Record.new_record - storing different records, remain different"
        rec_raws = [
                      {"name": "alice",   "age": "30"},
                      {"name": "bob",     "age": "31"},
                      {"name": "charlie", "age": "32"},
                      {"name": "dan",     "age": "33"},
                  ]
        newrecs = []

        for source in rec_raws:
            newrec = self.X.new_record( source )
            newrecs.append( newrec )

        for left,right in zip(rec_raws, newrecs):
            self.assertEqual( left["name"], right["name"] )
            self.assertEqual( left["age"], right["age"] )

class Test_Record_get_record(unittest.TestCase):
    def setUp(self):
        self.key = "personid"

        Record.EntitySet.Zap(name="People", key=self.key)
        self.X = Record.EntitySet(name="People", key=self.key)

    def test_get_record_onerecord(self):
        "Record.get_record - add record, get same record, should give same record."
        newrec = self.X.new_record({"name": "bob", "age": 30})
        self.assertEqual(newrec["personid"], "0")

        stored_rec = self.X.get_record("0")
        self.assertEqual( newrec["name"], stored_rec["name"] )
        self.assertEqual( newrec["age"], stored_rec["age"] )
        self.assertNotEqual( id(newrec), id(stored_rec) )

    def test_get_record_multiplerecords(self):
        "Record.get_record - add multiple records, get back records, should be same records "
        rec_raws = [
                      {"name": "alice",   "age": "30"},
                      {"name": "bob",     "age": "31"},
                      {"name": "charlie", "age": "32"},
                      {"name": "dan",     "age": "33"},
                  ]
        newrecs = []

        for i in rec_raws:
            self.X.new_record( i )

        for i in "0", "1", "2", "3":
             newrecs.append( self.X.get_record( i ) )

        for left,right in zip(rec_raws, newrecs):
            self.assertEqual( left["name"], right["name"] )
            self.assertEqual( left["age"], right["age"] )

    def test_get_record_multiplerecords_differentorder(self):
        "Record.get_record - add multiple records, get back records, should be same records "
        rec_raws = [
                      {"name": "alice",   "age": "30"},
                      {"name": "bob",     "age": "31"},
                      {"name": "charlie", "age": "32"},
                      {"name": "dan",     "age": "33"},
                  ]
        expected_recs = [
                    rec_raws[3], rec_raws[1], rec_raws[0], rec_raws[2],
                  ]
        newrecs = []

        for i in rec_raws:
            self.X.new_record( i )

        for i in "3", "1", "0", "2":
             newrecs.append( self.X.get_record( i ) )

        for left,right in zip(expected_recs, newrecs):
            self.assertEqual( left["name"], right["name"] )
            self.assertEqual( left["age"], right["age"] )

class Test_Record_update_record(unittest.TestCase):
    def setUp(self):
        self.key = "personid"

        Record.EntitySet.Zap(name="People", key=self.key)
        self.X = Record.EntitySet(name="People", key=self.key) # Put stuff in here
        self.Y = Record.EntitySet(name="People", key=self.key) # Check here
                                                               # Assumption that these are different :-)

    def test_UpdateOneRecord(self):
        "Record - update record. Create records. Get one, update it, store it, get it & check changed"
        rec_raws = [
                      {"name": "alice",   "age": "30"},
                      {"name": "bob",     "age": "31"},
                      {"name": "charlie", "age": "32"},
                      {"name": "dan",     "age": "33"},
                  ]

        for i in rec_raws:
            self.X.new_record( i )

        rec = self.X.get_record("2")
        rec["age"] = str(int(rec["age"])+1)

        self.X.store_record( rec )

        rec = self.Y.get_record("2")
        self.assertEqual( rec_raws[2]["name"], rec["name"])
        self.assertNotEqual( rec_raws[2]["age"], rec["age"])
        self.assertEqual( "33", rec["age"])

    def test_UpdateMultipleRecords(self):
        "Record - update many records. Create records. Get one, update it, store it, get it & check changed"
        rec_raws = [
                      {"name": "alice",   "age": "30"},
                      {"name": "bob",     "age": "31"},
                      {"name": "charlie", "age": "32"},
                      {"name": "dan",     "age": "33"},
                  ]

        for i in rec_raws:
            self.X.new_record( i )

        rec = self.X.get_record("0")
        rec["age"] = "21"
        rec["name"] = "alice smith"
        self.X.store_record( rec )

        rec = self.X.get_record("1")
        rec["age"] = "29"
        rec["name"] = "bob smith"
        self.X.store_record( rec )

        rec = self.X.get_record("2")
        rec["age"] = "40"
        rec["name"] = "charlie frank"
        self.X.store_record( rec )

        rec = self.X.get_record("3")
        rec["age"] = "41"
        rec["name"] = "dan frank"
        self.X.store_record( rec )

        rec = self.Y.get_record("0")
        self.assertEqual(rec["name"], "alice smith")
        self.assertEqual( rec["age"], "21")

        rec = self.Y.get_record("1")
        self.assertEqual(rec["name"], "bob smith")
        self.assertEqual( rec["age"], "29")


        rec = self.Y.get_record("2")
        self.assertEqual(rec["name"], "charlie frank")
        self.assertEqual( rec["age"], "40")


        rec = self.Y.get_record("3")
        self.assertEqual(rec["name"], "dan frank")
        self.assertEqual( rec["age"], "41")


class Test_Record_readDB(unittest.TestCase):
    def setUp(self):
        self.key = "personid"

        Record.EntitySet.Zap(name="People", key=self.key)
        self.X = Record.EntitySet(name="People", key=self.key) # Put stuff in here
        self.Y = Record.EntitySet(name="People", key=self.key) # Check here

    def test_readBD_oneRecord(self):
        newrec = self.X.new_record({"name": "bob", "age": 1})
        records = self.Y.read_database()
        self.assertEqual(len(records), 1)
        self.assert_( newrec in records )


    def test_readBD_manyRecords(self):
        rec_raws = [
                      {"name": "alice",   "age": "30"},
                      {"name": "bob",     "age": "31"},
                      {"name": "charlie", "age": "32"},
                      {"name": "dan",     "age": "33"},
                  ]
        recs = []

        for i in rec_raws:
            recs.append( self.X.new_record( i ) )

        records = self.Y.read_database()
        
        for rec in recs:
            self.assert_( rec in records )

class Test_Record_deleteRecord(unittest.TestCase):
    def setUp(self):
        self.key = "personid"

        Record.EntitySet.Zap(name="People", key=self.key)
        self.X = Record.EntitySet(name="People", key=self.key) # Put stuff in here
        self.Y = Record.EntitySet(name="People", key=self.key) # Check here

    def test_addonedeleteone(self):
        "Record.delete_record - add a record and delete it, confirm gone and empty set"
        newrec = self.X.new_record({"name": "bob", "age": 1})
        self.X.delete_record( "0" )
        records = self.Y.read_database()
        self.assertEqual(len(records), 0)

    def test_delete_addManyDeleteOne(self):
        "Record.delete_record - add man records, delete one."
        rec_raws = [
                      {"name": "alice",   "age": "30"},
                      {"name": "bob",     "age": "31"},
                      {"name": "charlie", "age": "32"},
                      {"name": "dan",     "age": "33"},
                  ]
        recs = []
        for i in rec_raws:
            self.X.new_record( i )
        
        records = self.Y.read_database()
        self.assertEqual(len(records), 4)
        equalCount = 0
        for record in records:
            if record["name"] == "charlie":
                equalCount += 1
        self.assertEqual( equalCount, 1 )
        
        self.X.delete_record( "2" )
        
        records = self.Y.read_database()
        self.assertEqual(len(records), 3)
        
        for record in records:
            self.assertNotEqual( "charlie", record["name"] )

    def test_delete_addManyDeleteAll(self):
        "Record.delete_record - add man records, delete one."
        rec_raws = [
                      {"name": "alice",   "age": "30"},
                      {"name": "bob",     "age": "31"},
                      {"name": "charlie", "age": "32"},
                      {"name": "dan",     "age": "33"},
                  ]
        recs = []
        for i in rec_raws:
            self.X.new_record( i )
        
        records = self.Y.read_database()
        self.assertEqual(len(records), 4)

        for key in [ "0", "1", "2", "3" ]:
            self.X.delete_record( key )
        
        records = self.Y.read_database()
        self.assertEqual(len(records), 0)

class Test_Record_key(unittest.TestCase):
    def setUp(self):
        self.key = "personid"

        Record.EntitySet.Zap(name="People", key=self.key)
        self.X = Record.EntitySet(name="People", key=self.key)

    def test_delete_addManyDeleteAll(self):
        "Record.key - returns the key for this entity"
        self.assertEqual(self.key, self.X.key() )

class Test_Record_Zap(unittest.TestCase):
    def setUp(self):
        self.key = "personid"

        Record.EntitySet.Zap(name="People", key=self.key)
        self.X = Record.EntitySet(name="People", key=self.key)
        
    def test_repeatedZapAfterAddingResetsKeyToZero(self):
        Record.EntitySet.Zap(name="People", key=self.key)
        X = Record.EntitySet(name="People", key=self.key)

        newrec1 = X.new_record( {"name": "alice",   "age": "30"} )

        Record.EntitySet.Zap(name="People", key=self.key)
        X = Record.EntitySet(name="People", key=self.key)
        newrec2 = X.new_record( {"name": "alice",   "age": "30"} )

        
        Record.EntitySet.Zap(name="People", key=self.key)
        X = Record.EntitySet(name="People", key=self.key)
        newrec3 = X.new_record( {"name": "alice",   "age": "30"} )
        
        self.assertEqual( newrec1[self.key] , newrec2[self.key] )
        self.assertEqual( newrec2[self.key] , newrec3[self.key] )
        


if __name__=="__main__":
    # Next line invokes voodoo magic that causes all the testcases above to run.
    unittest.main()
      
