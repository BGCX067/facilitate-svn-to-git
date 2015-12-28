#!/usr/bin/python

import unittest

import Facilitate.model.Record
from Facilitate.model.Record import EntitySet
import Facilitate.SimpleResponse as SR

class SimpleResponseTest(unittest.TestCase):
    def setUp(self):
        EntitySet.Zap("simpleresponses", key="responseid")
        self.X = EntitySet(name="simpleresponses", key="responseid")
        SR.SimpleResponses = self.X # Necessary due to design flaw in SimpleResponse (being practical about it)

    def test_defaultResponse1(self):
        "Facilitate.SimpleResponse.page_logic - called with junk responds with default response"
        argd = {}
        expect = ['__default__', {'record': {}, 'message': "Please don't send junk"+repr(argd) }]

        X = SR.page_logic(None)
        self.assertEqual(expect, X)

    def test_defaultResponse2(self):
        "Facilitate.SimpleResponse.page_logic - called with junk & empty *argd responds with default response"
        json = None
        argd = {}
        expect = ['__default__', {'record': {}, 'message': "Please don't send junk"+repr(argd) }]

        X = SR.page_logic(json, **argd)
        self.assertEqual(expect, X)

    def test_defaultResponse3(self):
        "Facilitate.SimpleResponse.page_logic - called with action=junk (ie junk action) results with default response "
        json = None
        argd = {"action" : "junk"}
        expect = ['__default__', {'record': {}, 'message': "Please don't send junk"+repr(argd) }]

        X = SR.page_logic(json, **argd)
        self.assertEqual(expect, X)

    def test_defaultResponse4(self):
        "Facilitate.SimpleResponse.page_logic - called with action=submitresponse, but nothing else causes error to be raised"
        json = None
        argd = {"action" : "submitresponse"}
        
        X = SR.page_logic(json, **argd)
        self.assertEqual( X[0], "error")

    def test_defaultResponse5(self):
        "Facilitate.SimpleResponse.page_logic - called with action=submitresponse, missing response causes response error"
        json = None
        argd = {"action" : "submitresponse"}
        expect = ['error', {'record': '', 'message': 'You really ought to fill in a response to the form you know!', 'problemfield': 'response'}]

        X = SR.page_logic(json, **argd)
        self.assertEqual( X, expect)
        self.assertEqual( X[1]["problemfield"], "response")

    def test_defaultResponse6(self):
        "Facilitate.SimpleResponse.page_logic - called with action, response, but missing type results in error"
        json = None
        argd = {"action" : "submitresponse", "response" : "a" }

        X = SR.page_logic(json, **argd)
        self.assertEqual( X[0], "error")

    def test_defaultResponse7(self):
        "Facilitate.SimpleResponse.page_logic - called with action, response, but missing type results in error - type error"
        json = None
        argd = {"action" : "submitresponse", "response" : "a"}

        expect = ['error', {'record': '', 'message': 'Response type not set, did something go wrong?', 'problemfield': 'type'}]

        X = SR.page_logic(json, **argd)
        self.assertEqual( X, expect)
        self.assertEqual( X[1]["problemfield"], "type")

    def test_defaultResponse8(self):
        "Facilitate.SimpleResponse.page_logic - called with action, response, type but missing mission results in error"
        json = None
        argd = {"action" : "submitresponse", "response" : "a", "type": "mcq" }

        X = SR.page_logic(json, **argd)
        self.assertEqual( X[0], "error")

    def test_defaultResponse9(self):
        "Facilitate.SimpleResponse.page_logic - called with action, response, type but missing mission results in error - mission error"
        json = None
        argd = {"action" : "submitresponse", "response" : "a", "type": "mcq" }

        expect = ['error', {'record': '', 'message': 'Mission ID not set, did something go wrong?', 'problemfield': 'mission'}]

        X = SR.page_logic(json, **argd)
        self.assertEqual( X, expect)
        self.assertEqual( X[1]["problemfield"], "mission")

    def test_defaultResponse10(self):
        "Facilitate.SimpleResponse.page_logic - called with action, response, type, mission but missing userid results in error"
        json = None
        argd = {"action" : "submitresponse", "response" : "a", "type": "mcq", "mission" : "1" }

        X = SR.page_logic(json, **argd)
        self.assertEqual( X[0], "error")

    def test_defaultResponse11(self):
        "Facilitate.SimpleResponse.page_logic - called with action, response, type, mission but missing userid results in error - userid error"
        json = None
        argd = {"action" : "submitresponse", "response" : "a", "type": "mcq", "mission" : "1" }
        expect = ['error', {'record': '', 'message': 'User ID not set, did something go wrong?', 'problemfield': 'userid'}]

        X = SR.page_logic(json, **argd)
        self.assertEqual( X, expect)
        self.assertEqual( X[1]["problemfield"], "userid")

    def test_defaultResponse12(self):
        "Facilitate.SimpleResponse.page_logic - called with all fields, but no matching rule, results in default 'thank you' response"

        json = None
        argd = {"action" : "submitresponse", "response" : "a", "type": "mcq", "mission" : "1", "userid": "1" }
        default_thankyou = ['responsestored', {'message': "Thanks for the response, it's been safely stored!",
                                               'rulematch' : "__default__"}]

        X = SR.page_logic(json, **argd)
        self.assertEqual( X[0], "responsestored")
        self.assertEqual( X[1]["rulematch"], "__default__")

class ComplextResponses(unittest.TestCase):
    def test_defaultResponse1(self):
        self.fail("Now we have support for matching rules, we need to add that code in and handle updating")
if __name__=="__main__":
    # Next line invokes voodoo magic that causes all the testcases above to run.
    unittest.main()
