# -*- coding: utf-8 -*-
import sys

from difference import difference

if __name__ == '__main__':
    name1 = sys.argv[1]
    name2 = sys.argv[2]

    print(name1, name2)

    with open(name1, mode='rt', encoding='utf-8') as f1:
        with open(name2, mode='rt', encoding='utf-8') as f2:
            list1 = f1.readlines()
            list2 = f2.readlines()

            print('list1', len(list1))
            print('list2', len(list2))

            diff = difference(list1, list2)

            print('diff')
            for raw in diff:
                print(raw)

