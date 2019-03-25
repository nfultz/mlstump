# -*- coding: utf-8 -*-

from fire import Fire

from functools import partial

"""Main module."""


def provides(*args):
    def impl(f):
        f.provides = args
        return f
    return impl

def get_needs(needs, f, self):
    providers = dict()
    for i in dir(self):
        ii = getattr(self, i)
        if hasattr(ii, "provides"):
            for k in ii.provides:
                providers[k] = ii

    for need in needs:
        if not hasattr(self, need):
            print("needs", need)
            if need in providers:
                providers[need]()
            else:
                raise Exception("needs %s (not provided)" % need)


def needs(*needs):
    def wrap(f):
        def wrapped_f(self, *args, **kwargs):
            get_needs(needs, f, self)
            f(self, *args, **kwargs)
            return self
        return wrapped_f
    return wrap


def graft(stump):
    def call2(f, g):
        def impl(self, *args, **kwargs):
            f(self, *args, **kwargs)
            g(self, *args, **kwargs)
            return self
        return impl

    def wrap(scion):
        # If in both, call stump then scion then return self
        for i in dir(scion):
            if not i.startswith("__") and hasattr(stump, i):
                setattr(scion, i, call2(getattr(stump, i), getattr(scion, i)))

        # If only in stump, plug in to scion
        for i in set(dir(stump)) - set(dir(scion)):
            setattr(scion, i, getattr(stump, i))

        return scion
    return wrap

class A:
    @provides("d")
    def a(self):
        self.d = True
        return self

    @needs("d")
    def b(self):
        print(self.d)



@graft(A)
class B:
    def b(self):
        pass

    def c(self):
        pass

