# -*- coding:utf-8 -*-

import os
import argparse
import json

import subprocess as sp
import shlex


def parse_json(path):
  with open(path, "rt") as f:
    data = json.load(f)
  return data

def main(**args):
  print(args)
  settings = parse_json(args['f'])
  print(settings)

  command = "git status -s"
  # (左辺).stdout.read()で出力内容を得る
  # ただし型は<bytes>で末尾に\nを含む
  command_results = sp.Popen(shlex.split(command), stdout=sp.PIPE)
  
  results = command_results.stdout.read().decode("utf-8")

  added_files = []
  for raw in results.rstrip().split("\n"):
    status = raw.split()[0]
    path = raw.split()[1]

    if status == "??":
      added_files.append(path)

  print(added_files)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="ファイル監視スクリプト")
  parser.add_argument("-p", type=str, help="target path", required=True)
  parser.add_argument("-f", type=str, help="setting file(.json)", required=True)

  args = parser.parse_args()
  main(path=args.p, f=args.f)
