from typing import Optional, Any

from flask import flash

from pytube import YouTube


def download(url: str, output_path: Optional[str]=None) -> None:
    try:
        YouTube(url, on_complete_callback=completed_download).streams.get_highest_resolution().download(output_path)
    except Exception as e:  # pylint: disable=broad-exception-caught
        flash(f'Problem occured while downloading: {e}', category='error')


def completed_download(stream: Optional[Any] = None, file_path: Optional[str] = None) -> None:  # pylint: disable=unused-argument
    flash('Your download was completed', category='info')
