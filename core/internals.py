from slugify import SLUG_OK, slugify
from core.const import log

import os


def input_link(links):
    """ Let the user input a choice. """
    while True:
        try:
            log.info('Choose your number:')
            the_chosen_one = int(input('> '))
            if 1 <= the_chosen_one <= len(links):
                return links[the_chosen_one - 1]
            elif the_chosen_one == 0:
                return None
            else:
                log.warning('Choose a valid number!')
        except ValueError:
            log.warning('Choose a valid number!')


def trim_song(text_file):
    """ Remove the first song from file. """
    with open(text_file, 'r') as file_in:
        data = file_in.read().splitlines(True)
    with open(text_file, 'w') as file_out:
        file_out.writelines(data[1:])


def is_spotify(raw_song):
    """ Check if the input song is a Spotify link. """
    status = len(raw_song) == 22 and raw_song.replace(" ", "%20") == raw_song
    status = status or raw_song.find('spotify') > -1
    return status


def is_youtube(raw_song):
    """ Check if the input song is a YouTube link. """
    status = len(raw_song) == 11 and raw_song.replace(" ", "%20") == raw_song
    status = status and not raw_song.lower() == raw_song
    status = status or 'youtube.com/watch?v=' in raw_song
    return status


def generate_songname(tags):
    """ Generate a string of the format '[artist] - [song]' for the given spotify song. """
    raw_song = u'{0} - {1}'.format(tags['artists'][0]['name'], tags['name'])
    return raw_song


def sanitize_title(title):
    """ Generate filename of the song to be downloaded. """
    title = title.replace(' ', '_')
    title = title.replace('/', '_')

    # slugify removes any special characters
    title = slugify(title, ok='-_()[]{}', lower=False)
    return title


def filter_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
    for temp in os.listdir(path):
        if temp.endswith('.temp'):
            os.remove(os.path.join(path, temp))


def videotime_from_seconds(time):
    if time<60:
        return str(time)
    if time<3600:
        return '{}:{}'.format(str(time//60), str(time%60).zfill(2))

    return '{}:{}:{}'.format(str(time//60),
                             str((time%60)//60).zfill(2),
                             str((time%60)%60).zfill(2))
