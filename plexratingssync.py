#!/usr/bin/env python
from argparse import ArgumentParser
from configparser import ConfigParser
import logging

from plexapi.server import PlexServer
from retry import retry

from cliparser import CliParser
from doublecolonratingsparser import DoubleColonRatingsParser
from googleplayjsonratingsparser import GooglePlayJsonRatingsParser
from ratingsparser import RatingsParser


def read_config(filename):
	config = ConfigParser()
	config.read(filename)
	return config


def select_ratings_parser(type: str, filename: str) -> RatingsParser:
	if type == 'double_colon':
		return DoubleColonRatingsParser(filename)
	if type == 'google_play_json':
		return GooglePlayJsonRatingsParser(filename)


def print_indent(indent_level, *args):
	indent = ' ' * (indent_level * 4 - 1)
	print(indent, *args)


def reset_all_ratings(library):
	all_tracks = library.searchTracks()
	for track in all_tracks:
		update_rating(track, 0.0)


@retry(tries=5)
def match_track(albums, track):
	found_album = track.album in albums
	if not found_album:
		print('No matches found for album:', track.album)
	else:
		album = albums[track.album]
		print('Album:', album.title)
		for candidate in album.tracks():
			print_indent(1, str_plex_track(candidate))

			parent_index = candidate.parentIndex
			if parent_index is not None:
				parent_index = int(parent_index)

			index = candidate.index
			if index is not None:
				index = int(index)

			match_title = candidate.title == track.title
			match_artist = candidate.originalTitle == track.artist
			match_disc_number = parent_index == track.disc_number
			match_track_number = index == track.track_number

			match_title and print_indent(2, 'Track matches title')
			match_artist and print_indent(2, 'Track matches artist')
			match_disc_number and print_indent(2, 'Track matches disc number')
			match_track_number and print_indent(2, 'Track matches track number')

			if match_title and match_artist and match_disc_number and match_track_number:
				return candidate
		return None


def update_rating(track, target_rating):
	current_rating = track.userRating

	if current_rating == target_rating:
		print('Ratings match, skipping:', track)
	else:
		update_rating_commit(track, target_rating)
		print('Track rating updated from', current_rating,
		      'to', track.userRating, ':', track)


def str_plex_track(track):
	fields = ['title', 'originalTitle', 'parentRatingKey', 'ratingKey', 'userRating']
	obj = {field: getattr(track, field) for field in fields}
	return str(obj)


@retry(tries=5)
def update_rating_commit(track, rating):
	track.edit(**{'userRating.value': rating})


def main():
	logging.basicConfig()
	args = CliParser(ArgumentParser()).parse()

	config = read_config(args.config_file)

	plex = PlexServer(config['server']['baseurl'], config['server']['token'])
	music_library = plex.library.section('Music')

	if args.reset:
		print('Resetting ratings for all tracks')
		reset_all_ratings(music_library)

	if args.input_file is not None and args.input_format is not None:
		albums = {album.title : album for album in music_library.albums()}

		ratings_parser = select_ratings_parser(args.input_format, args.input_file)
		tracks_to_rate = ratings_parser.tracks()
		print('Parsed', len(tracks_to_rate), 'tracks with ratings')

		for track in tracks_to_rate:
			print(track)

			track_match = match_track(albums, track)

			if track_match:
				print('Track matched, updating rating:', str_plex_track(track_match))
				update_rating(track_match, track.rating)
			else:
				print('No match for track:', track)


if __name__ == '__main__':
	main()
