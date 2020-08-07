# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/8/6 21:21
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_pwd(plain_password, hashed_password):
    return _pwd_context.verify(plain_password, hashed_password)


def hash_pwd(password):
    return _pwd_context.hash(password)
