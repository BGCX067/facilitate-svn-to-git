#!/usr/bin/python

import anydbm

import md5

class NoSuchUser(Exception): pass

cookiesFile = "/data/Cookies/Cookies.dbm"

def _newCookie(Cookies):
    try:
        highest = Cookies["meta:highest"]
    except KeyError:
        highest = "1"
    Cookies["meta:highest"] = repr(int(highest) + 1)
    return highest


def getCookie(userid):
    Cookies = anydbm.open(cookiesFile, "c")
    try:
       cookie = Cookies["user:"+userid]
    except KeyError:
       cookie = md5.md5(_newCookie(Cookies)).hexdigest()
       Cookies["user:"+userid] = cookie
       Cookies["cookie:"+cookie] = userid
    Cookies.close()
    return cookie
    
def getUser(cookie):
    Cookies = anydbm.open(cookiesFile, "c")
    try:
        user = Cookies["cookie:"+cookie]
    except KeyError:
        Cookies.close()
        raise NoSuchUser(cookie)
    Cookies.close()
    return user

def wipePairing(cookie,userid):
    Cookies = anydbm.open(cookiesFile, "c")
    try:
        Cookies["cookie:"+cookie]
        del Cookies["cookie:"+cookie]
    except KeyError:
       pass
    try:
        Cookies["user:"+userid]
        del Cookies["user:"+userid]
    except KeyError:
       pass
        
    Cookies.close()


def zapCookies():
    Cookies = anydbm.open(cookiesFile, "n")
    Cookies.close()

if __name__ == "__main__":
    # Basic acceptance test
    user = "0"
    cookie = getCookie("0")
    print cookie
    user_ = getUser(cookie)
    assert user_ == user
    print user_
    zapCookies()
    try:
        user_ = getUser(cookie)
        raise "Failed to zapCookies"
    except NoSuchUser:
        # Success
        pass
