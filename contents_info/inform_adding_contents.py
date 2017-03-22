# -*- coding: utf-8 -*-
from slacker import Slacker

import subprocess as sb
import argparse
import re
import os.path

class Slack(object):

    __slacker = None

    def __init__(self, token):

        self.__slacker = Slacker(token)

    def post_message_to_channel(self, channel, message):
        """
        Slackチームの任意のチャンネルにメッセージを投稿する。
        """

        channel_name = "#" + channel.lstrip('#')
        # slack.Response classはメンバbodyにjson形式でデータ持ってる
        self.__slacker.chat.post_message(channel_name, message, as_user=True)

    def post_message_to_person(self, channel, message):
        """
        Slackチームの任意のチャンネルにメッセージを投稿する。
        """

        self.__slacker.chat.post_message(channel, message, as_user=True)


def difference(latest, oldest):
    '''
    ２つのリストからlatestにある行のリストを作る
    '''
    set1 = set(latest)
    set2 = set(oldest)

    return list(set1.difference(set2))

def get_titles(path):
    '''
    パスの中からタイトルと巻数(comics限定)を
    抜き出してタプルにしてそれをリストにまとめて返す．
    '''
    titles = []

    for raw in path:
        volume = ''
        # 巻数を抜き出す．なければからの文字列になる．
        m = re.search('第[0-9]*巻$', raw)
        if m:
            volume = m.group()
        # タイトルを抜き出す
        # 巻数を消去
        tmp = re.sub('第[0-9]*巻.*$', '', raw)
        # 拡張子を分離
        result, _ = os.path.splitext(tmp)
        titles.append((result.rstrip('/').split('/')[-1:][0], volume))

    return sorted(list(set(titles)))

def is_exist(elem, target):
    '''
    targetリスト内にelemがあるかどうか
    '''

    for e in target:
        if re.search(elem, e):
            return True
    return False


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
    # 行末に/が必ずあるようにする
    target = args.path.rstrip('/') + '/'

    # 過去ファイルへのパス
    name = args.file
    with open(name, mode='rt', encoding='utf-8') as f:
        oldest = f.readlines()
    # 行末の改行文字を削除
    oldest = list(map(lambda x: x.rstrip(), oldest))

    # 実行するコマンド
    # '.'から始まる隠しファイルは無視
    if args.type == 'f' or args.type == 'd':
        command = 'find {0} -type {1} | grep -v ".*/\..*"'.format(target, args.type)
    else:
        command = 'find {0} | grep -v ".*/\..*"'.format(target)

    proc = sb.Popen(
           command,
           shell=True,
           stdin=sb.PIPE,
           stdout=sb.PIPE,
           stderr=sb.PIPE
    )
    result, _ = proc.communicate()
    # latest = result.decode('utf-8').split('\n')
    with open('res_anime', mode='rt', encoding='utf-8') as f:
        latest = f.readlines()
    latest = list(map(lambda x: x.rstrip(), latest))
    #latest = latest.split('\n')
    # print(latest)
    pattern = '\A.*/' + target.rstrip('/').split('/')[-1:][0] + '/'
    latest = list(map(lambda x: re.sub(pattern, '', x), latest))
    latest = list(map(lambda x: re.sub('単ページ', '', x), latest))

    diff = difference(latest, oldest)

    # ディレクトリのナンバリングが消去されただけの差分を消去
    for raw in oldest:
        temp = re.sub('\A[0-9]* ', '', raw)
        try:
            diff.remove(temp)
        except ValueError:
            pass
        finally:
            pass

    titles = get_titles(diff)

    # 途中のディレクトリ名が変更されただけの行を削除
    for title, volume in titles:
        if is_exist(title, oldest):
            try:
                titles.remove((title, volume))
            except ValueError:
                pass
            finally:
                pass

    # 差分がなければこのループに入らないから投稿しない
    arranges = []
    for title, volume in titles:
        message = ""
        # 新しいものが追加されたとき余計なものが出ないように対策
        if name.rstrip('/').split('/')[-1:][0] == 'comics' and not volume:
            continue
        # パス中のディレクトリ名が変更されただけの場合の対策
        if is_exist(title, oldest):
            arranges.append(title)
            continue
        message += name.rstrip('/').split('/')[-1:][0]
        message += " : "
        message += title
        if volume:
            message += " "
            message += volume
        print(message)
        # slack.post_message_to_channel(args.channel, message)

    # ディレクトリにまとめられたものを通知
    arrange = []
    for raw in arranges:
        for d in diff:
            if re.search(raw, d):
                arrange.append(d.rstrip('/').split('/')[0])
    print(arrange)
    print(set(arrange))
    for title in set(arrange):
        message = ''
        message += title
        message += 'がまとめられました'
        print(message)
        # slack.post_message_to_channel(args.channel, message)


    # ファイル内のリストを更新
    with open(name, mode='wt', encoding='utf-8') as f:
        pattern = '\A.*/' + target.rstrip('/').split('/')[-1:][0] + '/'
        for raw in latest:
            content = raw
            content = re.sub(pattern, '', raw)
            print(content, file=f)
