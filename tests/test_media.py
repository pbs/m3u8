import pytest

from m3u8.model import Media, InvalidMedia


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
        media = Media(type=value, group_id='abc', name='Spanish doubled',
                      instream_id='')
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
        Media(type='VIDEO', group_id='abc', name='Spanish doubled', force='')
    with pytest.raises(InvalidMedia):
        Media(type='VIDEO', group_id='abc', name='Spanish doubled',
              autoselect='n')


def test_invalid_values_for_boolean_fields_raises_errors():
    media = Media(type='VIDEO', group_id='abc', name='Spanish doubled')
    with pytest.raises(InvalidMedia):
        media.default = ''
    with pytest.raises(InvalidMedia):
        media.force = 'y'
    with pytest.raises(InvalidMedia):
        media.autoselect = 'n'
