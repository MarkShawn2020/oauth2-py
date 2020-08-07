# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/8/7 2:00
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

from fastapi import APIRouter
from .user.router import user_router


root_rooter = APIRouter()
root_rooter.include_router(user_router, prefix="/user")