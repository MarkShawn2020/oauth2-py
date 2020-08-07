# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/8/6 21:10
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
from settings import JWT_ALGO, JWT_SK

from jose import jwt, JWTError
from typing import Union


def jwt_encode_token(token_dict: dict) -> str:
    return jwt.encode(token_dict, JWT_SK, algorithm=JWT_ALGO)


def jwt_decode_token(token_value: str) -> Union[dict, None]:
    """
    自行处理返回值, JWT error

    :param token_value:
    :return:
    """
    return jwt.decode(token_value, JWT_SK, algorithms=[JWT_ALGO])

