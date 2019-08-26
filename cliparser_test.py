import unittest
from argparse import ArgumentParser
from typing import Text, NoReturn

from cliparser import CliParser


class TestArgumentParserError(Exception):
	pass


class TestArgumentParser(ArgumentParser):
	def error(self, message: Text) -> NoReturn:
		"""
		Override to prevent exiting the test runner, which argparse does when met with an error.
		"""
		raise TestArgumentParserError(message)


class CliParserArgs(unittest.TestCase):
	def setUp(self) -> None:
		self.parser = CliParser(TestArgumentParser())
		self.base_args = ['--input_format', 'double_colon', 'file']

	def test_default_config_file(self):
		actual = self.parser.parse(*self.base_args)
		self.assertEqual(actual.config_file, 'config.ini')

	def test_valid_ratings_input_format_parses(self):
		actual = self.parser.parse('--input_format', 'double_colon', 'file')
		self.assertEqual(actual.input_format, 'double_colon')

	def test_invalid_ratings_input_format_raises_error(self):
		with self.assertRaises(TestArgumentParserError):
			self.parser.parse('--input_format', 'not_a_real_parser', 'file')

	def test_no_ratings_input_format_raises_error(self):
		with self.assertRaises(TestArgumentParserError):
			self.parser.parse('file')


if __name__ == '__main__':
	unittest.main()