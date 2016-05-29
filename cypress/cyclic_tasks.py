#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import tempfile

import tweepy


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
    state.scheduler.enter(__task_delay, 5, task_update_authorized_list, [])
    pass


def task_debug_sched():
    return None  # inactivate debug task
    # logging.debug('triggered debug task')
    tf_handler, tempfilename = tempfile.mkstemp(suffix='.jpg', prefix='cypress-')
    webcam.take_image(tempfilename)
    # tf_handler.close()

    csched.enter(5, 7, task_debug_sched, [])
    pass
