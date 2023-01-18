# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/utility/video_downloader.ipynb.

# %% auto 0
__all__ = ['Chapter', 'VideoMetadata', 'download_video_and_extract_info', 'parse_video_metadata']

# %% ../nbs/utility/video_downloader.ipynb 1
import yt_dlp
import dataclasses
from typing import List, Dict, Any
from pathlib import Path
from .data_utils import *
import json

# %% ../nbs/utility/video_downloader.ipynb 2
@dataclasses.dataclass
class Chapter:
    start_time: int
    end_time: int
    title: str
    description: str

@dataclasses.dataclass
class VideoMetadata:
    id: str
    title: str
    alt_title: str
    description: str
    uploader: str
    timestamp: int
    upload_date: str
    release_date: str
    view_count: int
    concurrent_view_count: int
    like_count: int
    dislike_count: int
    comment_count: int
    duration: int
    chapters: List[Chapter]
    subtitles: Dict[str, str]
    fps:int
    resolution:str
    
    
def download_video_and_extract_info(url, output_filename, download=True, verborse=False):
    # Use youtube_dl to download the video and extract the metadata
    ydl_opts = {
        'outtmpl': output_filename,
        'http-chunk-size': 10485760,
        'external_downloader': 'aria2c',
        'external_downloader_args': [
            '--max-connection-per-server=8',
            '--split=8',
            '--continue',
            '--auto-file-renaming=false',
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=download)

    return info


def parse_video_metadata(info: dict):
    chapters = []
    try:
        for chapter in info.get('chapters', []):
            chapters.append(Chapter(
                start_time=chapter['start_time'],
                end_time=chapter['end_time'],
                title=chapter['title'],
                description=chapter['description'],
            ))
    except:
        pass
    v = VideoMetadata(
        id=info.get('id', 'N/A'),
        title=info.get('title', 'N/A'),
        alt_title=info.get('alt_title', 'N/A'),
        description=info.get('description', 'N/A'),
        uploader=info.get('uploader', 'N/A'),
        timestamp=info.get('timestamp', -1),
        upload_date=info.get('upload_date', 'N/A'),
        release_date=info.get('release_date', 'N/A'),
        view_count=info.get('view_count', -1),
        concurrent_view_count=info.get('concurrent_view_count', -1),
        like_count=info.get('like_count', -1),
        dislike_count=info.get('dislike_count', -1),
        comment_count=info.get('comment_count', -1),
        duration=info.get('duration', -1),
        chapters=[],
        subtitles=info.get('subtitles', {}),
        fps=info.get('fps', -1),
        resolution=info.get('resolution', 'N/A'),
    )
    return v
