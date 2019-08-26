import json
import unittest
from unittest import TestCase

from googleplayjsonratingsparser import GooglePlayJsonRatingsParser
from track import Track


class TestGooglePlayJsonRatingsParser(TestCase):
	def test_convert_complete_track(self):
		raw_input = """{"kind": "sj#track", "id": "00000000-0000-0000-0000-000000000000", "clientId": 
		"0000000000000000000000", "creationTimestamp": "1505179322773668", "lastModifiedTimestamp": 
		"1505199279130770", "recentTimestamp": "1505179322772000", "deleted": false, "title": "Fallin' Device", 
		"artist": "Hideyuki Eto", "composer": "Hideyuki Eto", "album": "Armored Core Last Raven", "albumArtist": 
		"Various", "year": 2005, "trackNumber": 19, "genre": "Game Soundtrack", "durationMillis": "190850", 
		"playCount": 0, "totalTrackCount": 26, "discNumber": 1, "totalDiscCount": 1, "rating": "3", "estimatedSize": 
		"7636379", "lastRatingChangeTimestamp": "1505199279111000"}"""
		parsed_input = json.loads(raw_input)

		actual = GooglePlayJsonRatingsParser.convert_to_track(parsed_input)

		expected = Track(
			title="Fallin' Device",
			artist="Hideyuki Eto",
			album="Armored Core Last Raven",
			track_number=19,
			disc_number=1,
			rating=6.0,
		)

		self.assertEqual(expected, actual)

	def test_convert_no_disc_number(self):
		raw_input = """{"kind": "sj#track", "id": "d8ce237c-749b-3ca7-b222-7a38a4364c45", "clientId": 
		"kh4/mECegQFnFFk7Yi1iLQ", "creationTimestamp": "1505260764322008", "lastModifiedTimestamp": 
		"1507802467339967", "recentTimestamp": "1507802467041000", "deleted": false, "title": "AL1V3", "artist": 
		"Daiki Kasho", "album": "Gran Turismo 6", "albumArtist": "Various", "year": 2013, "trackNumber": 74, 
		"genre": "Game Soundtrack", "durationMillis": "236856", "playCount": 1, "totalTrackCount": 103, "rating": "4", 
		"estimatedSize": "9476652"}"""
		parsed_input = json.loads(raw_input)

		actual = GooglePlayJsonRatingsParser.convert_to_track(parsed_input)

		expected = Track(
			title="AL1V3",
			artist="Daiki Kasho",
			album="Gran Turismo 6",
			track_number=74,
			# Tracks without a disc number are always numbered 1 in Plex
			disc_number=1,
			rating=8.0,
		)

		self.assertEqual(expected, actual)

	def test_convert_no_track_number(self):
		raw_input = """{"kind": "sj#track", "id": "d32028d0-74b5-3228-98e9-41e50765b611", "clientId": 
		"+Rbt+BpsUts90NdUTygBUw", "creationTimestamp": "1505502981397316", "lastModifiedTimestamp": 
		"1510876787051272", "recentTimestamp": "1505502981395000", "deleted": false, "title": 
		"Rebel Yell (Recorded In Berlin 29/02/2000)", "artist": "HIM", "album": "Unplugged And More", "albumArtist": 
		"HIM", "year": 2004, 
		"genre": "Rock", "durationMillis": "313469", "playCount": 0, "discNumber": 1, "totalDiscCount": 1, 
		"rating": "1", "estimatedSize": "7525948", "lastRatingChangeTimestamp": "1510876787045000"}"""
		parsed_input = json.loads(raw_input)

		actual = GooglePlayJsonRatingsParser.convert_to_track(parsed_input)

		expected = Track(
			title="Rebel Yell (Recorded In Berlin 29/02/2000)",
			artist="HIM",
			album="Unplugged And More",
			# Tracks without a track number are always numbered 1 in Plex
			track_number=1,
			disc_number=1,
			rating=2.0,
		)

		self.assertEqual(expected, actual)

	def test_no_rating_returns_false(self):
		raw_input = """{"kind": "sj#track", "id": "16f132db-e2ea-3b41-a3b9-4cf0ebd2772d", "clientId": 
		"9zV3Bs2pWDeZlQ0cegcc2g==Tdif4hlebxujefkxwniz7h3t2ga", "creationTimestamp": "1418769326434384", 
		"lastModifiedTimestamp": "1449564745518747", "recentTimestamp": "1449522929056000", "deleted": false, 
		"title": "It Came Upon a Midnight Clear (Remastered)", "artist": "Mario Lanza;Paul Baron", "composer": 
		"Richard Storrs Willis", "album": "Play Classical: Christmas Favourites", "albumArtist": "Various", 
		"year": 2014, "trackNumber": 4, "genre": "Classical", "durationMillis": "169324", "playCount": 1, 
		"totalTrackCount": 14, "discNumber": 1, "totalDiscCount": 1, "estimatedSize": "6775145", "trackType": "4", 
		"storeId": "Tdif4hlebxujefkxwniz7h3t2ga", "albumId": "Bkasv5ngb43eiq7wpu4awuv7yzu", "artistId": [
		"Aa2jat3iasyfwdif5bmj7ah5h7i"], "nid": "Tdif4hlebxujefkxwniz7h3t2ga", "explicitType": "2"}"""
		parsed_input = json.loads(raw_input)

		actual = GooglePlayJsonRatingsParser.has_rating(parsed_input)

		self.assertEqual(False, actual)

	def test_zero_rating_returns_false(self):
		raw_input = """{"kind": "sj#track", "id": "2e996a4e-715d-3155-9a96-ce6d53213541", "clientId": 
		"jCGMSZp+mQRZ7vNLXtZXww", "creationTimestamp": "1505355416721061", "lastModifiedTimestamp": 
		"1505664343177743", "recentTimestamp": "1505355416719000", "deleted": false, "title": "Maiya Theme", 
		"artist": "Shoji Meguro", "composer": "Kenichi Tsuchiya", "album": "Persona 3 fes", "albumArtist": "Various", 
		"year": 2007, "trackNumber": 9, "genre": "Game Soundtrack", "durationMillis": "173165", "playCount": 2, 
		"totalTrackCount": 17, "discNumber": 1, "totalDiscCount": 1, "rating": "0", "estimatedSize": "6929343"}"""
		parsed_input = json.loads(raw_input)

		actual = GooglePlayJsonRatingsParser.has_rating(parsed_input)

		self.assertEqual(False, actual)

	def test_non_zero_rating_returns_true(self):
		raw_input = """{"kind": "sj#track", "id": "2626fc6d-edbd-30be-8432-9e2ef48ade5b", "clientId": 
		"PqVKTWO1RI7QZC+YLdGhhw", "creationTimestamp": "1505358284810833", "lastModifiedTimestamp": 
		"1510877239780201", "recentTimestamp": "1505358284809000", "deleted": false, "title": 
		"\\"IDOLA\\" Have the Immortal Feather", "artist": "Hideaki Kobayashi", "composer": "Hideaki Kobayashi", 
		"album": "Phantasy Star Online Songs of Ragol Odyssey ~Soundtrack Episode 1 & 2~", "albumArtist": "Various", 
		"trackNumber": 14, "genre": "Game Soundtrack", "durationMillis": "266527", "playCount": 2, 
		"totalTrackCount": 16, "discNumber": 2, "totalDiscCount": 2, "rating": "5", "estimatedSize": "10663885", 
		"lastRatingChangeTimestamp": "1510877239668000"}"""
		parsed_input = json.loads(raw_input)

		actual = GooglePlayJsonRatingsParser.has_rating(parsed_input)

		self.assertEqual(True, actual)


if __name__ == '__main__':
	unittest.main()
