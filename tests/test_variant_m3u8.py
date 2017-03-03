# coding: utf-8
# Copyright 2014 Globo.com Player authors. All rights reserved.
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.

import m3u8, playlists


def test_create_a_variant_m3u8_with_two_playlists():
    variant_m3u8 = m3u8.M3U8()

    subtitles = m3u8.Media(uri='english_sub.m3u8',
                           type='SUBTITLES',
                           group_id='subs',
                           language='en',
                           name='English',
                           default='YES',
                           autoselect='YES',
                           forced='NO',
                           characteristics=None)
    variant_m3u8.add_media(subtitles)

    low_playlist = m3u8.Playlist('http://example.com/low.m3u8',
                                 stream_info={'bandwidth': 1280000,
                                              'program_id': 1,
                                              'subtitles': 'subs'},
                                 media=[subtitles],
                                 base_uri=None)
    high_playlist = m3u8.Playlist('http://example.com/high.m3u8',
                                  stream_info={'bandwidth': 3000000,
                                               'program_id': 1,
                                               'subtitles': 'subs'},
                                  media=[subtitles],
                                  base_uri=None)

    variant_m3u8.add_playlist(low_playlist)
    variant_m3u8.add_playlist(high_playlist)

    expected_content = """\
#EXTM3U
#EXT-X-MEDIA:URI="english_sub.m3u8",TYPE=SUBTITLES,GROUP-ID="subs",LANGUAGE="en",NAME="English",DEFAULT=YES,AUTOSELECT=YES,FORCED=NO
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1280000,SUBTITLES="subs"
http://example.com/low.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3000000,SUBTITLES="subs"
http://example.com/high.m3u8
"""
    assert expected_content == variant_m3u8.dumps()


def test_create_a_variant_m3u8_with_two_playlists_and_two_iframe_playlists():
    variant_m3u8 = m3u8.M3U8()

    subtitles = m3u8.Media(uri='english_sub.m3u8',
                           type='SUBTITLES',
                           group_id='subs',
                           language='en',
                           name='English',
                           default='YES',
                           autoselect='YES',
                           forced='NO',
                           characteristics=None)
    variant_m3u8.add_media(subtitles)

    low_playlist = m3u8.Playlist(
        uri='video-800k.m3u8',
        stream_info={'bandwidth': 800000,
                     'program_id': 1,
                     'resolution': '624x352',
                     'codecs': 'avc1.4d001f, mp4a.40.5',
                     'subtitles': 'subs'},
        media=[subtitles],
        base_uri='http://example.com/'
    )
    high_playlist = m3u8.Playlist(
        uri='video-1200k.m3u8',
        stream_info={'bandwidth': 1200000,
                     'program_id': 1,
                     'codecs': 'avc1.4d001f, mp4a.40.5',
                     'subtitles': 'subs'},
        media=[subtitles],
        base_uri='http://example.com/'
    )
    low_iframe_playlist = m3u8.IFramePlaylist(
        uri='video-800k-iframes.m3u8',
        iframe_stream_info={'bandwidth': 151288,
                            'program_id': 1,
                            'resolution': '624x352',
                            'codecs': 'avc1.4d001f'},
        base_uri='http://example.com/'
    )
    high_iframe_playlist = m3u8.IFramePlaylist(
        uri='video-1200k-iframes.m3u8',
        iframe_stream_info={'bandwidth': 193350,
                            'codecs': 'avc1.4d001f'},
        base_uri='http://example.com/'
    )

    variant_m3u8.add_playlist(low_playlist)
    variant_m3u8.add_playlist(high_playlist)
    variant_m3u8.add_iframe_playlist(low_iframe_playlist)
    variant_m3u8.add_iframe_playlist(high_iframe_playlist)

    expected_content = """\
#EXTM3U
#EXT-X-MEDIA:URI="english_sub.m3u8",TYPE=SUBTITLES,GROUP-ID="subs",\
LANGUAGE="en",NAME="English",DEFAULT=YES,AUTOSELECT=YES,FORCED=NO
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=800000,RESOLUTION=624x352,\
CODECS="avc1.4d001f, mp4a.40.5",SUBTITLES="subs"
video-800k.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1200000,\
CODECS="avc1.4d001f, mp4a.40.5",SUBTITLES="subs"
video-1200k.m3u8
#EXT-X-I-FRAME-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=151288,RESOLUTION=624x352,\
CODECS="avc1.4d001f",URI="video-800k-iframes.m3u8"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=193350,\
CODECS="avc1.4d001f",URI="video-1200k-iframes.m3u8"
"""
    assert expected_content == variant_m3u8.dumps()


