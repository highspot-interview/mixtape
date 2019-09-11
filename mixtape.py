import json
import sys

class MixtapeUpdate:

    def __init__(self, filename):
        self.mixtape = self.load_file(filename)
        self.users = self.return_users()
        self.playlists = self.return_playlists()
        self.songs = self.return_songs()

    def to_json(self):
        output = dict()
        output['users'] = [{'id': k,'name': v} for k, v in self.users.items()]
        output['playlists'] = [{'id': k,
                                'user_id': v['user_id'],
                                'song_ids': v['song_ids']}
                               for k, v in self.playlists.items()]
        output['songs'] = [{'id': k,
                            'artist': v['artist'],
                            'title': v['title']} for k, v in self.songs.items()]
        return output

    def load_file(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def apply_changes(self, change_filename):
        """

        :param change_filename: filename of changes
        :return:
        """
        changes = self.load_file(change_filename)['changes']
        change_map = {
            'add_song': self.add_song_to_playlist,
            'add_playlist': self.add_playlist,
            'remove_playlist': self.remove_playlist
        }
        for c in changes:
            action, data = c['action'], c['data']
            change_map[action](**data)

    def output(self, output_filename):
        """

        :param output_filename: filename of output
        :return:
        """
        self.save_file(output_filename, self.to_json())

    def save_file(self, filename, data):
        """

        :param filename: string; should end with .json
        :param data: dictionary
        :return:
        """
        with open(filename, 'w') as out:
            json.dump(data, out)

    def return_users(self):
        """

        :return: dictionary; {user_id : user_name}
        """
        return {u['id']: u['name'] for u in self.mixtape['users']}

    def return_playlists(self):
        """

        :return: dictionary; {playlist_id : {user_id, song_ids}}
        """
        return {u['id']: {'user_id': u['user_id'],
                          'song_ids': u['song_ids']} for u in self.mixtape['playlists']}

    def return_songs(self):
        """

        :return: songs; {song_id: {artist, title}}
        """
        return {u['id']: {'artist': u['artist'],
                          'title': u['title']} for u in self.mixtape['songs']}

    def add_song_to_playlist(self, song_ids, playlist_id):
        """
        Add an existing song to an existing playlist.

        :return:
        """
        for s in song_ids:
            if s in self.songs and s not in self.playlists[playlist_id]['song_ids']:
                self.playlists[playlist_id]['song_ids'].append(s)

    def add_playlist(self, song_ids, user_id):
        """
        Add a new playlist for an existing user; the playlist should contain at least one existing song.

        :return:
        """
        validated_songs = []

        for s in song_ids:
            if s in self.songs:
                validated_songs.append(s)

        new_id = str(max([int(p) for p in self.playlists])+1)
        if user_id in self.users and validated_songs:
            self.playlists[new_id] = {
                "user_id": user_id,
                "song_ids": validated_songs
            }
        return new_id

    def remove_playlist(self, playlist_id):
        """
        Remove an existing playlist.

        :return:
        """
        if playlist_id in self.playlists:
            del self.playlists[playlist_id]


if __name__ == '__main__':
    input_file, change_file, output_file = sys.argv[1:4]
    mx = MixtapeUpdate(input_file)
    mx.apply_changes(change_file)
    mx.output(output_file)
