#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

from actions import update_timeline_with_image, delete_status


def dm_handler(api, status, authorized_user_ids=list()):
    sender_id = status.direct_message['sender_id']
    dm_text = status.direct_message['text']
    dm_sent_by_me = sender_id == api.me().id
    if not dm_sent_by_me:  # we don't want to parse DMs sent by us
        if sender_id in authorized_user_ids:
            logging.debug('dm from authorized user {!s}'.format(sender_id))
            _parse_dm(api, status.direct_message)
        else:
            logging.debug('ignored dm from not authorized user {!s} with text {!s}'.format(sender_id, dm_text))
    pass


def _parse_dm(api, dm):
    dm_text = dm['text']
    dm_sender_id = dm['sender_id']
    if dm_text.startswith('take picture'):
        logging.debug('found command take picture')
        api.send_direct_message(user_id=dm_sender_id, text='will do!')
        update_timeline_with_image(api=api)
    elif dm_text.startswith('delete'):
        delete_index = int(dm_text.strip('delete'))
        if not delete_index:
            delete_index = 0
        logging.debug('found delete command with index {!s}'.format(delete_index))
        delete_status(api, delete_index, dm_sender_id)
    elif dm_text.startswith('say '):
        max_chars_in_status = 140
        status_text = dm_text[len('say '):max_chars_in_status]
        api.update_status(status=status_text)
    else:
        logging.debug('did not find a valid command')
        api.send_direct_message(user_id=dm_sender_id, text='did not recognize your message: {!s}'.format(dm_text))
    pass