def test_variant_playlist_with_average_bandwidth():
    variant_m3u8 = m3u8.M3U8()

    low_playlist = m3u8.Playlist(
        'http://example.com/low.m3u8',
        stream_info={'bandwidth': 1280000,
                     'average_bandwidth': 1257891,
                     'program_id': 1,
                     'subtitles': 'subs'},
        media=[],
        base_uri=None
    )
    high_playlist = m3u8.Playlist(
        'http://example.com/high.m3u8',
        stream_info={'bandwidth': 3000000,
                     'average_bandwidth': 2857123,
                     'program_id': 1,
                     'subtitles': 'subs'},
        media=[],
        base_uri=None
    )

    variant_m3u8.add_playlist(low_playlist)
    variant_m3u8.add_playlist(high_playlist)

    expected_content = """\
#EXTM3U
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1280000,AVERAGE-BANDWIDTH=1257891
http://example.com/low.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3000000,AVERAGE-BANDWIDTH=2857123
http://example.com/high.m3u8
"""
    assert expected_content == variant_m3u8.dumps()


def test_remove_playlist_from_variant_playlist():
    variant_m3u8 = m3u8.M3U8()
    low_playlist = m3u8.Playlist(
        'http://example.com/low.m3u8',
        stream_info={'bandwidth': 1280000,
                     'average_bandwidth': 1257891,
                     'program_id': 1,
                     'subtitles': 'subs'},
        media=[],
        base_uri=None
    )
    variant_m3u8.add_playlist(low_playlist)

    variant_m3u8.remove_playlist(low_playlist)

    assert len(variant_m3u8.playlists) == 0


def test_remove_unregistered_playlist_does_not_raise_error():
    variant_m3u8 = m3u8.M3U8()
    low_playlist = m3u8.Playlist(
        'http://example.com/low.m3u8',
        stream_info={'bandwidth': 1280000,
                     'average_bandwidth': 1257891,
                     'program_id': 1,
                     'subtitles': 'subs'},
        media=[],
        base_uri=None
    )

    variant_m3u8.remove_playlist(low_playlist)

    assert len(variant_m3u8.playlists) == 0


def test_remove_ifram_playlist_from_variant_playlist():
    variant_m3u8 = m3u8.M3U8()
    high_iframe_playlist = m3u8.IFramePlaylist(
        uri='video-1200k-iframes.m3u8',
        iframe_stream_info={'bandwidth': 193350,
                            'codecs': 'avc1.4d001f'},
        base_uri='http://example.com/'
    )
    variant_m3u8.add_iframe_playlist(high_iframe_playlist)

    variant_m3u8.remove_iframe_playlist(high_iframe_playlist)

    assert len(variant_m3u8.iframe_playlists) == 0


def test_removing_unregistered_ifram_playlist_from_variant_playlist():
    variant_m3u8 = m3u8.M3U8()
    high_iframe_playlist = m3u8.IFramePlaylist(
        uri='video-1200k-iframes.m3u8',
        iframe_stream_info={'bandwidth': 193350,
                            'codecs': 'avc1.4d001f'},
        base_uri='http://example.com/'
    )

    variant_m3u8.remove_iframe_playlist(high_iframe_playlist)

    assert len(variant_m3u8.iframe_playlists) == 0


