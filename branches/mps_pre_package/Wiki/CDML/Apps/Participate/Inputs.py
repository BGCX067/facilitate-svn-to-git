#!/usr/bin/env python

import os.path

class tagHandler(object):

      def dotextinput(bunch, text, env):
          "textinput"
          labelcols = bunch.get("labelcols", "twoC")
          boxcols = bunch.get("boxcols", "twoC")
          name = bunch.get("name", "")
          defaultvalue = bunch.get("defaultvalue", "")
          labelbgcolor = bunch.get("labelbgcolor", "")
          label = text
          if name == "":
              return "textbox needs a name..."
          R = """<div class="column %(labelcols)s  %(labelbgcolor)s right">%(label)s&nbsp;</div>
          <div class="column  %(boxcols)s"><input type="text" name="%(name)s" class="%(boxcols)s" value="%(defaultvalue)s"></div>
          """ % { "name" : name,  
                  "label": label,
                  "labelcols" : labelcols,
                  "boxcols" : boxcols,
                  "labelbgcolor" : labelbgcolor,
                  "defaultvalue": defaultvalue,
                }
          
          return R

      def dohiddeninput(bunch, text, env):
          "textinput"
          name = bunch.get("name", "")
          defaultvalue = bunch.get("defaultvalue", text)
          label = ""
          if name == "":
              return "textbox needs a name..."
          R = """ <input type="hidden" name="%(name)s" value="%(defaultvalue)s"> """ % { 
                  "name" : name,  
                  "label": label,
                  "defaultvalue": defaultvalue,
                }
          
          return R

      def dopasswordinput(bunch, text, env):
          "passwordinput"
          labelcols = bunch.get("labelcols", "twoC")
          boxcols = bunch.get("boxcols", "twoC")
          name = bunch.get("name", "")
          defaultvalue = bunch.get("defaultvalue", "")
          labelbgcolor = bunch.get("labelbgcolor", "")
          label = text
          if name == "":
              return "textbox needs a name..."
          R = """<div style="clear: left" class="column %(labelcols)s  %(labelbgcolor)s right">%(label)s&nbsp;</div>
          <div class="column  %(boxcols)s"><input type="password" name="%(name)s" class="%(boxcols)s" value="%(defaultvalue)s"></div>
          """ % { 
                  "name" : name,  
                  "label": label,
                  "labelcols" : labelcols,
                  "boxcols" : boxcols,
                  "labelbgcolor" : labelbgcolor,
                  "defaultvalue": defaultvalue,
                }
          
          return R

      def dosubmitinput(bunch, text, env):
          "submitinput"
          label = text
          return """<div class="twoC"><input type="submit" class="twoC" name="submit" value='"""+label+"'> </div>"

      def doform(bunch, text, env):
          "form"
          form = """<form method="get" action="%(action)s" enctype="application/x-www-form-urlencoded">
          %(text)s
          </form>
          """ % { "text" : text,
                  "action" : bunch.get("action", ""),
                }
          return form

      def doprofilepicinput(bunch, text, env):
         return """
         <div class="column oneC right"><b>Pic</b>&nbsp;</div>
         <div class="threeC last"><input class="twoC" size="20" name="profilepic" value="browse" type="file"></div>
         <div class="divide"></div>"""

      def doimageupload(bunch, text, env):
          "textinput"
          labelcols    = bunch.get("labelcols",    "twoC")
          boxcols      = bunch.get("boxcols",      "twoC")
          name         = bunch.get("name",         "")
          defaultvalue = bunch.get("defaultvalue", "")
          labelbgcolor = bunch.get("labelbgcolor", "")
          label = text

          if name == "":
              return "textbox needs a name..."

          R = """<div class="column %(labelcols)s  %(labelbgcolor)s right">%(label)s&nbsp;</div>
          <div class="column  %(boxcols)s"><input type="text" name="%(name)s" class="%(boxcols)s" value="%(defaultvalue)s"></div>
          """ % { "name" : name,  
                  "label": label,
                  "labelcols" : labelcols,
                  "boxcols" : boxcols,
                  "labelbgcolor" : labelbgcolor,
                  "defaultvalue": defaultvalue,
                }
          
          return R




      def dodatespinner(bunch, text, env):
          name = bunch.get("name", "date")
          label = text
          return """\
         <div class="divide"></div>
         <div class="column oneC  right">%(label)s&nbsp;</div>
         <div class="fourC last">
            <select name="%(name)s.day">
                <option value="na">day</option>

                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>

                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option value="10">10</option>
                <option value="11">11</option>
                <option value="12">12</option>

                <option value="13">13</option>
                <option value="14">14</option>
                <option value="15">15</option>
                <option value="16">16</option>
                <option value="17">17</option>
                <option value="18">18</option>

                <option value="19">19</option>
                <option value="20">20</option>
                <option value="21">21</option>
                <option value="22">22</option>
                <option value="23">23</option>
                <option value="24">24</option>

                <option value="25">25</option>
                <option value="26">26</option>
                <option value="27">27</option>
                <option value="28">28</option>
                <option value="29">29</option>
                <option value="30">30</option>

                <option value="31">31</option>
            </select>

            <select name="%(name)s.month">
                <option value="na">month</option>
                <option value="January">January</option>
                <option value="February">February</option>

                <option value="March">March</option>
                <option value="April">April</option>
                <option value="May">May</option>
                <option value="June">June</option>
                <option value="July">July</option>
                <option value="August">August</option>

                <option value="September">September</option>
                <option value="October">October</option>
                <option value="November">November</option>
                <option value="December">December</option>
            </select>

            <select name="%(name)s.year">
                <option value="na">year</option>
                    <option value="1990">1990</option>
                    <option value="1989">1989</option>
                    <option value="1988">1988</option>
                    <option value="1987">1987</option>
                    <option value="1986">1986</option>

                    <option value="1985">1985</option>
                    <option value="1984">1984</option>
                    <option value="1983">1983</option>
                    <option value="1982">1982</option>
                    <option value="1981">1981</option>
                    <option value="1980">1980</option>

                    <option value="1979">1979</option>
                    <option value="1978">1978</option>
                    <option value="1977">1977</option>
                    <option value="1976">1976</option>
                    <option value="1975">1975</option>
                    <option value="1974">1974</option>

                    <option value="1973">1973</option>
                    <option value="1972">1972</option>
                    <option value="1971">1971</option>
                    <option value="1970">1970</option>
                    <option value="1969">1969</option>
                    <option value="1968">1968</option>

                    <option value="1967">1967</option>
                    <option value="1966">1966</option>
                    <option value="1965">1965</option>
                    <option value="1964">1964</option>
                    <option value="1963">1963</option>
                    <option value="1962">1962</option>

                    <option value="1961">1961</option>
                    <option value="1960">1960</option>
                    <option value="1959">1959</option>
                    <option value="1958">1958</option>
                    <option value="1957">1957</option>
                    <option value="1956">1956</option>

                    <option value="1955">1955</option>
                    <option value="1954">1954</option>
                    <option value="1953">1953</option>
                    <option value="1952">1952</option>
                    <option value="1951">1951</option>
                    <option value="1950">1950</option>

                    <option value="1949">1949</option>
                    <option value="1948">1948</option>
                    <option value="1947">1947</option>
                    <option value="1946">1946</option>
                    <option value="1945">1945</option>
                    <option value="1944">1944</option>

                    <option value="1943">1943</option>
                    <option value="1942">1942</option>
                    <option value="1941">1941</option>
                    <option value="1940">1940</option>
                    <option value="1939">1939</option>
                    <option value="1938">1938</option>

                    <option value="1937">1937</option>
                    <option value="1936">1936</option>
                    <option value="1935">1935</option>
                    <option value="1934">1934</option>
                    <option value="1933">1933</option>
                    <option value="1932">1932</option>

                    <option value="1931">1931</option>
                    <option value="1930">1930</option>
                    <option value="1929">1929</option>
                    <option value="1928">1928</option>
                    <option value="1927">1927</option>
                    <option value="1926">1926</option>

                    <option value="1925">1925</option>
                    <option value="1924">1924</option>
                    <option value="1923">1923</option>
                    <option value="1922">1922</option>
                    <option value="1921">1921</option>
                    <option value="1920">1920</option>

                    <option value="1919">1919</option>
                    <option value="1918">1918</option>
                    <option value="1917">1917</option>
                    <option value="1916">1916</option>
                    <option value="1915">1915</option>
                    <option value="1914">1914</option>

                    <option value="1913">1913</option>
                    <option value="1912">1912</option>
                    <option value="1911">1911</option>
                    <option value="1910">1910</option>
                    <option value="1909">1909</option>
                    <option value="1908">1908</option>

                    <option value="1907">1907</option>
                    <option value="1906">1906</option>
                    <option value="1905">1905</option>
                    <option value="1904">1904</option>
                    <option value="1903">1903</option>
                    <option value="1902">1902</option>

                    <option value="1901">1901</option>
                    <option value="1900">1900</option>
            </select>
         </div>
         <div class="divide"></div>
""" % {
         "label" : label,
         "name" : name,
      }

      def doradiobutton(bunch, text, env):
          return """
<div class="column twoC right"> <label for="isambard"> <img src="/images/isambard.png"></label> <br><input id="isambard" name="side" value="isambard" type="radio">  <label for="isambard"> Isambard </labeL></div>
<div class="column twoC right"> <label for="eve"><img src="/images/eve.png"></label> <br><input id="eve" name="side" value="eve" type="radio"> <label
for="eve">Eve</label> </div>
"""

      mapping = {
                 "textinput" : dotextinput,
                 "passinput" : dopasswordinput,
                 "submitinput" : dosubmitinput,
                 "profilepicinput" : doprofilepicinput,
                 "form" : doform,
                 "hiddeninput" : dohiddeninput,
                 "datespinner": dodatespinner,
                 "doradiobuttons" : doradiobutton,
     }
      
mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   print "HMM", tagHandler.mapping["w"]({"location":"bingle"}, "hello world", {})
