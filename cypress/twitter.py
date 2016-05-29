#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import tweepy

import credentials


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, state=None):
        super(MyStreamListener, self).__init__()
        self.api = state.api
        self.state = state

    def on_direct_message(self, status):
        if not self.api:
            raise StandardError('need api')
        elif not self.dm_handler:
            raise StandardError('no handler for direct messages set')
        else:
            self.dm_handler(self.api, status, authorized_user_ids=self.state.authorized_user_ids)

    def on_error(self, status_code):
        if status_code == 420:
            print('got an 420 return code, stopping the stream...')
            return False


def get_auth():
    auth = tweepy.OAuthHandler(credentials.consumer_token, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_key)
    return auth


if __name__ == '__main__':
    pass