def test_playlist_stores_1st_of_2_equivalent_media_items():
    variant_m3u8 = m3u8.M3U8()
    default_subs = m3u8.Media(
        group_id='subs',
        type='SUBTITLES',
        name='English',
        uri='english_sub.m3u8',
        language='en',
        default='YES',
        autoselect='YES',
        forced='NO'
    )
    non_default_subs = m3u8.Media(
        group_id='subs',
        type='SUBTITLES',
        name='English',
        uri='english_sub.m3u8',
        language='en',
        default='NO',
        autoselect='NO',
        forced='NO'
    )
    variant_m3u8.add_media(default_subs)

    variant_m3u8.add_media(non_default_subs)

    assert len(variant_m3u8.media) == 1
    collected_subs = variant_m3u8.media.pop()
    assert collected_subs.default == collected_subs.autoselect == 'YES'


def test_playlist_stores_2nd_of_2_equivalent_media_items_when_specified():
    variant_m3u8 = m3u8.M3U8()
    default_subs = m3u8.Media(
        group_id='subs',
        type='SUBTITLES',
        name='English',
        uri='english_sub.m3u8',
        language='en',
        default='YES',
        autoselect='YES',
        forced='NO'
    )
    non_default_subs = m3u8.Media(
        group_id='subs',
        type='SUBTITLES',
        name='English',
        uri='english_sub.m3u8',
        language='en',
        default='NO',
        autoselect='NO',
        forced='NO'
    )
    variant_m3u8.add_media(default_subs)

    variant_m3u8.add_media(non_default_subs, replace=True)

    assert len(variant_m3u8.media) == 1
    collected_subs = variant_m3u8.media.pop()
    assert collected_subs.default == collected_subs.autoselect == 'NO'


def test_remove_media_from_playlist():
    variant_m3u8 = m3u8.M3U8()
    subs_1 = m3u8.Media(
        group_id='subs',
        type='SUBTITLES',
        name='English',
        uri='english_sub.m3u8',
        language='en',
        default='YES',
        autoselect='YES',
        forced='NO'
    )
    subs_2 = m3u8.Media(
        group_id='subs',
        type='SUBTITLES',
        name='English',
        uri='english_sub.m3u8',
        language='en',
        default='NO',
        autoselect='NO',
        forced='NO'
    )
    variant_m3u8.add_media(subs_1)

    variant_m3u8.remove_media(subs_2)

    assert len(variant_m3u8.media) == 0


def test_removing_unregistered_media_does_not_raise_error():
    variant_m3u8 = m3u8.M3U8()
    subs = m3u8.Media(
        group_id='subs',
        type='SUBTITLES',
        name='English',
        uri='english_sub.m3u8',
        language='en',
        default='YES',
        autoselect='YES',
        forced='NO'
    )

    variant_m3u8.remove_media(subs)

    assert len(variant_m3u8.media) == 0


def test_add_segment_to_playlist():
    variant_m3u8 = m3u8.M3U8()
    seg = m3u8.Segment('smth.ts', 'http://example.com/')

    variant_m3u8.add_segment(seg)

    assert len(variant_m3u8.segments) == 1


def test_removing_segment_from_playlist():
    variant_m3u8 = m3u8.M3U8()
    seg = m3u8.Segment('smth.ts', 'http://example.com/')
    variant_m3u8.add_segment(seg)

    variant_m3u8.remove_segment(seg)

    assert len(variant_m3u8.segments) == 0


def test_removing_unregistered_segment_from_playlist():
    variant_m3u8 = m3u8.M3U8()
    seg = m3u8.Segment('smth.ts', 'http://example.com/')

    variant_m3u8.remove_segment(seg)

    assert len(variant_m3u8.segments) == 0


def test_variant_playlist_with_multiple_media():
    variant_m3u8 = m3u8.loads(playlists.MULTI_MEDIA_PLAYLIST)
    assert variant_m3u8.dumps() == playlists.MULTI_MEDIA_PLAYLIST
