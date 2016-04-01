"""
Module with tests for the execute preprocessor.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import copy
import glob
import io
import os
import re

import nbformat

from nbconvert.preprocessors.tests.base import PreprocessorTestsBase
from nbconvert.preprocessors.execute import ExecutePreprocessor, CellExecutionError

from nbconvert.filters import strip_ansi
from nose.tools import assert_raises
from testpath import modified_env

addr_pat = re.compile(r'0x[0-9a-f]{7,9}')

class TestExecute(PreprocessorTestsBase):
    """Contains test functions for execute.py"""

    @staticmethod
    def normalize_output(output):
        """
        Normalizes outputs for comparison.
        """
        output = dict(output)
        if 'metadata' in output:
            del output['metadata']
        if 'text' in output:
            output['text'] = re.sub(addr_pat, '<HEXADDR>', output['text'])
        if 'text/plain' in output.get('data', {}):
            output['data']['text/plain'] = \
                re.sub(addr_pat, '<HEXADDR>', output['data']['text/plain'])
        if 'traceback' in output:
            tb = []
            for line in output['traceback']:
                tb.append(strip_ansi(line))
            output['traceback'] = tb
            
        return output


    def assert_notebooks_equal(self, expected, actual):
        expected_cells = expected['cells']
        actual_cells = actual['cells']
        self.assertEqual(len(expected_cells), len(actual_cells))

        for expected_cell, actual_cell in zip(expected_cells, actual_cells):
            expected_outputs = expected_cell.get('outputs', [])
            actual_outputs = actual_cell.get('outputs', [])
            normalized_expected_outputs = list(map(self.normalize_output, expected_outputs))
            normalized_actual_outputs = list(map(self.normalize_output, actual_outputs))
            self.assertEqual(normalized_expected_outputs, normalized_actual_outputs)

            expected_execution_count = expected_cell.get('execution_count', None)
            actual_execution_count = actual_cell.get('execution_count', None)
            self.assertEqual(expected_execution_count, actual_execution_count)


    def build_preprocessor(self, opts):
        """Make an instance of a preprocessor"""
        preprocessor = ExecutePreprocessor()
        preprocessor.log.setLevel(20)
        preprocessor.enabled = True
        for opt in opts:
            setattr(preprocessor, opt, opts[opt])
        return preprocessor


    def run_notebook(self, filename, opts, resources):
        """Loads and runs a notebook, returning both the version prior to 
        running it and the version after running it.
        """
        with io.open(filename) as f:
            input_nb = nbformat.read(f, 4)

        preprocessor = self.build_preprocessor(opts)
        cleaned_input_nb = copy.deepcopy(input_nb)
        for cell in cleaned_input_nb.cells:
            if 'execution_count' in cell:
                del cell['execution_count']
            cell['outputs'] = []

        # Override terminal size to standardise traceback format
        with modified_env({'COLUMNS': '80', 'LINES': '24'}):
            output_nb, _ = preprocessor(cleaned_input_nb, resources)

        return input_nb, output_nb

    def test_run_notebooks(self):
        """Runs a series of test notebooks and compares them to their actual output"""
        current_dir = os.path.dirname(__file__)
        input_files = glob.glob(os.path.join(current_dir, '../notebooks', '*.ipynb'))
        for filename in input_files:
            opts = dict(allow_errors=True)
            res = self.build_resources()
            res['metadata']['path'] = os.path.dirname(filename)
            input_nb, output_nb = self.run_notebook(filename, opts, res)
            self.assert_notebooks_equal(input_nb, output_nb)

if __name__ == '__main__':

    TestExecute()

