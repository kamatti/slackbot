# -*- encofing: utf-8 -*-
import csv
import re
import copy

def make_attachment(csvFile):
    """
    授業変更通知用のattachmentを生成
    ディクショナリをリストでまとめて返す
    """
    f = open(csvFile, 'rt')
    reader = csv.reader(f)

    # 返り値にするためのリスト
    attachments = []

    attachment = {
        'title': '授業変更情報',
        'title_link': 'http://hirose.sendai-nct.ac.jp/kyuko/',
        'fallback': '授業変更情報',
        'color': '#FF0000',
        'image_url': '',
        'text': '',
    }

    # クソみたいなあれに対応するためのゴリラみたいな正規表現
    pattern = '\A([4INA]|[４ＩＮＡ全]).?.?[^1-35]([4LN]|[４ＬＮ全])\Z'
    for row in reader:
        attachment['text'] = ''
        # 高専のHPの画像そのまま使う
        # TODO:どうにかローカルに保存された画像を使えないか
        attachment['image_url'] = 'http://hirose.sendai-nct.ac.jp/kyuko/img/'
        if re.match(pattern, row[1]):
            attachment['text'] += row[0] + '\n'
            attachment['text'] += row[2] + '\n'
            attachment['text'] += row[5]
            attachment['image_url'] += row[4]
            attachments.append(copy.deepcopy(attachment))

    f.close()

    return attachments

if __name__ == "__main__":
    make_attachment('2016122921_change_info.csv')
