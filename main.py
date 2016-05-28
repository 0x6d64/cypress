#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import os
import sched
import tempfile
import time

import tweepy

from cypress import twitter, fswebcamobject, config

authorized_user_ids = list()
csched = sched.scheduler(time.time, time.sleep)
last_dm_id = None
twit = None
webcam = None


def task_get_authorized_list():
    """
    retrieves the list auf authourized users from twitter
    """
    __task_delay = 5 * 60  # checking once ever 5 minutes is enough
    global authorized_user_ids
    temp_list = list()
    for user in tweepy.Cursor(twit.list_members, owner_id=twit.me().id, slug='authorized-users').items():
        temp_list.append(user.id)
    authorized_user_ids = temp_list
    logging.debug('got {} authorized users'.format(len(authorized_user_ids)))
    csched.enter(__task_delay, 5, task_get_authorized_list, [])
    pass


def dm_handler(status):
    print(status.direct_message)
    sender_id = status.direct_message['sender_id']
    dm_text = status.direct_message['text']
    dm_sent_by_me = sender_id is twit.me().id
    if not dm_sent_by_me:  # we don't want to parse DMs sent by us
        if sender_id in authorized_user_ids:
            logging.debug('dm from authorized user {!s}'.format(sender_id))
            parse_dm(status.direct_message)
        else:
            logging.debug('ignored dm from not authorized user {!s}'.format(sender_id))
    pass


def parse_dm(dm):
    dm_text = dm['text']
    dm_sender_id = dm['sender_id']
    if dm_text.startswith('take picture'):
        logging.debug('found command take picture')
        twit.send_direct_message(user_id=dm_sender_id, text='will do!')
        update_timeline_with_image()
    elif dm_text.startswith('delete'):
        delete_index = int(dm_text.strip('delete'))
        if not delete_index:
            delete_index = 0
        logging.debug('found delete command with index {!s}'.format(delete_index))
        delete_status(delete_index, dm_sender_id)
    else:
        logging.debug('did not find a valid command')
        twit.send_direct_message(user_id=dm_sender_id, text='did not recognize your message: {!s}'.format(dm_text))
    pass


def delete_status(index, userid_to_reply):
    tl = twit.user_timeline(user_id=twit.me().id, count=index + 1)
    try:
        twit.destroy_status(id=tl[index].id)
        twit.send_direct_message(user_id=userid_to_reply, text='deleted status at index {!s}'.format(index))
    except IndexError:
        error_msg = 'ERROR: index error using index {!s}'.format(index)
        twit.send_direct_message(user_id=userid_to_reply, text=error_msg)
        logging.debug(error_msg)
        pass
    pass


def update_timeline_with_image():
    with tempfile.NamedTemporaryFile(prefix='cypress-', suffix='.jpg') as tf:
        webcam.take_image(tf.name)
        time.sleep(5)
        twit.update_with_media(filename=os.path.abspath(tf.name), status=r'', file=tf)
    pass


def task_debug_sched():
    return None  # inactivate debug task
    # logging.debug('triggered debug task')
    tf_handler, tempfilename = tempfile.mkstemp(suffix='.jpg', prefix='cypress-')
    webcam.take_image(tempfilename)
    # tf_handler.close()

    csched.enter(5, 7, task_debug_sched, [])
    pass


def main():
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)

    global twit, webcam
    webcam = fswebcamobject.FsWebcamObject(input_device=config.captureDevice, resolution_x=640, resolution_y=480)
    webcam.frames_to_take = 2
    webcam.frames_to_skip = 5

    twit = twitter.authorize()

    # prefill scheduler task list
    csched.enter(0, 1, task_get_authorized_list, [])

    dm_listener = twitter.MyStreamListener()
    dm_listener.dm_handler = dm_handler
    dm_stream = tweepy.Stream(auth=twitter.authorize(get_auth=True), listener=dm_listener)
    dm_stream.userstream(async=True)

    csched.run()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.debug('exited because of keyboard interrupt')
    pass


if __name__ == "__main__":
    main()
    pass
