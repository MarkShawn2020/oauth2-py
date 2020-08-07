# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/8/7 2:19
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

import pymongo
from settings import MONGO_URI, MONGO_DB, MONGO_USERNAME, MONGO_PASSWORD
uri = pymongo.MongoClient(MONGO_URI)
uri[MONGO_DB].authenticate(name=MONGO_USERNAME, password=MONGO_PASSWORD)
db = uri[MONGO_DB]