from typing import List

from ratingsparser import RatingsParser
from track import Track

class DoubleColonRatingsParser(RatingsParser):
	"""
	Parses ratings files of the format:
	title :: artist :: album :: track number :: disc number :: rating
	"""
	def __init__(self, filename):
		self._filename = filename

	def filename(self):
		return self._filename

	def tracks(self) -> List[Track]:
		ratings_file = open(self._filename, mode='r', encoding='utf-8')
		tracks_to_rate = []

		for line in ratings_file:

			# Strip any line break from the line
			line = line.rstrip('\n')

			# Get metadata
			title, artist, album, track_number, disc_number, rating = line.split(' :: ')

			if rating == '':
				continue
			else:
				# foobar2000 ratings are out of 5 while Plex ratings are out of 10, so multiply by 2 to get from fb2k to Plex ratings
				rating = float(rating) * 2

			if track_number == '':
				track_number = None
			else:
				track_number = int(track_number)

			if disc_number == '':
				disc_number = 1   # Tracks without a disc number are always numbered 1 in Plex
			else:
				disc_number = int(disc_number)

			track = Track(
				title=title,
				artist=artist,
				album=album,
				track_number=track_number,
				disc_number=disc_number,
				rating=rating
			)

			tracks_to_rate.append(track)

		ratings_file.close()
		return tracks_to_rate
