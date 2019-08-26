import json
from typing import List

from ratingsparser import RatingsParser
from track import Track


class GooglePlayJsonRatingsParser(RatingsParser):
	def __init__(self, filename) -> None:
		self._filename = filename

	def tracks(self) -> List[Track]:
		with open(self._filename, 'r') as file:
			entries = json.load(file)

		return [self.convert_to_track(entry) for entry in entries if self.has_rating(entry)]


	@staticmethod
	def has_rating(entry) -> bool:
		return 'rating' in entry and entry['rating'] != '0'

	@staticmethod
	def convert_to_track(entry) -> Track:
		# Tracks without a disc number are always numbered 1 in Plex
		track_number = 'trackNumber' in entry and entry['trackNumber'] or 1
		disc_number = 'discNumber' in entry and entry['discNumber'] or 1

		try:
			return Track(
				title=entry['title'],
				artist=entry['artist'],
				album=entry['album'],
				track_number=track_number,
				disc_number=disc_number,
				rating=float(entry['rating']) * 2,
			)
		except:
			raise Exception(entry)
