import argparse


class CliParser:
	def __init__(self, parser: argparse.ArgumentParser) -> None:
		super().__init__()

		parser.add_argument('--config_file', default='config.ini')
		parser.add_argument('--input_format', choices=['double_colon', 'google_play_json'])
		parser.add_argument('--reset', action='store_true', default=False)
		parser.add_argument('input_file', nargs='?')

		self._parser = parser

	def parse(self, *args) -> argparse.Namespace:
		if len(args) > 0:
			values = self._parser.parse_args(args)
		else:
			values = self._parser.parse_args()

		if (values.input_file is None or values.input_format is None) and values.reset is False:
			self._parser.error('Need either input (both file and --input_format) or --reset')
		return values
