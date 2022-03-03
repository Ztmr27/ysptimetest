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
from pathlib import Path


def cut(original_video: typing.Union[str, os.PathLike],
        new_video: typing.Union[str, os.PathLike],
        start: str = '00:00:01',
        delete: bool = True):
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


def splice(*x):
    return os.path.join(*x)


def path_obj(p):
    return Path(p)


def abspath(p):
    return path_obj(splice(os.path.dirname(__file__), p)).resolve()


def file_exist(_fp, raise_error=True):
    """
    check the _fp exists
    :param _fp: file path
    :param raise_error: whether raise error
    :return:
    """
    if raise_error:
        if not os.path.exists(_fp):
            raise FileExistsError('file: %s dose not exists !' % _fp)
    else:
        return os.path.exists(_fp)


def md(_dir):
    if not file_exist(_dir, raise_error=False):
        os.makedirs(_dir)
    return _dir


if __name__ == '__main__':
    print(splice('../output', 'ysp'))