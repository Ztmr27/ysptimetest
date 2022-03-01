#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Ssfanli
@Time  : 2020/07/09 13:59
@Desc  : video cut
"""
import functools
import os
import typing
from loguru import logger


def cut(
        original_video: typing.Union[str, os.PathLike],
        new_video: typing.Union[str, os.PathLike],
        start: str = '00:00:01',
        delete: bool = True
):
    """video cut wrapper

    solve the blue screen at the beginning of ios video
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            cmd = f'ffmpeg -y -ss {start} -i {original_video} -c copy {new_video}'
            del_cmd = f'echo "delete original video ..." ; rm -rf {original_video}'
            if delete:
                cmd = cmd + ' && ' + del_cmd
            logger.debug(f"cut_cmd: {cmd}")
            os.system(cmd)
        return wrapper
    return decorator
