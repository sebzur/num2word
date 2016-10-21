#! -*- coding: utf-8 -*-

from django import template
from apap3.contracts.models.base import GridNodeContract
from num2word.num2word_PL import Num2Word_PL

register = template.Library()

@register.tag(name="n2w")
def do_n2w(parser, token):
    try:
        tag_name, identifier, option = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires two arguments" % token.contents.split()[0]
        )
    if not (option[0] == option[-1] and option[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's second argument should be in quotes" % tag_name
        )

    return N2W(identifier, option[1:-1])


class N2W(template.Node):
        def __init__(self, identifier, option):
            self.identifier = template.Variable(identifier)
            self.option = option

        def amount_to_string(self, amount): #the method is taken from contracts.py 
            # extracting ZL and GR in short:                                                                                                                                        
            cc = map(Num2Word_PL().to_cardinal, map(int, ("%.2f" % amount).split('.')))
            if len(cc) == 2:
                zl, gr = cc
            else:
                zl = cc[0]
                gr = Num2Word_PL().to_cardinal(0)
            return u"%s złotych %s groszy"%(zl, gr)

        def render(self, context):
            obj = GridNodeContract.objects.get(id = self.identifier.resolve(context))
            
            if self.option == "number":
                return obj.get_amount(obj.publication_datetime)
                
            if self.option == "word":
                return self.amount_to_string(obj.get_amount(obj.publication_datetime))
