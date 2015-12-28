#!/usr/bin/python
#
#
tokens = ( 'ESCAPEDBRA', 'BRA', 'BRABRA', 'EQUALS', 'KET',"ELSE", )

#f = open("/tmp/parse.txt", "wb")

def t_ESCAPEDBRA(t):
    r'\\\['
#    print t
    t.type = "ELSE"
    return t

t_BRA    = r'\['
t_BRABRA = r'\[\['
t_KET    = r'\]'
t_EQUALS = r'\='
def t_ELSE(t):
    r'[^\[\]\=]+'
    if t.value == r"\\\[":
       t.value = r"\["

#    t_ = t.__class__()
#    t_.type = t.type
#    t_.lineno = t.lineno
#    print t.__class__.__doc__
#    print t
    return t


#t_ELSE   = r'([^\[\]\=]+|\\\[)'

def t_error(t):
#    print "Illegal character '%s'" % t.value[0]
#    print "Illegal character ", ord(t.value[0])

    t.skip(1)

# Build the lexer
import lex
lex.lex()

source = """
[[this]junk
[theother=something]the text
 to be marked u
p[another=thingy]junk
]
"""

lex.input(source)
if 0:
   while 1:
      token = lex.token()
      if not token:
         break
#      print "TOKEN", token

#
###############################################################################################################################
#
# Parsing rules

precedence = (
# ('left','PLUS','MINUS')
    )

# dictionary of names
names = { }

def p_text(p):
    '''text : termlist'''
    p[0]=p[1]

def p_termlist_1(p):
    '''termlist : term'''
    p[0]=[p[1]]

def p_termlist_2(p):
    '''termlist : term termlist'''
    p[0]=[p[1]]+p[2]

def p_term_1(p):
    '''term : elselist '''
    p[0]= p[1]

def p_elselist_1(p):
    '''elselist : else '''
    p[0]= [p[1]]

def p_elselist_2(p):
    '''elselist : else elselist'''
    p[0]= [p[1]]+p[2]

def p_else_1(p):
    '''else : ELSE '''
    p[0]= ["else", p[1]]

def p_else_2(p):
    '''else : EQUALS '''
    p[0]= ["else", p[1]]

def p_term_2(p):
    '''term : hint'''
    p[0]= p[1]

def p_hint_1(p):
    '''hint : BRA ELSE KET'''
    p[0]= ["hint", p[1]+p[2]+p[3]]

def p_hint_2(p):
    '''hint : BRA ELSE EQUALS ELSE KET'''
    p[0]= ["attr_value", p[2],p[4]]

def p_hint_3(p):
    '''hint : BRA KET '''
    p[0]= ["hint", p[1]+p[2]]


def p_term_3(p):
    '''term : tag'''
    p[0]= p[1]

def p_tag_1(p):
    '''tag : BRABRA ELSE KET tagcontentlist KET'''
    p[0]= ["tag", p[2],p[4]]

def p_tagcontentlist_1(p):
    '''tagcontentlist : tagcontent'''
    p[0]=[p[1]]

def p_tagcontentlist_2(p):
    '''tagcontentlist : tagcontent tagcontentlist'''
    p[0]=[p[1]]+p[2]

def p_tagcontent_1(p):
    '''tagcontent : else '''
    p[0]= p[1]

def p_tagcontent_2(p):
    '''tagcontent : hint '''
    p[0]= p[1]

def p_tagcontent_3(p):
    '''tagcontent : tag '''
    p[0]= p[1]

def p_error(p):
    pass
#    raise "Syntax error at '%s','%s'" % (str(p),str(p.value))
#    raise "Syntax error at '%s'" % str(p)
    
#    print "Syntax error at '%s'" % p.value
#    raise "Syntax error at '%s'" % p.value

import yacc
yacc.yacc()

parser = yacc.parse

if __name__ == "__main__":

   print "-1------------------------------"
   source = """junk[[FOO]junk[this=true]junk[more=stuff]junk[much=more]]junk""" 
   print yacc.parse(source)

   print "-2------------------------------"
   source = """junk[[FOO][this=true]ju
[[FOO][this=true]junk]
[[FOO][this=true]junk]
[[FOO][this=true]junk]
if this&bra;that&ket; ==1:
   print hello
<a href="hello, world">
nk]"""
   print yacc.parse(source)

   print "-3------------------------------"
   source = """junk[[FOO][this=true]ju


nk]"""
   print yacc.parse(source)

   print "-4------------------------------"
   source = """junk[[FOO][this=true]junk]"""
   print yacc.parse(source)

   print "-5------------------------------"
   source = """junk[[FOO][this=true]]"""
   print yacc.parse(source)

   print "-6------------------------------"
   source = """junk[[FOO] ju
nk ]"""
   print yacc.parse(source)

   print "-7------------------------------"
   source = """junk[[FOO] junk ]"""
   print yacc.parse(source)   

   print "-8------------------------------"
   source = """junk[junk]"""
   print yacc.parse(source)

   print "-9------------------------------"
   source = """[ junk ]"""
   print yacc.parse(source)

   print "-10------------------------------"
   source = """
junk
"""
   print yacc.parse(source)

   print "-11------------------------------"
   source = """[]"""
   print yacc.parse(source)



