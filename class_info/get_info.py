# -*- encoding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from datetime import datetime as dt


def get_info(filename):
    """
    仙台高専広瀬の授業変更ページから変更，休講情報を抜き出してcsvとして保存する．
    授業変更ページの構成が残念なのでだいぶ無理やり情報を取得している．
    pram : filename -> 保存するファイル名
    """
    html = urlopen('http://hirose.sendai-nct.ac.jp/kyuko/kyuko.cgi')
    soup = BeautifulSoup(html, 'html.parser')

    # 変更情報はtable width=650に記載されている
    tables = soup.findAll('table', {'width': '650'})

    csvFile = open(filename, mode='wt', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)

    try:
        for row in tables:
            info = []
            # 日付，クラス，時間を取得
            for cell in row.findAll('b'):
                info.append(cell.get_text())
            # 教員名を取得(fontタグで指定)
            info.append(
                row.find('font', {'color': '#00008B'}).get_text().rstrip())
            # 変更の状態(休講，変更)を取得(画像のsrcタグで判断)
            img = row.find('img')['src'][6:]
            info.append(img)
            # 教科名を取得
            info.append(row.find('table').find('font').get_text())
            # 取得したデータを書き込む
            writer.writerow(info)
    finally:
        csvFile.close()

if __name__ == '__main__':
    # filename = '/Users/kamachi/slackbot/class_info/changes/' + dt.now().strftime('%Y%m%d') + '_change_info.csv'
    filename = './changes/latest.csv'
    get_info(filename)
