# -*- coding: utf-8 -*-

from fire import Fire

from functools import partial

"""Main module."""


def provides(*args):
    def impl(f):
        f.provides = args
        return f
    return impl

def get_needs(needs, f, self, *args, **kwargs):
    for need in needs:
        if not hasattr(self, need):
            print("needs", need)
    f(self, *args)
    return self


def needs(*args):
    def wrap(f):
        return partial(get_needs, args, f)
    return wrap


class A:
    @provides("d")
    def a(self):
        self.d = True
        return self

    @needs("d")
    def b(self):
        print(self.d)



