# -*- coding: utf-8 -*-

import time
import pyinotify

class Handler(pyinotify.ProcessEvent):

  def process_IN_CREATE(self, event):
    #print("{} has been created.".format(event))
    print(event)
    
  def process_IN_DELETE(self, event):
    #print("{} has been deleted.".format(event))
    print(event)

  def process_IN_MODIFY(self, event):
    #print("{} has been modified.".format(event))
    print(event)

def main():
  wm = pyinotify.WatchManager()

  notifier = pyinotify.ThreadedNotifier(wm, Handler())
  notifier.start()

  mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY

  #wdd = wm.add_watch('/home/squid/nas/work/趣味/うp依頼品', mask)
  wdd = wm.add_watch('/home/squid/', mask)

  while True:
    time.sleep(1)
  
  notifier.stop()


if __name__ == "__main__":
  main()
