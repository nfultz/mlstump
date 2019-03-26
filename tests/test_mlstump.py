#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mlstump` package."""

import pytest


from mlstump import provides, needs, graft

exec_order = []

class A:

    @provides("x")
    def a(self):
        exec_order.append("A.a")
        self.x = 1
        return self

    @provides("y")
    @needs("x")
    def b(self):
        exec_order.append("A.b")
        self.y = self.x



@graft(A)
class B:
    @provides("z")
    def b(self):
        exec_order.append("B.b")
        self.z = self.x
        self.x = self.x + 1
        pass

    @needs("z")
    def c(self):
        exec_order.append("B.c")
        del self.z

    @needs("y")
    def d(self):
        exec_order.append("B.d")
        del self.y

def test_A_b():
    exec_order.clear()
    a = A()
    assert not hasattr(a, "x")
    assert not hasattr(a, "y")
    assert a == a.b()
    assert a.x == 1
    assert a.y == 1
    assert exec_order == ["A.a", "A.b"]

def test_B_b():
    exec_order.clear()
    b = B()
    assert not hasattr(b, "x")
    assert not hasattr(b, "y")
    assert not hasattr(b, "z")
    assert b == b.b()
    assert b.x == 2
    assert b.y == 1
    assert b.z == 1
    assert exec_order == ["A.a", "A.b", "B.b"]


def test_B_c_d():
    exec_order.clear()
    b = B()
    assert not hasattr(b, "x")
    assert not hasattr(b, "y")
    assert not hasattr(b, "z")
    assert b == b.c().d()
    assert b.x == 2, "Should be created at 1, incremented to two, then cached and reused"
    assert not hasattr(b, "y")
    assert not hasattr(b, "z")
    assert exec_order == ["A.a", "A.b", "B.b", "B.c","B.d"]
