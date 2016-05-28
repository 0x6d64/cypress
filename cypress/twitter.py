#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import tweepy
import credentials


class MyStreamListener(tweepy.StreamListener):
    def on_direct_message(self, status):
        if self.dm_handler:
            self.dm_handler(status)
        else:
            raise StandardError('no handler for direct messages set')

    def on_error(self, status_code):
        if status_code == 420:
            print('got an 420 return code, stopping the stream...')
            return False


def authorize(get_auth=False):
    auth = tweepy.OAuthHandler(credentials.consumer_token, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_key)
    if not get_auth:
        return tweepy.API(auth, retry_count=10, retry_delay=5)
    else:
        return auth


if __name__ == '__main__':
    pass
