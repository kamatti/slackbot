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
  settings = parse_json(args['f'])["team"]["kaz_lab"]
  print(settings)

  # アクセストークンを取得
  token = settings["access_token"]
  # slack = Slack(token)

  # 更新確認したい場所に移動
  os.chdir(args["path"])

  command = "git status -s"
  # (左辺).stdout.read()で出力内容を得る
  # ただし型は<bytes>で末尾に\nを含む
  command_results = sp.Popen(shlex.split(command), stdout=sp.PIPE)
  
  results = command_results.stdout.read().decode("utf-8")

  # 追加されたファイル一覧を取得する
  added_files = []
  for raw in results.rstrip().split("\n"):
    status = raw.split()[0]
    path = raw.split()[1]

    if status == "??":
      added_files.append(path)

  print(added_files)

  # 追加ファイル一覧をいい感じに整形する

  # slack.post_message_to_channel(settings["channel"], hoge)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="ファイル監視スクリプト")
  parser.add_argument("-p", type=str, help="target path", required=True)
  parser.add_argument("-f", type=str, help="setting file(.json)", required=True)

  args = parser.parse_args()
  main(path=args.p, f=args.f)
