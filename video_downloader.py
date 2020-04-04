import requests
import urllib
import re
import argparse
import sys
import os


def _add_program_args():
    arg_parser = argparse.ArgumentParser(description="Downloads videos from Facebook.")
    arg_parser.add_argument('video_url', type=str, nargs=1, metavar='url', help="The URL of the video to be downloaded.")
    arg_parser.add_argument('-o', '--output', type=str, nargs='?', default=os.path.abspath(os.path.dirname(sys.argv[0])), help="Output file")
    arg_parser.add_argument('-q', '--quality', type=str, nargs='?', choices={'sd', 'hd'}, default='hd', help="Quality of the video")

    return arg_parser.parse_args()


def download_video_from_facebook(destination_path, url, quality='hd'):
    # Quality can also be 'sd'

    request = requests.get(url)
    quality_prefix = quality + '_src:'

    # Look for the actual video url
    url = re.search(quality_prefix + '"(.+?)"', request.text)[0]
    url = url.replace(quality_prefix, '')
    url = url.replace('"', '')
    
    # Save the video
    urllib.request.urlretrieve(url, destination_path)


if __name__ == "__main__":
    args = _add_program_args()
    download_video_from_facebook(args.output, args.video_url[0], args.quality)
