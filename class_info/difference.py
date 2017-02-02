# -*- encoding: utf-8 -*-
from datetime import datetime as dt


def difference(latest, oldest):
    '''
    ２つのファイルからlatestにある行のリストを作る
    '''
    with open(latest, 'r') as f:
        set1 = set(f.readlines())
    with open(oldest, 'r') as f:
        set2 = set(f.readlines())

    return sorted(list(set1.difference(set2)))

if __name__ == '__main__':
    diff = difference('./changes/latest.csv', './changes/oldest.csv')

    for d in diff:
        print(d)

