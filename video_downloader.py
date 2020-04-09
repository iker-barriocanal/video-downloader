import sys
import os
import urllib
import re
import argparse
from datetime import datetime
import requests
from pytube import YouTube


FILE_EXTENSION_PATTERN = re.compile(r'\.\w+$')
FILENAME_PATTERN = re.compile(r'\w+$')
DIRECTORY_PATTERN = re.compile(r'^.?/?([\w\-]+/)*')
FB_VIDEO_URL_PATTERN = '"(.+?)"'  # The prefix with the desired quality is missing: (hd|sd)_src:

EXIT_NO_CODECS = "There are no streams with video and audio codecs available for this video."
EXIT_NO_CODECS_CUSTOM_RES = "No streams found with both audio and video codecs. Try setting the resolution to max."


def _add_program_args():
    arg_parser = argparse.ArgumentParser(description="Downloads videos from some platforms on the internet.")
    arg_parser.add_argument('platform', type=str, nargs=1, choices=['fb', 'yt'],
                            help="Selects the platform to download videos from.")
    arg_parser.add_argument('video_url', type=str, nargs=1, metavar='url',
                            help="The URL of the video to be downloaded.")
    arg_parser.add_argument('-o', '--output', type=str, nargs='?', default=None, help="Output file")
    arg_parser.add_argument('-r', '--resolution', type=str, nargs=1, default='max', help="Quality of the video.")

    return arg_parser.parse_args()


def _parse_args(args_to_parse):
    args_to_parse.platform = args_to_parse.platform[0]
    args_to_parse.video_url = args_to_parse.video_url[0]
    if args_to_parse.output is None:
        args_to_parse.output = os.path.abspath(os.path.dirname(sys.argv[0]))
        args_to_parse.output = args_to_parse.output + '/video_' + datetime.today().strftime(r'%Y_%m_%d_%f') + '.mp4'
    if isinstance(args_to_parse.resolution, list):
        args_to_parse.resolution = args_to_parse.resolution[0]

    if args_to_parse.platform == 'fb' and args_to_parse.resolution == 'max':
        args_to_parse.resolution = 'hd'

    return args_to_parse


def download_video_from_facebook(destination_path, url, quality='hd'):
    request = requests.get(url)
    quality_prefix = quality + '_src:'
    # Look for the actual video url
    url = re.search(quality_prefix + FB_VIDEO_URL_PATTERN, request.text)[0]
    url = url.replace(quality_prefix, '')
    url = url.replace('"', '')
    # Save the video
    urllib.request.urlretrieve(url, destination_path)


def download_video_from_youtube(destination_path, url, resolution):
    yt_video = YouTube(url)
    # Porgressive streams are these with both audio and video codecs.
    progressive_streams = yt_video.streams.filter(progressive=True)
    if len(progressive_streams) == 0:
        sys.exit(EXIT_NO_CODECS)
    if resolution == 'max':
        stream = progressive_streams.get_highest_resolution()
    else:
        progressive_streams_custom_resolution = progressive_streams.filter(res=resolution)
        if len(progressive_streams_custom_resolution) == 0:
            sys.exit(EXIT_NO_CODECS_CUSTOM_RES)
        stream = progressive_streams_custom_resolution.last()

    # Extract file info
    destination_path = re.sub(FILE_EXTENSION_PATTERN, '', destination_path)  # Remove file extension, if any
    out_name = re.search(FILENAME_PATTERN, destination_path)[0]
    out_path = re.search(DIRECTORY_PATTERN, destination_path)[0]

    stream.download(output_path=out_path, filename=out_name)


if __name__ == "__main__":
    args = _add_program_args()
    args = _parse_args(args)
    if args.platform == 'fb':
        download_video_from_facebook(destination_path=args.output, url=args.video_url, quality=args.resolution)
    elif args.platform == 'yt':
        download_video_from_youtube(destination_path=args.output, url=args.video_url, resolution=args.resolution)
