# -*- encoding: utf-8 -*-
from datetime import datetime as dt


def difference(latest, oldest):
    '''
    ２つのリストからlatestにある行のリストを作る
    '''
    set1 = set(latest)
    set2 = set(oldest)

    # 集合にすると順番保証されなくなるから日付順でソート
    return list(set1.difference(set2)))

if __name__ == '__main__':
    diff = difference(['tets', 'tttt'], ['asdf', 'tttt'])

    for d in diff:
        print(d.rstrip())
