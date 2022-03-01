# -*- coding: utf-8 -*- 
"""Created by ssfanli on 2022/01/23 
"""
import contextlib
import functools
import os
import sys
import time
import typing

import cv2
import numpy as np
from loguru import logger


@contextlib.contextmanager
def video_capture(video_path: str):
    video_cap = cv2.VideoCapture(video_path)
    try:
        yield video_cap
    finally:
        video_cap.release()


def get_current_frame_id(video_cap: cv2.VideoCapture) -> int:
    # IMPORTANT:
    # this id is the frame which has already been grabbed
    # we jump to 5, which means the next frame will be 5
    # so the current frame id is: 5 - 1 = 4
    return int(video_cap.get(cv2.CAP_PROP_POS_FRAMES))


def get_current_frame_time(video_cap: cv2.VideoCapture) -> float:
    # same as get_current_frame_id, take good care of them
    return video_cap.get(cv2.CAP_PROP_POS_MSEC) / 1000


def turn_grey(old: np.ndarray) -> np.ndarray:
    try:
        return cv2.cvtColor(old, cv2.COLOR_RGB2GRAY)
    except cv2.error:
        return old


def compress_frame(
    old: np.ndarray,
    compress_rate: float = None,
    target_size: typing.Tuple[int, int] = None,
    not_grey: bool = None,
    interpolation: int = None,
    *_,
    **__,
) -> np.ndarray:
    """
    Compress frame

    :param old:
        origin frame

    :param compress_rate:
        before_pic * compress_rate = after_pic. default to 1 (no compression)
        eg: 0.2 means 1/5 size of before_pic

    :param target_size:
        tuple. (100, 200) means compressing before_pic to 100x200

    :param not_grey:
        convert into grey if True

    :param interpolation:
    :return:
    """

    target = turn_grey(old) if not not_grey else old

    if not interpolation:
        interpolation = cv2.INTER_AREA
    # target size first
    if target_size:
        return cv2.resize(target, target_size, interpolation=interpolation)
    # else, use compress rate
    # default rate is 1 (no compression)
    if not compress_rate:
        return target
    return cv2.resize(target, (0, 0), fx=compress_rate, fy=compress_rate, interpolation=interpolation)


class VideoFrame(object):
    def __init__(self, frame_id: int, timestamp: float, data: np.ndarray):
        self.frame_id: int = frame_id
        self.timestamp: float = timestamp
        self.data: np.ndarray = data

    def __str__(self):
        return f"<VideoFrame id={self.frame_id} timestamp={self.timestamp}>"

    @classmethod
    def init(cls, cap: cv2.VideoCapture, frame: np.ndarray) -> "VideoFrame":
        frame_id = get_current_frame_id(cap)
        timestamp = get_current_frame_time(cap)
        grey = turn_grey(frame)
        logger.debug(f"new a frame: {frame_id}({timestamp})")
        return VideoFrame(frame_id, timestamp, grey)


class Frame(object):
    def __init__(self, path: typing.Union[str, os.PathLike]):
        assert os.path.isfile(path), f"video {path} not existed"
        self.path: str = str(path)
        self.video_frame_dir = os.path.splitext(self.path)[0]
        if not os.path.isdir(self.video_frame_dir):
            os.mkdir(self.video_frame_dir)

    def __str__(self):
        return f"<VideoObject path={self.path}>"

    __repr__ = __str__

    def load_frames(self):
        logger.info(f"video: {self.path} load frames to: {self.video_frame_dir} ...")

        with video_capture(self.path) as cap:
            # the first
            success, frame = cap.read()
            while success:
                frame_object = VideoFrame.init(cap, frame)
                compressed = compress_frame(frame_object.data, compress_rate=0.2)

                image_name = f"{frame_object.frame_id}_{frame_object.timestamp}.png"
                each_frame_path = os.path.join(self.video_frame_dir, image_name)

                cv2.imwrite(each_frame_path, compressed)
                # read the next one
                success, frame = cap.read()


def video2frame(video_path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            time.sleep(.5)
            return Frame(video_path).load_frames()
        return wrapper
    return decorator


if __name__ == '__main__':
    args = sys.argv
    args = args[1:]
    assert len(args) == 1, 'please input video dir path, such as: python3 capture/frame.py video_dir_path'
    video_dir_path = args[0]
    for each_video in os.listdir(video_dir_path):
        if os.path.splitext(each_video)[-1].lower() in ('.mp4', '.mov'):
            Frame(os.path.join(video_dir_path, each_video)).load_frames()
