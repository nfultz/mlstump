# -*- coding: utf-8 -*-

__all__ = ["provides", "needs", "graft"]

def provides(*provides):
    def impl(f):
        f.provides = provides
        return f
    return impl

def get_needs(needs, f, self):
    providers = dict()
    for i in dir(self):
        ii = getattr(self, i)
        for k in getattr(ii, "provides", []):
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
        wrapped_f.needs = needs
        if hasattr(f, "provides"):
            wrapped_f.provides = provides
        return wrapped_f
    return wrap


def graft(stump):
    def call2(f, g):
        def impl(self, *args, **kwargs):
            f(self, *args, **kwargs)
            g(self, *args, **kwargs)
            return self
        if hasattr(f, "provides") or hasattr(g, "provides"):
            impl.provides = getattr(f, "provides", tuple()) + getattr(g, "provides", tuple())
        #if hasattr(f, "needs") or hasattr(g, "needs"):
        #    impl.needs = getattr(f, "needs", tuple()) + getattr(g, "needs", tuple())
        return impl

    def wrap(scion):
        # If in both, call stump then scion then return self
        for i in dir(scion):
            if not i.startswith("__") and hasattr(stump, i):
                setattr(scion, i, call2(getattr(stump, i), getattr(scion, i)))

        # If a provider is only in stump, plug in to scion
        for i in set(dir(stump)) - set(dir(scion)):
            if hasattr(getattr(stump, i), "provides"):
                setattr(scion, i, getattr(stump, i))

        return scion
    return wrap

