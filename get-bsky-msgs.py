#!/usr/bin/env python
# coding: UTF-8
#
# get self Bluesky posts
#
# necessary environment variables:
#   BSKY_ID: Bluesky ID like digitune.bsky.social
#   BSKY_APPPASSWORD: App Password generated by you in Bluesky
#
from atproto import Client
import re
from urllib.parse import urlparse
from os import environ
# for debug
import pprint

def get_bsky_msgs():
    # login
    client = Client(base_url='https://bsky.social')
    client.login(environ['BSKY_ID'], environ['BSKY_APPPASSWORD'])

    # get recent messages
    data = client.get_author_feed(
        actor=client.me.did,
        filter='posts_no_replies',
        limit=30,
    )
    for feed in data.feed:
        # filter replies
        if feed.reply:
            if feed.reply.parent.author.did != client.me.did:
                continue # reply to someone
        pprint.pprint(feed) # debug
        # get text
        text = feed.post.record.text
        print("orig=" + text) # debug
        # extract links
        uris = []
        if feed.post.record.facets:
            for facet in feed.post.record.facets:
                uris.append(facet.features[0].uri)
        for uri in uris:
            uri_o = urlparse(uri)
            (text, num) = re.subn('([^/])' + uri_o.hostname + '.+\\.\\.\\.', '\\1' + uri, text, 1)
            if num == 0:
                text = re.sub('([^/])' + uri_o.hostname, '\\1' + uri, text, 1)
        # get attached images
        images = []
        if feed.post.embed and hasattr(feed.post.embed, 'images'):
            for image in feed.post.embed.images:
                images.append(image.fullsize)
        print('text=' + text) # debug
        for image_url in images:
            print('image_url=' + image_url) # debug
        print('==================================') # debug

if __name__ == '__main__':
    get_bsky_msgs()
