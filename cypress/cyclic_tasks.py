#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import os
import time

import tweepy

import config
import fswebcamobject


def task_update_authorized_list(state=None):
    """
    retrieves the list auf authourized users from apiter
    """
    __task_delay = 5 * 60  # checking once ever 5 minutes is enough
    api = state.api
    temp_list = list()
    for user in tweepy.Cursor(api.list_members, owner_id=api.me().id, slug='authorized-users').items():
        temp_list.append(user.id)
    state.set_authorized_user_ids(temp_list)
    logging.debug('got {} authorized users'.format(len(state.authorized_user_ids)))
    state.scheduler.enter(__task_delay, 5, task_update_authorized_list, [state])
    pass


def task_take_picture_cyclic(state=None):
    if state.take_picture_cyclic_active:
        if not os.path.isdir(config.cyclicImageFolder):
            os.mkdir(config.cyclicImageFolder)
            logging.info('created folder {!s}'.format(config.cyclicImageFolder))
        logging.debug('take picture triggered by cyclic task')
        cam = fswebcamobject.FsWebcamObject(input_device=config.captureDevice, resolution_x=640, resolution_y=480)
        cam.frames_to_take = 2
        cam.frames_to_skip = 5
        fn = time.strftime('%Y%m%d-%H%M%S') + '.jpg'
        fullpath = os.path.abspath(os.path.join(config.cyclicImageFolder, fn))
        cam.take_image(filename=fullpath)
    else:
        pass  # do nothing except scheduling of new task
    state.scheduler.enter(state.take_picture_cyclic_delay, 6, task_take_picture_cyclic, [state])
    pass
