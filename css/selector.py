# -*- coding: utf-8 -*-
'''
CSS Selectors.
'''

from css import SyntaxObject
import serialize

class Simple(SyntaxObject):
    '''
    An simple selector pattern.
    '''
    def __init__(self, element_name='*', ids=None, classes=None, attribs=None, pseudo=None):
        self.element_name = element_name
        self.ids = ids or list()
        self.classes = classes or list()
        self.attribs = attribs or list()
        self.pseudo = pseudo or list()

    def __repr__(self):
        r = list()

        if not (self.ids or self.classes or self.attribs or self.pseudo):
            r.append( repr(self.element_name) )
        if self.ids:
            r.append( 'ids=' + repr(self.ids) )
        if self.classes:
            r.append( 'classes=' + repr(self.classes) )
        if self.attribs:
            r.append( 'attribs=' + repr(self.attribs) )
        if self.pseudo:
            r.append( 'pseudo=' + repr(self.pseudo) )
        return 'Simple(%s)' % (', '.join(r),)

    def datum(self, serializer):
        return serialize.serialize_SimpleSelector(self, serializer)

class Combined(SyntaxObject):
    '''
    A combined selector, e.g. a descendant, child, or adjacent sibling selector.
    '''
    Combinators = {
        'descendant' : object(),
        'child' : object(),
        'adjacent' : object()
        }
    Combinators.update({
        ' ' : Combinators['descendant'],
        '>' : Combinators['child'],
        '+' : Combinators['adjacent']
        })

    def __init__(self, selectorA, selectorB, combinator=' '):
        self.selectorA = selectorA
        self.selectorB = selectorB
        self.combinator = self.Combinators[combinator]

    def __repr__(self):
        Combinators = self.Combinators
        r = 'Combined(%r, %r' % (self.selectorA, self.selectorB)
        if not self.combinator is Combinators['descendant']:
            if self.combinator is Combinators['child']:
                r += ', combinator=%r' % (">",)
            elif self.combinator is Combinators['adjacent']:
                r += ', combinator=%r' % ("+",)
        r += ')'
        return r

def descendant(selectorA, selectorB):
    return Combined(selectorA, selectorB, 'descendant')

def child(selectorA, selectorB):
    return Combined(selectorA, selectorB, 'child')

def adjacent(selectorA, selectorB):
    return Combined(selectorA, selectorB, 'adjacent')

class Group(SyntaxObject):
    '''
    A group of several SimpleSelector instances that can share the same ruleset.
    '''
    def __init__(self, *selectors):
        self.selectors = list(selectors)

    def __repr__(self):
        return 'Group(' + ','.join([repr(x) for x in self.selectors]) + ')'

    def __iter__(self):
        '''Iterates the list of selectors.'''
        return iter(self.selectors)

    def __len__(self):
        '''Returns the number of selectors.'''
        return len(self.selectors)

    def __getitem__(self, index):
        '''Returns the selector at the given index.'''
        return self.selectors[index]

    def __contains__(self, selector):
        '''Indicates whether the given selector is present.'''

    def append(self, selector):
        '''
        Appends a selector to the end of the group.

        Modifies the group of selectors *in place.*
        '''
        self.selectors.append(selector)

    def datum(self, serializer):
        return serialize.serialize_SelectorGroup(self, serializer)
