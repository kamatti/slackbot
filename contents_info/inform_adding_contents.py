# -*- coding: utf-8 -*-
from slacker import Slacker

import subprocess as sb
import sys   # 引数取得
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

def read_json_file(path):
    with open(path, 'rt') as f:
        date = json.load(f)
    return date

def difference(latest, oldest):
    '''
    ２つのリストからlatestにある行のリストを作る
    '''
    set1 = set(latest)
    set2 = set(oldest)

    return list(set1.difference(set2))


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print('Usage : python {} "setting file(.json)" "team name"'.format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    # 設定ファイルの読み込み
    settings = read_json_file(sys.argv[1])
    team = settings['team'][sys.argv[2]]

    slack = Slack(team['access_token'])

    prefix = '/home/squid/nas/'

    # エラー出力用
    err = open('/dev/null', mode='w')

    for target in team['target']:
        oldest = []
        latest = []

        # targetのパスから対象のディレクトリ名を抜き出してそれをファイル名にする
        name = target.rstrip('/').split('/')[-1:][0]
        with open(name, mode='rt', encoding='utf-8') as f:
            oldest = f.readlines()
        # 行末の改行文字を削除
        oldest = list(map(lambda x: x.rstrip(), oldest))

        # コマンドの実行結果をリストにする
        latest = sb.run(['ls', '-lR', prefix + target], stdout=sb.PIPE, stderr=err).stdout.decode('utf-8').split('\n')

        diff = difference(latest, oldest)
        # 差分があれば投稿
        if len(diff):
            slack.post_message_to_channel(team['channel'], name + "が更新されました", name='お知らせ君', icon=':white-glass:')

        # ファイル内のリストを更新
        with open(name, mode='wt', encoding='utf-8') as f:
            for raw in latest:
                print(raw, file=f)
    err.close()
