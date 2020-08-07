# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/8/7 2:00
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
from settings import PROJECT_TITLE
from fastapi import FastAPI
from api.root_router import root_rooter

with open('readme.md', 'r', encoding='utf-8') as f:
    openapi_desc = f.read().split('OpenAPI调试')[-1]

app = FastAPI(title=PROJECT_TITLE, description=openapi_desc)
app.include_router(root_rooter, prefix="/api/v1")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)