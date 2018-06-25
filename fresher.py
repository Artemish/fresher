#!/usr/bin/env python3.6
import os
import re
import json
import argparse
import pprint

FRESHER_DIR=os.path.expanduser("~")+"/.fresher"
FRESHER_CACHE=f"{FRESHER_DIR}/cache.json"

MUSIC_DIRECTORY = "/home/mitch/Music"
MUSIC_REGEX = "(.+)\.(mp3|ogg|opus|m4a|mp4)$"

def populate_scores(music_dir):
    exploration_queue = [MUSIC_DIRECTORY]
    song_scores = {}

    while len(exploration_queue) != 0:
        d = exploration_queue.pop()
        for fname in os.listdir(d):
            abs_path = f"{MUSIC_DIRECTORY}/{fname}"
            if os.path.isfile(abs_path):
                m = re.match(MUSIC_REGEX, fname)
                if m is not None:
                  title = m.groups()[0]
                  song_scores[title] = 0
                elif os.path.isdir(abs_path):
                  exploration_queue.append(abs_path)
    
    return song_scores

def write_data(song_scores):
    with open(FRESHER_CACHE, 'w') as f:
        json.dump(song_scores, f)

def read_data():
    with open(FRESHER_CACHE, 'r') as f:
        song_scores = json.load(f)

    return song_scores

def load_data():
    if not os.path.exists(FRESHER_DIR):
        os.mkdir(FRESHER_DIR)

    if not os.path.exists(FRESHER_CACHE):
        song_scores = populate_scores(MUSIC_DIRECTORY)
        write_data(song_scores)
        return song_scores
    else:
        return read_data()

def update(title, adjustment, song_scores):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fresher - freshen your music library')
    parser.add_argument('command', metavar='command', type=str, help='What to do')
    args = parser.parse_args()
    
    song_scores = load_data()

    if args.command == "show":
        pprint.pprint(song_scores)
    elif args.command == "update":
        pass
    else:
        pass
