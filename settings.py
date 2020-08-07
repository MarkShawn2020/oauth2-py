# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/8/7 1:52
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

# user: default
class DefaultUser:
    username = 'Markshawn'
    password = 'secret'
    nickname = 'mark'
    scopes   = ['user:read', 'user:delete']


# openssl rand --hex 32
JWT_SK = 'fa5bf890c1c502fbf7460c9ea27c1cfa13f1776c5c4dd6b19bcd6a103c3c6f85'
JWT_ALGO = 'HS256'


# database: mongodb
MONGO_URI = 'nanchuan.site:2708'
MONGO_DB = 'guest-OAuth2'
MONGO_USERNAME = 'guest-OAuth2'
MONGO_PASSWORD = 'guest-OAuth2'


# token
TOKEN_TYPE = "Bearer"
TOKEN_EXPIRE_SECONDS = 60 * 60 # seconds