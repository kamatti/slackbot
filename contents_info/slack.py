# -*- coding: utf-8 -*-
from slacker import Slacker

import sys   # 引数取得
import json  # 設定ファイルのパース

class Slack(object):

    __slacker = None

    def __init__(self, token):

        self.__slacker = Slacker(token)

    def get_channel_list(self):
        """
        Slackチーム内のチャンネルID、チャンネル名一覧を取得する。
        """

        # bodyで取得することで、[{チャンネル1},{チャンネル2},...,]の形式で取得できる。
        raw_data = self.__slacker.channels.list().body

        result = []
        for data in raw_data["channels"]:
            result.append(
                dict(channel_id=data["id"], channel_name=data["name"]))

        return result

    def post_message_to_channel(self, channel, message, *, ts=None, name=None, icon=None):
        """
        Slackチームの任意のチャンネルにメッセージを投稿する。
        """

        channel_name = "#" + channel
        #thread化するかどうか
        if ts:
            info = self__slacker.chat.post_message(channel_name, message, as_user=True, thread_ts=ts)
        else:
            # slack.Response classはメンバbodyにjson形式でデータ持ってる
            info = self.__slacker.chat.post_message(channel_name, message, username=name, icon_emoji=icon)

        return info

    def post_attachment_to_channel(self, channel, attachment, *, ts=0, name=None, icon=None):
        """
        Slackチームの任意のチャンネルにアタッチメントを投稿する．
        """

        channel_name = '#' + channel

        # thread化するかどうか
        if ts:
            self.__slacker.chat.post_message(channel_name, attachments=[attachment],
                                             text='', thread_ts=ts)
        else:
            self.__slacker.chat.post_message(channel_name, attachments=[attachment],
                                             text='', username=name, icon_emoji=icon)

def read_json_file(path):
    with open(path, 'rt') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
  # 設定ファイルの読み込み
  settings = read_json_file(sys.argv[1])
  team = settings['team'][sys.argv[2]]

  slack = Slack(team['access_token'])

  # 投稿
  # slack.post_message_to_channel(team['channel'], dt.now().strftime('取得日 : %Y年%m月%d日'), name='reminder', icon=':ghost:')
  for pat in team['pattern']:
      attachments = make_attachment(prefix + filename, pat)
      for mes in attachments:
          slack.post_attachment_to_channel(team['channel'], mes, name='reminder', icon=':ghost:')

