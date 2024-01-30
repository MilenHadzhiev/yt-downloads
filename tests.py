from validations import validate_url


def test_url_validator_recognize_correct_youtube_urls():
    urls = [
        'http://youtube.com/watch?v=iwGFalTRHDA',
        'http://www.youtube.com/watch?v=iwGFalTRHDA&feature=related',
        'https://www.youtube.com/channel/UCDZkgJZDyUnqwB070OyP72g',
        'https://youtube.com/channel/UCDZkgJZDyUnqwB070OyP72g',
        'https://youtube.com/iwGFalTRHDA',
        'http://youtu.be/n17B_uFF4cA',
        'youtube.com/iwGFalTRHDA',
        'youtube.com/n17B_uFF4cA',
        'http://www.youtube.com/embed/watch?feature=player_embedded&v=r5nB9u4jjy4',
        'http://www.youtube.com/watch?v=t-ZRX8984sc',
        'http://youtu.be/t-ZRX8984sc'
        ]

    for url in urls:
        assert validate_url(url)


def test_url_validator_incorrect_urls():
    urls = [
        'aaaaaaaaaaa',
        'https://',
        '.com',
        'http:/a.a',
        'http://a',
        'http://',
        'asasa',
        'youtube',
        'http//youtube'
    ]
    for url in urls:
        assert not validate_url(url)


def test_url_validator_recognizes_non_youtube_urls():
    urls = [
        'https://pytube.io/en/latest/index.html',
        'getbootstrap.com',
        'https://pythonbasics.org/',
        'https://www.regexpal.com/94360',
        'https://github.com/',
        'https://www.linkedin.com/in/milen-hadzhiev/',
        'https://www.vbox7.com/play:e9a80d2d40',
        'https://raft.github.io/raft.pdf',
        'http://learnyouahaskell.com/chapters' # not secure
    ]
    for url in urls:
        assert not validate_url(url)


if __name__ == '__main__':
    test_url_validator_recognizes_non_youtube_urls()
    test_url_validator_incorrect_urls()
    test_url_validator_recognize_correct_youtube_urls()
