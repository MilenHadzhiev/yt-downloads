from flask import flash
from pytube import YouTube
from typing import Optional, Any


def download(
        url: str,
        output_path: Optional[str]=None,
        get_highest_res: Optional[bool] = True) -> None:
    try:
        if get_highest_res:
            YouTube(url, on_complete_callback=completed_download)\
                .streams.get_highest_resolution()\
                .download(output_path)
            pass
    except Exception as e:
        flash(f'Problem occured while downloading: {e}', category='error')


def completed_download(stream: Optional[Any] = None, file_path: Optional[str] = None) -> None:
    flash('Your download was completed', category='info')