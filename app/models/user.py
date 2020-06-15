#!/usr/bin/env python
import logging

from enum import Enum


class Role(Enum):
    MANAGER = 'Manager'
    DEV = 'Developer'
    OPS = 'Operations'
    GUEST = 'Guest'


class User(object):
    def __init__(self, entries={}):
        self.id = None
        self.name = None
        self.email = None
        self.role = None
        self.picture = None

        if entries is not None:
            for key in entries:
                if hasattr(self, key):
                    if key == 'role':
                        self.role = Role(entries[key])
                        continue
                    setattr(self, key, entries[key])

    def __repr__(self) -> str:
        return f"User(email: {self.email}, role: {self.role})"

    def to_dict(self, without_None=False, without_Id=False) -> {}:
        if without_None:
            res = vars(self)
            for x in list(res.keys()):
                if res[x] is None:
                    res.pop(x)
        else:
            res = vars(self)

        if without_Id:
            res.pop('id')
        if 'role' in res:
            res['role'] = res['role'].value
        return res

