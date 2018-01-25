#!/usr/bin/env python
# encoding: utf-8

from dingding_sdk import config
from dingding_sdk import auth
from dingding_sdk import user
from dingding_sdk import department
from dingding_sdk import utils
from dingding_sdk import message
from dingding_sdk import media

def print_dict(result):
    for k, v in result.iteritems():
        print '%s : %s' % (k, v)

is_success, result = auth.get_access_token(config.CorpID, config.Secret)
access_token = result.get('access_token')

# department
# is_success, result = department.get_department_list(access_token)
# print_dict(result)


touser = '13570206541269367'
toparty = None

#send text message ok!
send_type = 'text'
content = {'content': 'ding-message-test777'}
is_success, result = message.send(access_token, touser, toparty, send_type, content)
print is_success, result



#upload media ok!
media_type = 'image'
media_file = open('./picture_test.jpg', 'rb')
is_success, result = media.upload_media(access_token, media_type, media_file)
print is_success, result

picture_media_id = result.get('media_id')


#send image message ok!
send_type = 'image'
content = {'media_id': picture_media_id}
is_success, result = message.send(access_token, touser, toparty, send_type, content)
print is_success, result
