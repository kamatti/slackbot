# -*- coding: utf-8 -*-
from slacker import Slacker
from datetime import datetime as dt
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
            result.append(dict(channel_id=data["id"], channel_name=data["name"]))

        return result

    def post_message_to_channel(self, channel, message):
        """
        Slackチームの任意のチャンネルにメッセージを投稿する。
        """

        channel_name = "#" + channel
        self.__slacker.chat.post_message(channel_name, message, as_user=True)

    def post_attachment_to_channel(self, channel, attachment):
        """
        Slackチームの任意のチャンネルにアタッチメントを投稿する．
        """

        channel_name = '#' + channel
        self.__slacker.chat.post_message(channel_name, attachments=[attachment], text='', as_user=True)

if __name__ == "__main__":

    slack = Slack("API TOKEN")
    #print(slack.get_channel_list())

    filename = dt.now().strftime('%Y%m%d') + '_change_info.csv'
    get_info(filename)

    attachments = make_attachment(filename)

    for mes in attachments:
        slack.post_attachment_to_channel('bot_test', mes)
