import pytest
from validations import validate_url


@pytest.mark.parametrize('url, should_pass',
                         (
                                 ('https://youtube.com/watch?v=iwGFalTRHDA', True),
                                 ('http://www.youtube.com/watch?v=iwGFalTRHDA&feature=related', True),
                                 ('http://youtu.be/n17B_uFF4cA', True),
                                 ('youtube.com/iwGFalTRHDA', True),
                                 ('aaaaaaaaaaa', False),
                                 ('https://', False),
                                 ('.com', False),
                                 ('http//youtube', False),
                                 ('youtube', False),
                                 ('https://pytube.io/en/latest/index.html', False),
                                 ('https://github.com/', False),
                                 ('https://raft.github.io/raft.pdf', False),
                                 ('http://learnyouahaskell.com/chapters', False),
                         ),
                         ids=(
                                 'Valid secure standard Youtube URL passes validation',
                                 'Valid standard Youtube URL with query data passes validation',
                                 'Valid shorthand Youtube URL passes validation',
                                 'Valid no http/s Youtube URL passes validation',
                                 'Invalid Youtube URL fails validation',
                                 'https only url fails validation',
                                 '.com only url fails validation',
                                 'http//youtube only url fails validation',
                                 'youtube only url fails validation',
                                 'Non-youtube pytube url fails validation',
                                 'Non-youtube github url fails validation',
                                 'Non-youtube raft url fails validation',
                                 'Non-youtube haskell url fails validation',
                         )
                         )
def test_url_validator_recognize_correct_youtube_urls(url: str, should_pass: bool) -> None:
    assert validate_url(url) == should_pass
