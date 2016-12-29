# -*- encoding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

html = urlopen('http://hirose.sendai-nct.ac.jp/kyuko/kyuko.cgi')
soup = BeautifulSoup(html, 'html.parser')

tables = soup.findAll('table', {'width': '650'})

csvFile = open('change_class.csv', 'wt', newline='', encoding='utf-8')
writer = csv.writer(csvFile)

try:
    for row in tables:
        info = []
        # 日付，クラス，時間を取得
        for cell in row.findAll('b'):
            info.append(cell.get_text())
        # 教員名を取得(fontタグで指定)
        info.append(row.find('font', {'color': '#00008B'}).get_text().rstrip())
        # 変更の状態(休講，変更)を画像イメージのsrcから判断
        img = row.find('img')['src'][6:]
        info.append(img)
        # 教科名を取得
        info.append(row.find('table').find('font').get_text())
        # 取得したデータを書き込む
        writer.writerow(info)
finally:
    csvFile.close()
