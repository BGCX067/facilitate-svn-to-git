#!/usr/bin/env python

import os.path

class tagHandler(object):

      def doshowpanel(bunch, text, env):
          "showpanel"
          panel = bunch.get("panel", None)
          if panel == None:
              return "No panel!"
          return env.get("participate.args.panels."+panel, text)

      def dopanel(bunch, text, env):
          "panel"
          panel = bunch.get("panel", None)
          if panel == None:
              return "No panel?"

          env["participate.args.panels."+panel] = text
          if bunch.get("debug", False):
               return "PANEL DONE "+"participate.args.panels."+panel+" "+text
          return ""

      def doshowleftpanel(bunch, text, env):
          "showleftpanel"
          return env.get("participate.args.leftpanel", "No leftpanel")

      def doshowrightpanel(bunch, text, env):
          "showrightpanel"
          return env.get("participate.args.rightpanel", text)

      def dorightpanel(bunch, text, env):
          "rightpanel"
          env["participate.args.rightpanel"] = text
          return ""

      def doleftpanel(bunch, text, env):
          "leftpanel"
          env["participate.args.leftpanel"] = text
          return ""

      def doaddrightpanel(bunch, text, env):
          "rightpanel"
          env["participate.args.rightpanel"] = env.get("participate.args.rightpanel", "") + text
          return ""

      def doaddleftpanel(bunch, text, env):
          "leftpanel"
          env["participate.args.leftpanel"] = env.get("participate.args.leftpanel", "") + text
          return ""

      def doblock(bunch, text, env):
          "block"
          format = bunch.get("format", None)
          if format is None:
               return text
          if format == "1t,6,1t":
               colour = bunch.get("colour", bunch.get("color",""))
               div_id = bunch.get("id", "")
               pre_p = bunch.get("pre_p", False)
               if pre_p:
                   pre_p="<P>"
               else:
                   pre_p=""
               if div_id != "":
                   div_id = 'id="%s"' % div_id
               RESULT = """<div class="column oneC">
                <P> &nbsp;
                </div>
                <div %(id)s class="column sixC %(color)s">%(pre_p)s
                %(text)s
                </div>
                <div class="column last oneC">
                <P> &nbsp;
                </div> """ % {"color" : colour, "text" : text, "id": div_id, "pre_p": pre_p }
               return RESULT


          if format == "2":
               colour = bunch.get("colour", bunch.get("color",""))
               last = bunch.get("colour", bunch.get("last",""))
               if last:
                   last = "last"
               div_id = bunch.get("id", "")
               pre_p = bunch.get("pre_p", False)
               if pre_p:
                   pre_p="<P>"
               else:
                   pre_p=""
               if div_id != "":
                   div_id = 'id="%s"' % div_id
               RESULT = """
                <div %(id)s class="column twoC %(last)s %(color)s">%(pre_p)s
                %(text)s
                </div> """ % {"color" : colour, "text" : text, "id": div_id, "pre_p": pre_p, "last" : last}
               return RESULT

          return text

      def dodivider(bunch, text, env):
          return """<div class='divide'></div>"""
      def dobutton(bunch, text, env):
          colour = bunch.get("colour", bunch.get("color","black"))
          align =  bunch.get("align", "right")
          klass =  bunch.get("class", "button")
          columns = bunch.get("columns", "twoC")
          if text == "":
              text == "&nbsp;"
          return """<div class="%(klass)s %(columns)s %(color)s %(align)s">%(text)s</div>""" % { "text" : text, 
                                                                                                 "color" : colour,
                                                                                                 "align" : align,
                                                                                                 "klass" : klass,
                                                                                                 "columns" : columns,
                                                                                               }

      mapping = {
                 "leftpanel"      : doleftpanel,
                 "rightpanel"     : dorightpanel,
                 "addleftpanel"   : doaddleftpanel,
                 "addrightpanel"  : doaddrightpanel,
                 "showpanel"      : doshowpanel,
                 "panel"          : dopanel,
                 "showrightpanel" : doshowrightpanel,
                 "showleftpanel"  : doshowleftpanel,
                 "block"          : doblock,
                 "button"         : dobutton,
                 "divider"         : dodivider,
      }
      
mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   print "HMM", tagHandler.mapping["w"]({"location":"bingle"}, "hello world", {})
