#!/usr/bin/env python
from configparser import ConfigParser
from ratingsparser import RatingsParser
from plexapi.server import PlexServer
from retry import retry

config = ConfigParser()
config.read('config.ini')

plex = PlexServer(config['server']['baseurl'], config['server']['token'])
music = plex.library.section('Music')

for track in music.searchTracks(title='Reach for the Summit'):
	track.edit(**{'userRating.value': 8.0})
	print(track.userRating)

ratings = RatingsParser('ratings.txt')
tracks_to_rate = ratings.tracks()
print('Parsed', len(tracks_to_rate), 'tracks with ratings')

# foobar2000 ratings are out of 5, Plex ratings are out of 10, so multiply by 2 to get from fb2k to Plex ratings
tracks_to_rate = [{**track, 'rating': track['rating'] * 2} for track in tracks_to_rate]

def print_indent(indent_level, *args):
	indent = ' ' * (indent_level * 4 - 1)
	print(indent, *args)

@retry(tries=5)
def match_track(library, track):
	albums = music.searchAlbums(title=track['album'])
	if len(albums) == 0:
		print('No matches found for album:', track['album'])
	for album in albums:
		print('Album:', album.title)
		for candidate in album.tracks():
			print_indent(1, candidate.title, candidate.originalTitle, candidate.parentIndex, candidate.index)
			# print_indent(1, track['title'], track['artist'], track['discNumber'], track['trackNumber'])

			parentIndex = candidate.parentIndex
			if parentIndex != None:
				parentIndex = int(parentIndex)

			index = candidate.index
			if index != None:
				index = int(index)

			match_title = candidate.title == track['title']
			match_artist = candidate.originalTitle == track['artist']
			match_disc_number = parentIndex == track['discNumber']
			match_track_number = index == track['trackNumber']

			match_title and print_indent(2, 'Track matches title')
			match_artist and print_indent(2, 'Track matches artist')
			match_disc_number and print_indent(2, 'Track matches disc number')
			match_track_number and print_indent(2, 'Track matches track number')

			if match_title and match_artist and match_disc_number and match_track_number:
				return candidate


@retry(tries=5)
def update_rating(track, rating):
	track.edit(**{'userRating.value': rating})


for track in tracks_to_rate:
	print(track)

	track_match = match_track(music, track)

	if track_match:
		print('Track matched, updating rating')
		rating_before = track_match.userRating
		rating_after = track['rating']

		if rating_before == rating_after:
			print('Ratings match, skipping')
		else:
			update_rating(track_match, rating_after)
			print('Track rating updated from', rating_before, 'to', rating_after)
