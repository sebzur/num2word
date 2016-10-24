#! -*- coding: utf-8 -*-

from django import template
from num2word.num2word_PL import Num2Word_PL

register = template.Library()

@register.filter
def n2w(value):
    return Num2Word_PL().to_cardinal(value)


@register.filter
def pl_a2w(value):
    cc = map(Num2Word_PL().to_cardinal, map(int, ("%.2f" % value).split('.')))
    if len(cc) == 2:
        zl, gr = cc
    else:
        zl = cc[0]
        gr = Num2Word_PL().to_cardinal(0)
    return u"%s złotych %s groszy"%(zl, gr)
