# -*- coding: utf-8 -*-
'''
CSS Selectors.
'''

import css
import serialize

class Simple(css.SyntaxObject):
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

        if self.ids:
            r.append( 'ids=' + repr(self.ids) )
        if self.classes:
            r.append( 'classes=' + repr(self.classes) )
        if self.attribs:
            r.append( 'attribs=' + repr(self.attribs) )
        if self.pseudo:
            r.append( 'pseudo=' + repr(self.pseudo) )
        return 'Simple(%r, %s)' % (self.element_name, ', '.join(r),)

    def datum(self, serializer):
        return serialize.serialize_SimpleSelector(self, serializer)

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

class Combined(css.SyntaxObject):
    '''
    A combined selector, e.g. a descendant, child, or adjacent sibling selector.
    '''
    def __init__(self, lhs, rhs, combinator=' '):
        self.lhs = lhs
        self.rhs = rhs
        self.combinator = Combinators[combinator]

    def __repr__(self):
        r = 'Combined(%r, %r' % (self.lhs, self.rhs)
        if not self.combinator is Combinators['descendant']:
            if self.combinator is Combinators['child']:
                r += ', combinator=%r' % (">",)
            elif self.combinator is Combinators['adjacent']:
                r += ', combinator=%r' % ("+",)
        r += ')'
        return r

    def datum(self, serializer):
        return serialize.serialize_CombinedSelector(self, serializer)

def descendant(lhs, rhs):
    return Combined(lhs, rhs, ' ')

def child(lhs, rhs):
    return Combined(lhs, rhs, '>')

def adjacent(lhs, rhs):
    return Combined(lhs, rhs, '+')

class Group(css.SyntaxObject):
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
