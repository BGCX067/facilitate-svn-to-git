#!/usr/bin/env  python

import os
import cjson

class EntitySet(object):
    data = "data"

#    @classmethod
    def Zap(cls, name="Demo", key="personid"):
        try:
            files = os.listdir(cls.data + "/" + name)
            for f in files:
                os.unlink( cls.data + "/" + name + "/" + f )

            os.removedirs(cls.data + "/" + name)

        except OSError, e:
            errno, err = e
            if errno != 2:
                raise
    Zap = classmethod(Zap)

    def __init__(self, name="Demo", key="personid"):
        self.meta = self.__get_meta(name=name, key=key)
        self.__get_records()

    def __get_records(self):
        records = []
        try:
            records = os.listdir(self.data+"/"+self.meta["name"])
        except OSError:
            os.makedirs(self.data+"/"+self.meta["name"])
            records = os.listdir(self.data+"/"+self.meta["name"])
        records = [ x for x in records if x != ".meta" ]
        return records

    def __get_meta(self, name="Demo", key="personid"):
        meta = {
            "highestid" : -1,
            "name" : name,
            "key" : key,
        }
        try:
            F = open(self.data + "/" + name + "/" + ".meta")
            serialised_meta = F.read()
            F.close()
            stored_meta = cjson.decode(serialised_meta)
            meta.update(stored_meta)
        except IOError:

            try:
                records = os.listdir(self.data+"/"+name)
            except OSError:
                os.makedirs(self.data+"/" + name)

            self.__store_meta(meta) # checkpoint

        return meta

    def __store_meta(self, meta=None):
        if meta is None:
            meta = self.meta

        F = file("%s/%s/%s" % (self.data, meta["name"], ".meta"), "w")
        serialised_meta = cjson.encode(meta)
        F.write(serialised_meta)
        F.close()

    def __newid(self):
        self.meta["highestid"] += 1
        self.__store_meta()
        return str(self.meta["highestid"])

    def key(self):
        return self.meta["key"]

    def new_record(self, json):
        # This is all hideously insecure :-)
        people = self.__get_records()

        filename = self.__newid()

        X = {}
        X.update(json)
        X[self.key()] = filename

        serialised_person = cjson.encode(X)

        F = file("%s/%s/%s" % (self.data, self.meta["name"], filename), "w")
        F.write(serialised_person)
        F.close()
        people = self.__get_records()
        return X

    def store_record(self, json):
        # This is all probably hideously insecure :-)
        filename = json[self.key()]
        serialised_person = cjson.encode(json)
        F = file("%s/%s/%s" % (self.data, self.meta["name"], filename), "w")
        F.write(serialised_person)
        F.close()


    def get_record(self, recordid):
        f = file("%s/%s/%s" % (self.data, self.meta["name"], recordid), "r")
        serialised_record = f.read()
        f.close()
        record = cjson.decode(serialised_record)
        return record

    def read_database(self):
        records = []
        people = self.__get_records()
        for person in people:
            records.append( self.get_record(person) )
        return records

    def delete_record(self, personid):
        os.unlink("%s/%s/%s" % (self.data, self.meta["name"], personid))

if __name__ == "__main__":
    for set in ["Add","res","ses"]:
        P = EntitySet(set)
        for person in people:
            P.new_record(person)
            print person

        print P.read_database()


if 0:
    def _____new_record(self, json):
        # This is all hideously insecure :-)
        people = self.__get_records()
        serialised_person = cjson.encode(json)

        filename = str(len(people))

        F = file("%s/%s/%s" % (self.data, self.meta["name"], filename), "w")
        F.write(serialised_person)
        F.close()
        people = self.__get_records()
        return filename   # Latest Person id


    def ______store_record(self, json):
        # This is all hideously insecure :-)
        filename = json[self.key()]
        del json[self.key()]        # This is a tad nasty really
        serialised_person = cjson.encode(json)
        F = file("%s/%s/%s" % (self.data, self.meta["name"], filename), "w")
        F.write(serialised_person)
        F.close()
        json[self.key()] = filename

    def ____get_record(self, person):
        F = file("%s/%s/%s" % (self.data, self.meta["name"], person), "r")
        serialised_record = F.read()
        F.close()
        record = cjson.decode(serialised_record)
        record[self.key()] = person
        return record
