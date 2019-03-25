#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mlstump` package."""

import pytest


from mlstump import provides, needs, graft


class A:
    @provides("x")
    def a(self):
        self.x = 1
        return self

    @provides("y")
    @needs("x")
    def b(self):
        self.y = self.x



@graft(A)
class B:
    @provides("z")
    def b(self):
        self.z = self.x
        self.x = self.x + 1
        pass

    @needs("z")
    def c(self):
        del self.z

    @needs("y")
    def d(self):
        del self.y

def test_A_b():
    a = A()
    assert not hasattr(a, "x")
    assert not hasattr(a, "y")
    assert a == a.b()
    assert a.x == 1
    assert a.y == 1

def test_B_b():
    b = B()
    assert not hasattr(b, "x")
    assert not hasattr(b, "y")
    assert not hasattr(b, "z")
    assert b == b.b()
    assert b.x == 2
    assert b.y == 1
    assert b.z == 1


def test_B_c_d():
    b = B()
    assert not hasattr(b, "x")
    assert not hasattr(b, "y")
    assert not hasattr(b, "z")
    assert b == b.c().d()
    assert b.x == 2, "Should be created at 1, incremented to two, then cached and reused"
    assert not hasattr(b, "y")
    assert not hasattr(b, "z")
