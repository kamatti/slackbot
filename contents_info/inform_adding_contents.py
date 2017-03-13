# -*- coding: utf-8 -*-
from slacker import Slacker

import subprocess as sb
import sys   # 引数取得
import argparse
import json

class Slack(object):

    __slacker = None

    def __init__(self, token):

        self.__slacker = Slacker(token)

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

    def post_message_to_person(self, channel, message, *, ts=None, name=None, icon=None):
        """
        Slackチームの任意のチャンネルにメッセージを投稿する。
        """

        #thread化するかどうか
        if ts:
            info = self__slacker.chat.post_message(channel, message, as_user=True, thread_ts=ts)
        else:
            # slack.Response classはメンバbodyにjson形式でデータ持ってる
            info = self.__slacker.chat.post_message(channel, message, username=name, icon_emoji=icon)


def difference(latest, oldest):
    '''
    ２つのリストからlatestにある行のリストを作る
    '''
    set1 = set(latest)
    set2 = set(oldest)

    return list(set1.difference(set2))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='コンテンツの追加を確認するためのスクリプト')
    parser.add_argument('channel', default='contents', help='投稿するチャンネル')
    parser.add_argument('--access_token', help='投稿するアカウントのアクセストークン')
    parser.add_argument('-p', '--path', action='store', type=str,
                        help='検索するディレクトリパス．絶対パスで指定した方が幸せです．')
    parser.add_argument('-f', '--file', action='store', type=str,
                        help='以前のデータを保存したファイルを指定．絶対パスで指定した方が幸せです．')
    parser.add_argument('-type', action='store', choices=['f', 'd'],
                        help='検索する対象を指定する．指定がなければどちらも検索する．')
    args = parser.parse_args()

    slack = Slack(args.access_token)

    # 探索するディレクトリのパス
    target = args.path

    name = args.file
    with open(name, mode='rt', encoding='utf-8') as f:
        oldest = f.readlines()
    # 行末の改行文字を削除
    oldest = list(map(lambda x: x.rstrip(), oldest))

    # 実行するコマンド
    if args.type == 'f' or args.type == 'd':
        command = 'find {0} -type {1} | grep -v ".AppleDouble" | grep -v ".DS_Store"'.format(target, args.type)
    else:
        command = 'find {0} | grep -v ".AppleDouble" | grep -v ".DS_Store"'.format(target)

    proc = sb.Popen(
           command,
           shell=True,
           stdin=sb.PIPE,
           stdout=sb.PIPE,
           stderr=sb.PIPE
    )
    latest, err = proc.communicate()
    latest = latest.decode('utf-8').split('\n')

    diff = difference(latest, oldest)
    # 差分があれば投稿
    if len(diff):
        slack.post_message_to_channel(args.channel, name.rstrip('/').split('/')[-1:][0] + "が更新されました", name='諜報部', icon=':nerv:')
        for raw in diff:
            slack.post_message_to_person('D1L0FHJCA', raw.split('\n')[-1:][0] + " が追加されました")

    # ファイル内のリストを更新
    with open(name, mode='wt', encoding='utf-8') as f:
        for raw in latest:
            print(raw, file=f)
