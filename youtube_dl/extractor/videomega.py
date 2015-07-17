# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..compat import compat_urllib_request


class VideoMegaIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?videomega\.tv/(?:(?:view|iframe|cdn)\.php)?\?ref=(?P<id>[A-Za-z0-9]+)'
    _TESTS = [{
        'url': 'http://videomega.tv/cdn.php?ref=AOSQBJYKIDDIKYJBQSOA',
        'md5': 'cc1920a58add3f05c6a93285b84fb3aa',
        'info_dict': {
            'id': 'AOSQBJYKIDDIKYJBQSOA',
            'ext': 'mp4',
            'title': '1254207',
            'thumbnail': 're:^https?://.*\.jpg$',
        }
    }, {
        'url': 'http://videomega.tv/cdn.php?ref=AOSQBJYKIDDIKYJBQSOA&width=1070&height=600',
        'only_matching': True,
    }, {
        'url': 'http://videomega.tv/view.php?ref=090051111052065112106089103052052103089106112065052111051090',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        iframe_url = 'http://videomega.tv/cdn.php?ref=%s' % video_id
        req = compat_urllib_request.Request(iframe_url)
        req.add_header('Referer', url)
        req.add_header('Cookie', 'noadvtday=0')
        webpage = self._download_webpage(req, video_id)

        title = self._html_search_regex(
            r'<title>(.+?)</title>', webpage, 'title')
        title = re.sub(
            r'(?:^[Vv]ideo[Mm]ega\.tv\s-\s*|\s*-\svideomega\.tv$)', '', title)
        thumbnail = self._search_regex(
            r'<video[^>]+?poster="([^"]+)"', webpage, 'thumbnail', fatal=False)
        video_url = self._search_regex(
            r'<source[^>]+?src="([^"]+)"', webpage, 'video URL')

        return {
            'id': video_id,
            'title': title,
            'url': video_url,
            'thumbnail': thumbnail,
            'http_headers': {
                'Referer': iframe_url,
            },
        }
