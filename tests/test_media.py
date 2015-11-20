import pytest

from m3u8.model import Media, InvalidMedia, MediaList


def test_group_id_not_provided_in_init_raises_error():
    with pytest.raises(InvalidMedia):
        Media(type='AUDIO', name='Spanish doubled')


def test_empty_value_for_group_id_raises_error():
    media = Media(group_id='abc', type='AUDIO', name='Spanish doubled')
    with pytest.raises(InvalidMedia):
        media.group_id = None


def test_name_not_provided_in_init_raises_error():
    with pytest.raises(InvalidMedia):
        Media(type='AUDIO', group_id='abc')


def test_empty_value_for_name_raises_error():
    media = Media(group_id='abc', type='AUDIO', name='Spanish doubled')
    with pytest.raises(InvalidMedia):
        media.name = None


def test_type_not_provided_in_init_raises_error():
    with pytest.raises(InvalidMedia):
        Media(group_id='abc', name='Spanish doubled')


def test_invalid_value_for_type_raises_error():
    media = Media(group_id='abc', type='AUDIO', name='Spanish doubled')
    with pytest.raises(InvalidMedia):
        media.type = 'NONEXISTENT'


def test_valid_values_for_type_in_init():
    valid_values = ('AUDIO', 'VIDEO', 'SUBTITLES', 'CLOSED-CAPTIONS')
    for value in valid_values:
        if value == 'CLOSED-CAPTIONS':
            instream_id = 'CC4'
        else:
            instream_id = None
        media = Media(type=value, group_id='abc', name='Spanish doubled',
                      instream_id=instream_id)
        assert media.type == value


def test_valid_values_for_type_in_direct_assignment():
    valid_values = ('AUDIO', 'VIDEO', 'SUBTITLES', 'CLOSED-CAPTIONS')
    media = Media(type='VIDEO', group_id='abc', name='Spanish doubled')
    for value in valid_values:
        media.type = value
        assert media.type == value


def test_invalid_values_for_boolean_fields_in_init_raises_errors():
    with pytest.raises(InvalidMedia):
        Media(type='VIDEO', group_id='abc', name='Spanish doubled',
              default='y')
    with pytest.raises(InvalidMedia):
        Media(type='VIDEO', group_id='abc', name='Spanish doubled', forced='')
    with pytest.raises(InvalidMedia):
        Media(type='VIDEO', group_id='abc', name='Spanish doubled',
              autoselect='n')


def test_invalid_values_for_boolean_fields_raises_errors():
    media = Media(type='VIDEO', group_id='abc', name='Spanish doubled')
    with pytest.raises(InvalidMedia):
        media.default = ''
    with pytest.raises(InvalidMedia):
        media.forced = 'y'
    with pytest.raises(InvalidMedia):
        media.autoselect = 'n'


def test_valid_values_for_instream_id_for_closed_captions_type():
    valid_values = ('CC1', 'CC3', 'SERVICE1', 'SERVICE20', 'SERVICE59',
                    'SERVICE63')
    for value in valid_values:
        media = Media(group_id='abc', type='CLOSED-CAPTIONS',
                      name='Spanish CCs', instream_id=value)
        assert media.instream_id == value


def test_error_raised_when_instream_id_set_for_non_closed_captions_types():
    non_cc_types = ('AUDIO', 'VIDEO', 'SUBTITLES')
    for type_ in non_cc_types:
        with pytest.raises(InvalidMedia):
            Media(group_id='abc', type=type_, name='Spanish CCs',
                  instream_id='CC1')


def test_invalid_instream_id_for_closed_captions_type_raises_error():
    invalid_values = (None, 'CC0', 'CC5', 'SERVICE0', 'SERVICE64')
    for value in invalid_values:
        with pytest.raises(InvalidMedia):
            Media(group_id='abc', type='CLOSED-CAPTIONS', name='Spanish CCs',
                  instream_id=value)


def test_media_instances_equal_on_group_type_name():
    en_sub_1 = Media(group_id='subs', type='SUBTITLES', name='English subs',
                     uri='en_subs.vtt', default='NO')
    en_sub_2 = Media(group_id='subs', type='SUBTITLES', name='English subs',
                     uri='en_subs_2.vtt', default='YES')
    assert en_sub_1 == en_sub_2


def test_equivalent_media_instances_have_the_same_hash():
    en_sub_1 = Media(group_id='subs', type='SUBTITLES', name='English subs',
                     uri='en_subs.vtt', default='NO')
    en_sub_2 = Media(group_id='subs', type='SUBTITLES', name='English subs',
                     uri='en_subs_2.vtt', default='YES')
    assert hash(en_sub_1) == hash(en_sub_2)


def test_media_instances_compared_based_on_group_type_name():
    media1 = Media(group_id='subs', type='SUBTITLES', name='English subs')
    media2 = Media(group_id='audio', type='AUDIO', name='Spanish audio')
    media3 = Media(group_id='subs', type='CLOSED-CAPTIONS',
                   name='Inlayed subs', instream_id='CC1')
    media4 = Media(group_id='subs', type='SUBTITLES', name='Spanish subs')

    assert media2 < media3 < media1 < media4


def test_media_elements_are_unique_based_on_group_type_name():
    en_sub_1 = Media(group_id='subs', type='SUBTITLES', name='English subs',
                     uri='en_subs.vtt')
    en_sub_2 = Media(group_id='subs', type='SUBTITLES', name='English subs',
                     uri='en_subs_2.vtt', default='YES')
    sp_sub = Media(group_id='subs', type='SUBTITLES', name='Spanish subs')
    sp_aud_1 = Media(group_id='aud', type='AUDIO', name='Spanish Audio',
                     language='sp')
    sp_aud_2 = Media(group_id='aud', type='AUDIO', name='Spanish Audio',
                     default='YES')

    media_list = MediaList([en_sub_1, sp_sub, en_sub_2, sp_aud_1, sp_aud_2])

    assert len(media_list) == 3
    media = sorted(media_list)
    assert media[0].language == 'sp' and media[0].default is None
    assert media[1].uri == 'en_subs.vtt' and media[1].default is None
    assert media[2] == sp_sub


def test_equivalent_media_element_not_added_to_list():
    en_sub_1 = Media(group_id='subs', type='SUBTITLES', name='English subs',
                     uri='en_subs.vtt')
    en_sub_2 = Media(group_id='subs', type='SUBTITLES', name='English subs',
                     uri='en_subs_2.vtt', default='YES')
    media_list = MediaList([en_sub_1])

    media_list.add(en_sub_2)

    assert len(media_list) == 1
    en_sub = media_list.pop()
    assert en_sub.uri == 'en_subs.vtt' and en_sub.default is None


def test_equivalent_media_element_added_if_specified():
    en_sub_1 = Media(group_id='subs', type='SUBTITLES', name='English subs',
                     uri='en_subs.vtt')
    en_sub_2 = Media(group_id='subs', type='SUBTITLES', name='English subs',
                     uri='en_subs_2.vtt', default='YES')
    media_list = MediaList([en_sub_1])

    media_list.add(en_sub_2, replace=True)

    assert len(media_list) == 1
    en_sub = media_list.pop()
    assert en_sub.uri == 'en_subs_2.vtt' and en_sub.default == 'YES'


def test_add_unregistered_media_with_replace_flag_set():
    en_sub = Media(group_id='subs', type='SUBTITLES', name='English subs',
                   uri='en_subs.vtt')
    media_list = MediaList()

    media_list.add(en_sub, replace=True)

    assert len(media_list) == 1
