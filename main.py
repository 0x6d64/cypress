#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import sched
import time

import tweepy

from cypress import twitter, fswebcamobject, config, handle_direct_message, cyclic_tasks


class CypressState(object):
    def __init__(self):
        self.authorized_user_ids = list()
        self.scheduler = None
        self.take_picture_cyclic_active = False
        self.take_picture_cyclic_delay = 15 * 60

    def set_authorized_user_ids(self, authorized_user_ids):
        self.authorized_user_ids = authorized_user_ids

    pass


# TODO add logfile to logging handler

def main():
    logging.basicConfig(level=logging.DEBUG)

    log = logging.getLogger(__name__)
    state = CypressState()
    state.take_picture_cyclic_delay = config.cyclicImageDelaySeconds
    state.take_picture_cyclic_active = config.cyclicImageActive
    # state.authorized_user_ids = list()
    state.authorized_user_ids = [2342]

    state.webcam = fswebcamobject.FsWebcamObject(input_device=config.captureDevice, resolution_x=640, resolution_y=480)
    state.webcam.frames_to_take = 2
    state.webcam.frames_to_skip = 5
    state.api = tweepy.API(twitter.get_auth(), retry_count=10, retry_delay=5)
    state.scheduler = sched.scheduler(time.time, time.sleep)

    # prefill scheduler task list
    state.scheduler.enter(0, 1, cyclic_tasks.task_update_authorized_list, [state])
    state.scheduler.enter(0, 2, cyclic_tasks.task_take_picture_cyclic, [state])

    dm_listener = twitter.MyStreamListener(state=state)
    dm_listener.dm_handler = handle_direct_message.dm_handler
    dm_stream = tweepy.Stream(auth=twitter.get_auth(), listener=dm_listener)
    dm_stream.userstream(async=True)

    state.scheduler.run()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.debug('exited because of keyboard interrupt')
    pass


if __name__ == "__main__":
    main()
    pass
