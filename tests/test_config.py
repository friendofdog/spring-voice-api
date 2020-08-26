import argparse
import unittest
from bin.config import create_config_filepath
from unittest import mock


class TestSpringapiConfig(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_create_config_filepath_raises_FileNotFoundError(self, mock_args):
        file = 'abc'
        mock_args.return_value = argparse.Namespace(
            config_filepath=file)

        with self.assertRaises(FileNotFoundError) as context:
            create_config_filepath()

        self.assertEqual(f"[Errno 2] No such file or directory: '{file}'",
                         str(context.exception))

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_create_config_filepath_reads_file(self, mock_args):
        file = 'sample-config.json'
        schema = 'abc'
        mock_args.return_value = argparse.Namespace(
            config_filepath=file, protocol=schema)

        uri = create_config_filepath()
        self.assertIn(schema, uri)
