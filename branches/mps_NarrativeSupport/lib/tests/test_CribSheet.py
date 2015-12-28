#!/usr/bin/python
#
# running this as "test_CribSheet.py -v "
# - gives you some cribsheet docs on what's going on and runs all the tests
#
# running this as "./test_CribSheet.py -v LikeCycleOfATest"
# - allows you to just run one of the suites.
#
# This doesn't replace documentation, and there's probably some hidden
# assumptions here, but it's quite useful.
#

import unittest
import os

class DemoDocStringsImpact(unittest.TestCase):
    # Note that the next test doesn't have a doc string. Look at the results in -v
    def test_DefaultVerboseMessage(self):
        pass

    # Note that the next test does have a doc string. Look at the results in -v
    def test_NonDefaultVerboseMessage(self):
        "This message will be shown in -v"
        pass

class LikeCycleOfATest(unittest.TestCase):

    def setUp(self):
        "We get called before every test_ in this class"
        self.value = 2

    def test_test1(self):
        "LifeCycle : 1 - we get called after setUp, but before tearDown"
        self.assertNotEqual(1, self.value)
        self.value = 1

    def test_test2(self):
        """LifeCycle : 2 - self.value wiped from previous test case
        - this is because setUp & tearDown are called before/after every test"""
        self.assertNotEqual(1, self.value)

    def tearDown(self):
        "We get called before *every* test_ in this class"
        # We could for example close the file used by every test, or close
        # a database or network connection

class Escape_tests(unittest.TestCase):

    def test_NullTest1(self):
        "assertNotEquals - fails with AssertionError if Equal"
        self.assertNotEqual(1, 2)

    def test_NullTest2(self):
        "assertEquals  - fails with AssertionError if not Equal"
        self.assertEqual(1, 1)

    def test_NullTest3(self):
        "assertEquals, custom error message -  - fails with AssertionError + custom message if not Equal"
        self.assertEqual(1, 1, "If you see this, the test is broken")

    def test_CallsSelfFailShouldBeCaughtByAssertionError(self):
        "self.fail - fail with AssertionError + custom message - useful for failing if an assertion does not fire when it should"
        try:
            self.fail("Fail!")
        except AssertionError:
            pass

    def test_NullTest4(self):
        "assert_ - for those times when you just want to assert something as try. Can have a custom message"
        self.assert_(1 ==1 , "one and one is two...")

    def test_NullTest5(self):
        "fail unless - This is essentially the same as self.assert_ really"
        self.failUnless(1 ==1)

    def test_NullTest6(self):
        "fail unless - code for this shows how to catch the Assertion error"
        try:
            self.failUnless(1 !=1 )
        except AssertionError:
            pass

    def test_NullTest7(self):
        "fail unless - how to extract the error message"
        try:
            self.failUnless(1 !=1, "Looks like the test is wrong!")
        except AssertionError, e:
            self.assert_(e.message == "Looks like the test is wrong!")

    def test_NullTest8(self):
        "assertRaises - can be useful for checking boundary cases of method/function calls."
        def LegendaryFail():
             1/0
        self.assertRaises(ZeroDivisionError, LegendaryFail)

    def test_NullTest9(self):
        "failUnlessRaises - can be useful for checking boundary cases of method/function calls. - can also pass in arguments"
        def LegendaryFail(left, right):
             left/right
        self.failUnlessRaises(ZeroDivisionError, LegendaryFail,1,0)


    def test_NullTest10(self):
        "assertRaises - how to simulate this so your assertion error can get a custom message"
        def LegendaryFail(left, right):
             left/right
        try:
            LegendaryFail(1,0)
            self.fail("This would fail here is LegendaryFail did not raise a ZeroDivisionError")
        except ZeroDivisionError:
            pass


if __name__=="__main__":
    # Next line invokes voodoo magic that causes all the testcases above to run.
    unittest.main()
