import os
import filecmp
import shutil
import time
import logging
import argparse
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


def sync_folder(src, dst, time_interval):
    if not os.path.isdir(dst):
        os.makedirs(dst)
    while True:
        time.sleep(time_interval)
        compare_folders(src, dst)


def compare_files(file1, file2):
    return filecmp.cmp(file1, file2, shallow=False)


def compare_folders(src, dst):
    files_src = os.listdir(src)
    files_dst = os.listdir(dst)

    for file in files_src:
        src_file_path = os.path.join(src, file)
        dst_file_path = os.path.join(dst, file)

        if file in files_dst:
            if compare_files(src_file_path, dst_file_path):
                continue
            else:
                os.remove(dst_file_path)
                shutil.copy2(src_file_path, dst_file_path)
        else:
            shutil.copy2(src_file_path, dst_file_path)

    for file in files_dst:
        if file not in files_src:
            os.remove(os.path.join(dst, file))
                    

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
    sync_folder(args.source, args.replica, args.interval)
    
