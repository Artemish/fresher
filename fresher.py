#!/usr/bin/env python3.6
import os
import re
import json
import argparse
import pprint
import collections

FRESHER_DIR=os.path.expanduser("~")+"/.fresher"
FRESHER_CACHE=f"{FRESHER_DIR}/cache.json"

MUSIC_DIRECTORY = "/home/mitch/Music"
MUSIC_REGEX = "(.+)\.(mp3|ogg|opus|m4a|mp4)$"

BASE_SCORE=100

def populate_scores(music_dir = MUSIC_DIRECTORY):
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
                  song_scores[title] = BASE_SCORE
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
        song_scores = populate_scores()
        write_data(song_scores)
        return song_scores
    else:
        return read_data()

def selection_prompt(song_titles):
    for i in range(len(song_titles)):
        print(f"\t[{i}] " + song_titles[i])
    selection = input("Selection: ")
    return song_titles[int(selection)]

def find_by_title(title, song_scores):
    all_titles = song_scores.keys()
    matching_titles = list(filter(lambda t: title.lower() in t.lower(), all_titles))

    if len(matching_titles) == 1:
        return matching_titles[0]
    elif len(matching_titles) > 1:
        return selection_prompt(matching_titles)
    else:
        raise RuntimeError(f"No song matching '{title}' was found.")

def handle_upvote(args):
    song_scores = load_data()
    update(args.title, args.score, song_scores)

def handle_downvote(args):
    song_scores = load_data()
    update(args.title, -1 * args.score, song_scores)

def update(title, adjustment, song_scores):
    full_title = find_by_title(title, song_scores)
    song_scores[full_title] += adjustment
    write_data(song_scores)
    print(f"Adjusted '{full_title}' by {adjustment} points.")

def get_parser(): 
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='commands')

    # Show command
    show_parser = subparsers.add_parser('show', help='Dump the score dictionary')
    show_parser.set_defaults(func=handle_show)

    # Repopulate command
    repopulate_parser = subparsers.add_parser('repopulate', help='Repopulate and reset the score dictionary')
    repopulate_parser.set_defaults(func=handle_repopulate)

    # Upvote command
    upvote_parser = subparsers.add_parser('upvote', help='Upvote the currently playing song')
    upvote_parser.add_argument('title', action='store', type=str, help='Title of the song to upvote')
    upvote_parser.add_argument('score', action='store', type=int, default=10, help='How much to increase the song score')
    upvote_parser.set_defaults(func=handle_upvote)

    # Upvote command
    downvote_parser = subparsers.add_parser('downvote', help='Downvote the currently playing song')
    downvote_parser.add_argument('title', action='store', type=str, help='Title of the song to downvote')
    downvote_parser.add_argument('score', action='store', type=int, default=10, help='How much to decrease the song score')
    downvote_parser.set_defaults(func=handle_downvote)

    return parser

def handle_show(args):
    song_scores = load_data()
    pprint.pprint(song_scores)

def handle_repopulate(args):
    scores = load_data()
    new_scores = populate_scores()

    songs = set(scores.keys())
    new_songs = set(new_scores.keys())

    for song in (new_songs - songs):
        print(f"Registering {song}.")
        scores[song] = new_scores[song]

    for song in (songs - new_songs):
        print(f"Deregistering {song}.")
        del scores[song]

    write_data(scores)

    print("Repopulated the score data")

if __name__ == "__main__":
    global args
    parser = get_parser()

    args = parser.parse_args()

    args.func(args)
