# -*- coding: UTF-8 -*-

from core import const
from core import handle
import spotdl

import os

const.args = handle.get_arguments(to_group=False, raw_args='')
const.args.folder = 'test'
const.args.overwrite = 'skip'
const.args.log_level = handle.logging.DEBUG

spotdl.args = const.args
spotdl.log = const.logzero.setup_logger(formatter=const.formatter,
                                  level=const.args.log_level)


raw_song = "Tony's Videos VERY SHORT VIDEO 28.10.2016"

def test_youtube_url():
    expect_url = 'http://youtube.com/watch?v=qOOcy2-tmbk'
    url = spotdl.youtube_tools.generate_youtube_url(raw_song, meta_tags=None)
    assert url == expect_url


def test_youtube_title():
    global content
    global title
    expect_title = "Tony's Videos VERY SHORT VIDEO 28.10.2016"
    content = spotdl.youtube_tools.go_pafy(raw_song, meta_tags=None)
    title = spotdl.youtube_tools.get_youtube_title(content)
    assert title == expect_title

def test_check_exists():
    expect_check = False
    # prerequisites for determining filename
    file_name = spotdl.internals.sanitize_title(title)
    check = spotdl.check_exists(file_name, raw_song, meta_tags=None)
    assert check == expect_check


def test_download():
    expect_download = True
    # prerequisites for determining filename
    file_name = spotdl.internals.sanitize_title(title)
    download = spotdl.youtube_tools.download_song(file_name, content)
    assert download == expect_download


def test_convert():
    # exit code 0 = success
    expect_convert = 0
    # prerequisites for determining filename
    file_name = spotdl.internals.sanitize_title(title)
    global input_song
    global output_song
    input_song = file_name + const.args.input_ext
    output_song = file_name + const.args.output_ext
    convert = spotdl.convert.song(input_song, output_song, const.args.folder)
    assert convert == expect_convert


def test_metadata():
    expect_metadata = None
    # prerequisites for determining filename
    meta_tags = spotdl.spotify_tools.generate_metadata(raw_song)
    file_name = spotdl.internals.sanitize_title(title)
    if meta_tags:
        metadata_output = spotdl.metadata.embed(os.path.join(const.args.folder, output_song), meta_tags)
        metadata_input = spotdl.metadata.embed(os.path.join(const.args.folder, input_song), meta_tags)
    else:
        metadata_input = None
        metadata_output = None
    assert (metadata_output == expect_metadata) and (metadata_input == expect_metadata)


def test_check_exists2():
    expect_check = True
    # prerequisites for determining filename
    file_name = spotdl.internals.sanitize_title(title)
    os.remove(os.path.join(const.args.folder, input_song))
    check = spotdl.check_exists(file_name, raw_song, meta_tags=None)
    os.remove(os.path.join(const.args.folder, output_song))
    assert check == expect_check
