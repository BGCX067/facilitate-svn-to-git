#!/usr/bin/python

from Lexer import parser
import os
import sys

ENV = {}

def noTag(bunch, text, env):
   return text

class CDML(object):
    CDML_TAGS = {}
    CDML_TYPES = {}

    def __init__(self, config):
        self.config = config

    def getModules(self, path = "CDML/Handlers"):
        handlers = []
        for x in os.listdir(path):
            if x[-3:] ==".py" and x !="__init__.py":
                handlers.append(x[:-3])
        modules =  [ __import__("CDML.Handlers."+ str(H),[],[],[""]) for H in handlers ]

        handlers = []
        for app in os.listdir("CDML/Apps/"):
            if not os.path.isdir("CDML/Apps/"+app+"/"):
                continue
            for x in os.listdir("CDML/Apps/"+app+"/"):
               if x[-3:] ==".py" and x !="__init__.py":
                   handlers.append((app,x[:-3]))
        modules = modules + [ __import__("CDML.Apps."+ str(app)+"."+str(H),
                                         [],[],[""]) for app, H in handlers ]
        return modules

    def addHandlers(self, CDML_TAGS, modules):
        for Module in modules:
            Module.evalTree = self.evalTree
            Module.parser = parser
            CDML_TAGS.update(Module.mapping)

    def doElse(self, data):
       return data[0]

    def doTag(self, data):
       bunch,text = {},""
       tag = data[0]
       rest = data[1:]
       for i in rest[0]: # rest is a list containing a single list of atoms
          if i[0] == "attr_value":
             bunch[i[1].lower()] = i[2]
          else: # Anything else
             handler = self.getTopHandler(i[0].lower())
             result = handler(self, i[1:])
             text += result
       handler = self.getTagHandler(data[0].lower())
       ENV.update(self.config)
       return handler(bunch, text, ENV)

    CDML_TYPES["else"] = doElse
    CDML_TYPES["tag"] = doTag

    def getTagHandler(self, item):
       try:
          return CDML.CDML_TAGS[item]
       except KeyError:
         return noTag

    def getTopHandler(self, item):
       try:
          return CDML.CDML_TYPES[item]
       except KeyError:
          return CDML.CDML_TYPES["else"]
      
    def evalTree(self, tree, d=0):
        if isinstance(tree[0], str):
           handler = self.getTopHandler(tree[0])
           if tree[0]=="tag" and False:
               print "Content-Type: text/plain\n\n"
               print tree
           yield handler(self, tree[1:])
        else:
           for atom in tree:
              for i in self.evalTree(atom,d=d+1):
                 yield i


X = CDML({})
modules = X.getModules("CDML/Handlers")
X.addHandlers(CDML.CDML_TAGS, modules)

# evalTree = X.evalTree

if __name__ == "__main__":
   source = """
<a href='bla bla bla'>This is some</a> text
[[HREF][location=hello][STYLE=newlink] [[HREF][location=bingle] foo] that]
and more text """

   print "".join([x for x in evalTree(parser(source))])
