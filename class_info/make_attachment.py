# -*- encofing: utf-8 -*-
import csv
import re
import copy
from datetime import datetime as dt


def make_attachment(csvFile, pattern):
    """
    授業変更通知用のattachmentを生成
    ディクショナリをリストでまとめて返す
    """
    with open(csvFile, 'rt') as f:
        reader = csv.reader(f)

        # 返り値にするためのリスト
        attachments = []

        attachment = {
            'title': '',
            'title_link': 'http://hirose.sendai-nct.ac.jp/kyuko/',
            'fallback': '',
            'color': '',
            'image_url': '',
            'text': '',
        }

        # クソみたいなあれに対応するためのゴリラみたいな正規表現
        # pattern = '\A([4INA]|[４ＩＮＡ全]).?.?[^1-35]([4LN]|[４ＬＮ全])\Z'
        for row in reader:
            attachment['text'] = ''
            # 高専のHPの画像そのまま使う
            # TODO:どうにかローカルに保存された画像を使えないか
            attachment['image_url'] = 'http://hirose.sendai-nct.ac.jp/kyuko/img/'
            if re.match(pattern, row[1]):
                attachment['text'] += row[0] + '\n'     # 日付
                attachment['text'] += row[2] + '\n'     # 時限
                attachment['text'] += row[5]            # 教科
                attachment['image_url'] += row[4]       # 画像のurl
                # 通知で変更情報か休講情報か
                if re.match('henko', row[4]):
                    attachment['text'] = row[1] + '変更情報\n' + attachment['text']
                    attachment['fallback'] = row[1] + '変更情報'
                    attachment['color'] = '#00FF00'
                elif re.match('kyuko', row[4]):
                    attachment['text'] = row[1] + '休講情報\n' + attachment['text']
                    attachment['fallback'] = row[1] + '休講情報'
                    attachment['color'] = '#FF0000'
                else:
                    # 登録側のシステムが変わらない限りここは通らない
                    attachment['fallback'] = '管理者に連絡してください'
                attachments.append(copy.deepcopy(attachment))

    return attachments

if __name__ == "__main__":
    filename = dt.now().strftime('%Y%m%d') + '_change_info.csv'
    attachments = make_attachment(filename)

    for e in attachments:
        print(e)
