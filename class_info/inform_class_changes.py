# -*- coding: utf-8 -*-
from slacker import Slacker

from datetime import datetime as dt
import sys   # 引数取得
import json  # 設定ファイルのパース

from make_attachment import make_attachment
from get_info import get_info


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

    def post_message_to_channel(self, channel, message, *, ts=0):
        """
        Slackチームの任意のチャンネルにメッセージを投稿する。
        """

        channel_name = "#" + channel
        #thread化するかどうか
        if ts:
            info = self__slacker.chat.post_message(channel_name, message, as_user=True, thread_ts=ts)
        else:
            # slack.Response classはメンバbodyにjson形式でデータ持ってる
            info = self.__slacker.chat.post_message(channel_name, message, as_user=True)

        return info

    def post_attachment_to_channel(self, channel, attachment, *, ts=0):
        """
        Slackチームの任意のチャンネルにアタッチメントを投稿する．
        """

        channel_name = '#' + channel

        # thread化するかどうか
        if ts:
            self.__slacker.chat.post_message(channel_name, attachments=[attachment],
                                             text='', as_user=True, thread_ts=ts)
        else:
            self.__slacker.chat.post_message(channel_name, attachments=[attachment],
                                             text='', as_user=True)

def read_json_file(path):
    with open(path, 'rt') as f:
        date = json.load(f)
    return date

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print('Usage : python {} "setting file(.json)" "team name"'.format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    # 設定ファイルの読み込み
    settings = read_json_file(sys.argv[1])
    team = settings['team'][sys.argv[2]]

    slack = Slack(team['access_token'])

    # ファイルはchangesディレクトリ配下に日付付きで保存しておく
    # TODO : ファイルの保存方法は検討
    filename = '/home/squid/SlackBot/class_info/changes/' + dt.now().strftime('%Y%m%d') + '_change_info.csv'
    get_info(filename)

    # 投稿
    slack.post_message_to_channel(team['channel'], dt.now().strftime('取得日 : %Y年%m月%d日'))
    for pat in team['pattern']:
        attachments = make_attachment(filename, pat)
        for mes in attachments:
            slack.post_attachment_to_channel(team['channel'], mes)
