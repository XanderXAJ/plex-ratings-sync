from dataclasses import dataclass


@dataclass
class Track:
	title: str
	artist: str
	album: str
	track_number: int
	disc_number: int
	rating: float
