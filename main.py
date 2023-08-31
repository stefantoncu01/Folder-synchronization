import os
import shutil
import time
import logging
import argparse
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


def sync_target_folder(src, dst):
    if not os.path.isdir(dst):
        os.makedirs(dst)
    shutil.copytree(src, dst, dirs_exist_ok=True)


def clear_folder_content(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for item in os.listdir(folder):
        file_path = os.path.join(folder, item)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, help='the path to the source folder')
    parser.add_argument('--replica', type=str, help='the path to the replica folder')
    parser.add_argument('--interval', type=int, default=30, help='time between synchronizations in seconds')
    parser.add_argument('--log_file', type=str, default='logfile.txt', help='the path to the log file')

    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s:%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.FileHandler(args.log_file),
                            logging.StreamHandler()]
                        )
    logging.info(f'start watching directory {args.source!r}')
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, args.source, recursive=True)
    observer.start()

    while True:
        time.sleep(args.interval)
        clear_folder_content(args.replica)
        sync_target_folder(args.source, args.replica)
