import argparse


class CliParser:
	def __init__(self, parser: argparse.ArgumentParser) -> None:
		super().__init__()

		parser.add_argument('--config_file', default='config.ini')
		parser.add_argument('--input_format', choices=['double_colon', 'google_play_json'], required=True)
		parser.add_argument('input_file')

		self._parser = parser

	def parse(self, *args) -> argparse.Namespace:
		if len(args) > 0:
			return self._parser.parse_args(args)
		else:
			return self._parser.parse_args()
