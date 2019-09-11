import mixtape
import json

my_mixtape = mixtape.MixtapeUpdate('mixtape.json')

def test_classcreation():
    assert type(my_mixtape) == mixtape.MixtapeUpdate
    assert len(my_mixtape.users) > 0
    assert len(my_mixtape.playlists) > 0
    assert len(my_mixtape.songs) > 0


def test_to_json():
    """
    additional tests:
        * ensure that all newly created records have the same structure
    :return:
    """
    input = my_mixtape.load_file('mixtape.json')
    output = my_mixtape.to_json()
    assert input == output


def test_add_song_all_exist():
    """
    additional tests:
        * missing playlist id
        * no duplicate song ids (assumption)
    :return:
    """
    valid_songs = list(my_mixtape.songs)[:4]
    playlist_id = list(my_mixtape.playlists)[:1][0]
    my_mixtape.add_song_to_playlist(valid_songs, playlist_id)
    assert len(set(valid_songs) -
               set(my_mixtape.playlists[playlist_id]['song_ids'])) == 0


def test_add_playlist():
    """
    additional tests:
        * user does not exist
        * no valid songs
    :return:
    """
    valid_songs = list(my_mixtape.songs)[:4]
    user_id = list(my_mixtape.users)[:1][0]
    prior = list(my_mixtape.playlists)
    new_id = my_mixtape.add_playlist(valid_songs, user_id)
    assert new_id not in prior
    assert type(new_id) == str
    assert my_mixtape.playlists[new_id]['song_ids'] == valid_songs
    assert my_mixtape.playlists[new_id]['user_id'] == user_id


def test_remove_playlist():
    """
    additional tests:
        * playlist does not exist
    :return:
    """
    prior = list(my_mixtape.playlists)
    playlist_id = list(my_mixtape.playlists)[:1][0]
    my_mixtape.remove_playlist(playlist_id)
    assert playlist_id not in my_mixtape.playlists

