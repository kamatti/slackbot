#-*- coding: utf-8 -*-
import sys
import subprocess as sb

if __name__ == "__main__":
  if len(sys.argv) <= 2:
    print('Usage: {} save_file_name command <arg...>'.format(sys.argv[0]))
    sys.exit()
  command = sys.argv[2:]
  filename = sys.argv[1]
  #print(command, filename)

  result = sb.run(command, stdout=sb.PIPE).stdout.decode('utf-8').split('\n')

  with open(filename, mode='wt', encoding='utf-8') as f:
    for i, raw in enumerate(result):
      print(raw, file=f)

