# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/8/7 2:09
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
import time
from settings import TOKEN_EXPIRE_SECONDS
from database.client import db
from database.response import CRUD
from utils.pwd import hash_pwd, verify_pwd
from utils.jwt import jwt_encode_token, jwt_decode_token


coll = db['user']


"""
token part
"""
def verify_token(token: str, scopes: list = None) -> CRUD:
    """
    exp等jwt默认进行校验

    本函数主要结合数据库验证sub（即用户名）和scopes

    :param token:
    :param scopes: 列表，包含所需要验证的scopes
    :return:
    """
    try:
        token_dict = jwt_decode_token(token)
    except Exception as e:
        return CRUD(msg=e.args)

    if not coll.find_one({"username": token_dict.get("sub")}):
        return CRUD(msg="token not valid")

    print({"scopes_demand": scopes, "scopes_owned": token_dict["scopes"]})
    for scope in scopes or []:
        if scope not in token_dict["scopes"]:
            return CRUD(msg="not enough privilege")

    return CRUD(data=token_dict)


def verify_token_wrapper(scopes: list = None):
    def real_function(func):
        def wrapper(token, *args, **kwargs):
            result = verify_token(token, scopes or [])
            if not result.data:
                return result
            return func(token, *args, **kwargs)
        return wrapper
    return real_function

def get_username_from_token(token):
    return jwt_decode_token(token)["sub"]


"""
crud part of common
"""
def db_create(**kwargs):
    """
    - 对password进行了哈希存储
    - 为scopes增加了默认赋值（权限）
    - 为_id做了逻辑判断（mongodb）

    :param kwargs:
    :return:
    """
    if not "username" in kwargs or not "password" in kwargs:
        return CRUD(msg="missing fields")
    if coll.find_one({"username": kwargs["username"]}):
        return CRUD(msg="user existed")
    hashed_password = hash_pwd(kwargs["password"])
    kwargs.pop("password")
    kwargs["hashed_password"] = hashed_password
    kwargs["scopes"] = kwargs.get("scopes") or []
    kwargs["_id"] = kwargs.get("_id") or kwargs["username"]
    coll.insert_one(kwargs)
    return CRUD(data=coll.find_one({"_id": kwargs["_id"]}))

"""
crud part of token
"""
def db_get_token(username, password):
    """
    有了获取token这个环节，其实登录就等于获取token+读取user信息两步

    所以在数据库环节没必要多写一个登录函数，在前端写即可

    此外，基于token的认证，在数据库环节也无需多写一个基于id查找用户的函数

    :param username:
    :param password:
    :return:
    """
    user_item = coll.find_one({"username": username})
    if user_item and verify_pwd(password, user_item['hashed_password']):
        token = jwt_encode_token({
            "sub": username,
            "scopes": user_item.get("scopes", []),
            "exp": time.time() + TOKEN_EXPIRE_SECONDS
        })
        return CRUD(data={"access_token": token, "token_type": "Bearer"})
    return CRUD(msg="incorrect username or password")

@verify_token_wrapper(scopes=['user:read'])
def db_test_read(token):
    username = get_username_from_token(token)
    print({"username": username})
    user_item = coll.find_one({"username": username})
    return CRUD(data=user_item)

@verify_token_wrapper(scopes=['user:write'])
def db_test_write(token, data: dict):
    try:
        user_item = coll.find_one_and_update(
            {"username": get_username_from_token(token)}, {"$set": data}, upsert=False, return_document=True)
    except Exception as e:
        return CRUD(msg=e.args)
    else:
        return CRUD(data=user_item)

@verify_token_wrapper(scopes=['user:delete'])
def db_test_delete(token):
    username = get_username_from_token(token)
    try:
        coll.delete_one({"username": username})
    except Exception as e:
        return CRUD(msg=str(e.args))
    else:
        return CRUD(data={"status": f"successfully deleted user: {username}"})