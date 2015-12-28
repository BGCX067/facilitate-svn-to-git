#!/usr/bin/python


class MimeDict(dict):
   def __init__(self, **args):
      super(MimeDict,self).__init__(**args)
      self.insertionorder = []
      self.invalidSource = False
      # This is HIDEOUS
      for k in self.keys():
         if isinstance(self[k], list):
            if self[k] == []:
                self.insertionorder.append(k)
            else:
               for i in self[k]:
                  self.insertionorder.append(k)
         else:
            self.insertionorder.append(k)
      try:
         self["__BODY__"]
      except KeyError:
         self["__BODY__"] = ""

   def __setitem__(self,i,y):
      super(MimeDict, self).__setitem__(i,y)
      if i != "__BODY__":
           self.insertionorder = [ x for x in self.insertionorder if x != i ]
           if isinstance(y,list):
              for _ in y:
                 self.insertionorder.append(i)
           else:
              self.insertionorder.append(i)

   def __delitem__(self,y):
      self.insertionorder = [ x for x in self.insertionorder if x != y ]
      super(MimeDict, self).__delitem__(y)

   def __str__(self):
      # This is HIDEOUS
      result = []

      seen = {}
      for k in self.insertionorder:
         if k == "__BODY__": continue
         try:
            seen[k] += 1
         except KeyError:
            seen[k] = 0
         if isinstance(self[k], list):
            try:
               value = self[k][seen[k]]
            except IndexError: # Empty list, empty value
               value = ""
         else:
            value = self[k]
         try:
            trailing_chars = value[-2:]
         except TypeError, t:
            value = ""
         else:
            if trailing_chars == "\r\n":
               value = value + "   " # Add some spaces so that the trailing new line is preserved

         result.append("%s: %s\r\n" % (k,value))

      result.append("\r\n")
      result.append(self["__BODY__"])
      resultString = "".join(result)
      if self.invalidSource:
         return resultString[2:]
      else:
         return resultString

   def fromString(source):
      import sre
      result = {}
      insertionorder = []
      fail = False
      originalsource = source # preserve original in case of broken header
      headervalueRE_sX = "^([^: ]+[^:]*):( ?)((.|\n)+)" # TODO: This could be optimised

      lines = source.split("\r\n")
      I = 0
      headerLines = []
      valid = False
      for I in xrange(len(lines)):
          if lines[I] != "":
             headerLines.append(lines[I])
          else:
             # The divider cannot be the last line
             valid = not (I == len(lines)-1)
             break

      if not valid:
          body = originalsource
          fail = True
      else:
          bodyLines = lines[I+1:]
          body = "\r\n".join(bodyLines)
          key = None
          for line in headerLines:
             match = sre.search(headervalueRE_sX, line)
             if match:
                (key, spaces,value,X) = match.groups()
                if value == " " and not spaces:
                   value = ""
                try:
                   result[key].append(value)
                except KeyError:            
                   result[key] = value
                except AttributeError:
                   result[key] = [ result[key], value ]
                insertionorder.append(key)

             else:
                if key:
#                       value = line.strip() # Strictly speaking, surely we should be doing this??? (Breaks tests though if we do...)
                       value = line
                       if isinstance(result[key], list):
                          # Append to last item in the list
                          result[key][len(result[key])-1] += "\r\n" + value
                       else:
                          result[key] += "\r\n" + value
                else:
#                    print "NOMATCH!NOMATCH!NOMATCH!NOMATCH!NOMATCH!NOMATCH!"
                    fail = True
                    break
      if not fail:
          result["__BODY__"]=body
      else:
          result["__BODY__"]=originalsource
      md = MimeDict(**result)
      md.insertionorder = insertionorder
      md.invalidSource = fail
      return md
   fromString = staticmethod(fromString)
 