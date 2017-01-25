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

if __name__ == "__main__":

    slack = Slack("YOUR ACCESS TOKEN")

    filename = dt.now().strftime('%Y%m%d') + '_change_info.csv'
    # get_info(filename)

    info = slack.post_message_to_channel('bot_test', 'wawawawaawa')
    # print(info.body['ts'])

    # 4年の変更情報
    attachments_for_4th = make_attachment(filename, '\A([4INA]|[４ＩＮＡ全]).?.?[^1-35]([4LN]|[４ＬＮ全])\Z')
    for mes in attachments_for_4th:
        slack.post_attachment_to_channel('bot_test', mes)

    # 5年の変更情報
    attachments_for_5th = make_attachment(filename, '\A([5INA]|[５ＩＮＡ全]).?.?[^1-4]([5LN]|[５ＬＮ全])\Z')
    for mes in attachments_for_5th:
        slack.post_attachment_to_channel('bot_test', mes)
