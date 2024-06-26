import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from unittest import IsolatedAsyncioTestCase
import argparse

import aiofiles
import main  # assuming 'main' is the name of your module

class TestParseArgs(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(input='input.txt', addresses='addresses.txt', output='output.txt'))
    def test_parse_args(self, mock_parse_args):
        args = main.parse_args()
        self.assertEqual(args.input, 'input.txt')
        self.assertEqual(args.addresses, 'addresses.txt')
        self.assertEqual(args.output, 'output.txt')

class TestReadFile(IsolatedAsyncioTestCase):

    @patch('asyncio.run')
    async def test_read_file(self, test_input_file):
        test_input_file = 'test_input.txt'
        # Call the function under test
        result = await main.read_file(test_input_file)
        # Assert the result
        self.assertEqual(result, ['Line1', 'Line2', 'Line3'])

class TestWriteResult(IsolatedAsyncioTestCase):

    async def test_write_result(self):
        test_output_file = 'test_output.txt'
        output = ("Hello", "World")

        # Call the function under test
        result = await main.write_result(test_output_file, output)
        # Assert the result
        expected_result = f"{output[0]} {output[1]}\n"
        async with aiofiles.open(test_output_file, mode='r') as file:
            lines = await file.readlines()
            for line in lines:
                self.assertEqual(line, expected_result)

if __name__ == '__main__':
    unittest.main()
