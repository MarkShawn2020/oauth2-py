# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/8/7 2:08
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
from settings import DefaultUser, TOKEN_TYPE
from pydantic import BaseModel, Field

"""
user
"""

class UserBase(BaseModel):
    username: str = Field(..., example=DefaultUser.username, description="用户名，也是唯一ID的存在")

class UserLogin(UserBase):
    password: str = Field(..., example=DefaultUser.password, description="用户密码，在登录和注册时需要")

class UserReturn(UserBase):
    nickname: str = Field(..., example=DefaultUser.nickname, description="后端返回至前端时，显示用户昵称")

class UserCreate(UserLogin, UserReturn):
    scopes: list = Field(..., example=DefaultUser.scopes, description="注册用户时分配的用户权限")

class UserInDB(UserBase):
    hashed_password: str = Field(..., description="用户密码存入数据库时，需要在后端进行加密")


"""
token
"""
class TokenModel(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(TOKEN_TYPE)