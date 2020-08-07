# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/8/7 2:00
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

from fastapi import FastAPI
from api.root_router import root_rooter


app = FastAPI(title="基于FastAPI的OAuth2实现")
app.include_router(root_rooter, prefix="/api/v1")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)