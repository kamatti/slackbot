# -*- coding: utf-8 -*-

import time
import os

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

def getext(filename):
  return os.path.splitext(filename)[-1].lower()

class ChangeHandler(FileSystemEventHandler):
  
  def on_created(self, event):
    if event.is_directory:
      return
    if getext(event.src_path) in ('.jpg', '.png', '.txt'):
      print('{} has been created.'.format(event.src_path))

  def on_modified(self, event):
    if event.is_directory:
      return
    if getext(event.src_path) in ('.jpg', '.png', '.txt'):
      print('{} has been modified.'.format(event.src_path))

  def on_deleted(self, event):
    if event.is_directory:
      return
    if getext(event.src_path) in ('.jpg', '.png', '.txt'):
      print('{} has been deleted.'.format(event.src_path))

def main():
  BASE_DIR = os.path.abspath(os.path.dirname(__file__))

  while True:
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, BASE_DIR, recursive=True)
    observer.start()
    try:
      while True:
        time.sleep(1)
    except KeyboardInterrupt:
      observer.stop()
    observer.join()

if __name__ in '__main__':
  main()
