class RatingsParser():
	def __init__(self, filename):
		self._filename = filename

	def filename(self):
		return self._filename

	def tracks(self):
		ratings_file = open(self._filename, mode='r', encoding='utf-8')
		tracks_to_rate = []

		for line in ratings_file:
			# The ratings file is expected to be in the format:
			# title :: artist :: album :: track number :: disc number :: rating

			# Strip any line break from the line
			line = line.rstrip('\n')

			# Get metadata
			title, artist, album, track_number, disc_number, rating = line.split(' :: ')

			if rating == '':
				continue

			if track_number == '':
				track_number = None
			else:
				track_number = int(track_number)

			if disc_number == '':
				disc_number = 1   # Tracks without a disc number are always numbered 1 in Plex
			else:
				disc_number = int(disc_number)

			track = {
				'title': title,
				'artist': artist,
				'album': album,
				'trackNumber': track_number,
				'discNumber': disc_number,
				'rating': float(rating)
			}

			tracks_to_rate.append(track)

		ratings_file.close()
		return tracks_to_rate
