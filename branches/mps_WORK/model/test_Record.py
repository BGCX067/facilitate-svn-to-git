#!/usr/bin/env python

import Record

Record.EntitySet.Zap(name="People", key="personid")
X = Record.EntitySet(name="People", key="personid")
X = Record.EntitySet(name="People", key="personid") # should not fail!

if 0:
    # basic test
    newrec = X.new_record({"name": "michael", "age": 34})
    print newrec

if 1:
    # common tests
    rec_raw = [
                {"name": "michael", "age": "34"},
                {"name": "polina", "age": "35"},
                {"name": "sam", "age": "5"},
                {"name": "nat", "age": "4"},
              ]
    recs_new = [ ]

    for rec in rec_raw:
        newrec = X.new_record(rec)
        print newrec
        recs_new.append(newrec)

    print recs_new

    print recs_new[2]

    recs_new[2]["name"] = "sam sparks"
    X.store_record(recs_new[2])

    print recs_new

    record = X.get_record("3")

    print "Record","3", record

    for myrec in X.read_database():
        print "R", myrec


