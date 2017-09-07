# -*- coding:utf-8 -*-

import subprocess as sp
import shlex

def main():
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
  main()
