# Folder-synchronization
Synchronization of two folders - one way

This is a program that performs one-way synchronization of two folders.
 - Synchronization is carried out periodically and changes(file update, copying, removal operations) are displayed in the console and written to a log file.
 - Folder paths, synchronization intervals, and log file paths will be provided using command-line arguments

## Requirements
 - Python 3
 - Libraries os, shutil, time, logging, argparse, watchdog

### How to Use
 - Python 3 installed on your system
 - Watchdog library installed - use pip install watchdog

#### How to run the script
 - python3 main.py --source SOURCE --replica REPLICA --time-interval interval --log-file LOG_FILE.txt
 - --source: Path to the source folder to be synchronized (default: "source").
 - --replica: Path to the replica folder that will be updated to match the source folder (default: "replica").
 - --time-interval: Time interval for synchronization in seconds (default: 30).
 - --log-file: Path to the log file (default: "logfile.txt").
 
   

##### Notes
 - The script first clears the replica folder.
 - If a replica folder doesn't exist it will create one.
 - The content of the source file will be copied to the replica folder on a specified interval (default one is 30 seconds, which will be overwritten by the console input)
 - Every change made to the source folder like folder creation, folder deletion, file creation, file renaming, and so on.. it's observed by the Observer class and logged to the console and a log file.
 - To stop the script manually, use the keyboard interrupt (CTRL+C).
 
