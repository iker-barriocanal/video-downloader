import requests
import urllib
import re


FB_VIDEO_URL = ''  # Put here fb video url

def download_from_facebook(destination_path, url, quality='hd'):
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
    download_from_facebook('videos/fb_test.mp4', FB_VIDEO_URL)
