# video-downloader
video-downloader is a simple script to download videos from YouTube and Facebook.

## Getting started
In order to use the project, python3 and the libraries in `requirements.txt` are needed.

The requirements can be installed as follows:
```
pip install -r requirements.txt
```

## Usage

### Getting help
You can ask for help by running either of the following options:
```
python3 video_downloader.py -h
python3 video_downloader.py --help
```
```
usage: video_downloader.py [-h] [-o [OUTPUT]] [-r RESOLUTION] {fb,yt} url

Downloads videos from some platforms on the internet.

positional arguments:
  {fb,yt}               Selects the platform to download videos from.
  url                   The URL of the video to be downloaded.

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        Output file
  -r RESOLUTION, --resolution RESOLUTION
                        Quality of the video.
```

### Default values
Every flag has a default value but the url.
- The output file, if not given, will follow the following pattern: `video_YYYY_MM_DD_mmmmmm` (`m` stands for microseconds).
- The resolution will always be the maximum available resolution for the given video.

### YouTube
In order to download videos from YouTube, only the positional arguments are needed.
The [pytube](https://python-pytube.readthedocs.io/en/latest/index.html) library has been used to interact with this platform.

By default, the maximum quality is selected (or by setting `max` in `resolution`), but any resolution can be selected (e.g. `480p`, `1080p`). However, there might be issues with the codecs (both audio and video codecs are needed), and an error message will be printed if they are not available.
Thus, it's recommended to select `max` (or don't select anything), since always selects the video of maximum resolution with both codecs available.

Examples (substitute `<url>` with the url of the video, and `<output file>` with the path and name to the desired file):
```
python3 video_downloader.py yt <url> -o <output file>
python3 video_downloader.py yt <url> -o <output file> -r max
python3 video_downloader.py yt <url> -o <output file> -r 720p
```

### Facebook
Downloading videos from Facebook is similar to the YouTube approach. The difference here is the available quality options given in the resolution flag, only `sd` and `hd` (default choice) are possible.

Examples (substitute <url> with the url of the video, and <output file> with the path and name to the desired file):
```
python3 video_downloader.py fb <url> -o <output file>
python3 video_downloader.py fb <url> -o <output file> -r hd
```