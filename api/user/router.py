# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/8/7 2:02
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
from typing import Union, List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Header, Body
from .model import UserBase, UserInDB, UserCreate, UserReturn, UserLogin, TokenModel
from .crud import db_create, db_get_token, db_test_read, db_test_write, db_test_delete

user_router = APIRouter()


@user_router.post("/create", tags=['guest'], summary='用户注册')
def user_create(user: UserCreate):
    res = db_create(**user.dict())
    if res.data:
        return UserReturn(**res.data).dict()
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=res.msg)


@user_router.post("/token", tags=['user'], summary='获取token（本api不应直接暴露在客户端）')
def user_token(user: UserLogin):
    res = db_get_token(user.username, user.password)
    if res.data:
        token_model = TokenModel(access_token=res.data['access_token'], token_type=res.data["token_type"])
        return token_model.dict()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)


@user_router.post("/login", tags=['user'], summary='用户登录（会自动调用获取token的api）')
def user_login(user: UserLogin):
    res_token = db_get_token(user.username, user.password)
    if not res_token.data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res_token.msg)
    res_user = db_test_read(res_token.data['access_token'])
    print(res_user.dict())
    return {
        "token": res_token.data,
        "user": UserReturn(**res_user.data).dict()
    }

@user_router.get("/home", tags=['user'], summary='用户查看', description='''需要`user:read`权限''')
def user_home(authorization_: str = Header(...)):
    res = db_test_read(authorization_)
    if res.data:
        return UserReturn(**res.data).dict()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)


@user_router.post("/update", tags=['user'], summary='用户修改', description="""需要`user:write`权限，注册时默认没有，
因此该接口会返回权限不够的提示""")
def user_update(authorization_: str = Header(...), data: dict = Body(..., example={"gender": 1})):
    res = db_test_write(authorization_, data)
    if res.data:
        return UserReturn(**res.data).dict()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)


@user_router.delete("/delete", tags=['superuser'], summary='用户注销', description="""需要`user:delete`权限，尽管注册时已经添加，
但是数据库已经特意限制了用户删除数据的权限，因此本接口也无法正常使用""")
def user_delete(authorization_: str = Header(...)):
    res = db_test_delete(authorization_)
    if res.data:
        return res.data
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
