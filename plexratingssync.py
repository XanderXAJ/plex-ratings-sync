#!/usr/bin/env python
from argparse import ArgumentParser
from configparser import ConfigParser

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


@retry(tries=5)
def match_track(library, track):
	albums = library.searchAlbums(title=track.album)
	if len(albums) == 0:
		print('No matches found for album:', track.album)
	for album in albums:
		print('Album:', album.title)
		for candidate in album.tracks():
			print_indent(1, candidate.title, candidate.originalTitle, candidate.parentIndex, candidate.index)

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


@retry(tries=5)
def update_rating(track, rating):
	track.edit(**{'userRating.value': rating})


def main():
	args = CliParser(ArgumentParser()).parse()

	config = read_config(args.config_file)

	plex = PlexServer(config['server']['baseurl'], config['server']['token'])
	music = plex.library.section('Music')

	ratings_parser = select_ratings_parser(args.input_format, args.input_file)
	tracks_to_rate = ratings_parser.tracks()
	print('Parsed', len(tracks_to_rate), 'tracks with ratings')

	for track in tracks_to_rate:
		print(track)

		track_match = match_track(music, track)

		if track_match:
			print('Track matched, updating rating')
			rating_before = track_match.userRating
			rating_after = track.rating

			if rating_before == rating_after:
				print('Ratings match, skipping')
			else:
				update_rating(track_match, rating_after)
				print('Track rating updated from', rating_before, 'to', rating_after)


if __name__ == '__main__':
	main()
