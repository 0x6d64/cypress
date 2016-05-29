#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import os
import tempfile
import time

import config
import fswebcamobject


def delete_status(api, index, userid_to_reply):
    tl = api.user_timeline(user_id=api.me().id, count=index + 1)
    try:
        api.destroy_status(id=tl[index].id)
        api.send_direct_message(user_id=userid_to_reply, text='deleted status at index {!s}'.format(index))
    except IndexError:
        error_msg = 'ERROR: index error using index {!s}'.format(index)
        api.send_direct_message(user_id=userid_to_reply, text=error_msg)
        logging.debug(error_msg)
        pass
    pass


def update_timeline_with_image(api):
    webcam = fswebcamobject.FsWebcamObject(input_device=config.captureDevice, resolution_x=640, resolution_y=480)
    webcam.frames_to_take = 2
    webcam.frames_to_skip = 5

    with tempfile.NamedTemporaryFile(prefix='cypress-', suffix='.jpg') as tf:
        webcam.take_image(tf.name)
        time.sleep(5)
        api.update_with_media(filename=os.path.abspath(tf.name), status=r'', file=tf)
    pass
