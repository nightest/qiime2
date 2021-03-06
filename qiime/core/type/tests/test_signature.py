# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import unittest
import collections

from qiime.core.type import Visualization
from qiime.core.type.signature import (
    PipelineSignature, MethodSignature, VisualizerSignature)
from qiime.plugin import Int
from qiime.core.testing.type import IntSequence1


class TestPipelineSignature(unittest.TestCase):

    def test_constructor(self):
        signature = PipelineSignature(
            inputs={'input1': (IntSequence1, list),
                    'input2': (IntSequence1, list)},
            parameters={'param1': (Int, int),
                        'param2': (Int, int)},
            defaults={'param1': 42},
            outputs=collections.OrderedDict([
                ('output1', (IntSequence1, list)),
                ('output2', (IntSequence1, list))]))

        self.assertEqual(signature.inputs,
                         {'input1': (IntSequence1, list),
                          'input2': (IntSequence1, list)})
        self.assertEqual(signature.parameters,
                         {'param1': (Int, int), 'param2': (Int, int)})
        self.assertEqual(signature.defaults,
                         {'param1': 42})
        self.assertEqual(
            signature.outputs,
            collections.OrderedDict([
                ('output1', (IntSequence1, list)),
                ('output2', (IntSequence1, list))]))

    def test_solve_output(self):
        signature = PipelineSignature(
            inputs={'input1': (IntSequence1, list),
                    'input2': (IntSequence1, list)},
            parameters={'param1': (Int, int),
                        'param2': (Int, int)},
            defaults={'param1': 42},
            outputs=collections.OrderedDict([
                ('output1', (IntSequence1, list)),
                ('output2', (IntSequence1, list))])
            )
        self.assertEqual(
            signature.solve_output(**{}),
            collections.OrderedDict([
                ('output1', (IntSequence1, list)),
                ('output2', (IntSequence1, list))]))


class TestMethodSignature(unittest.TestCase):
    def test_from_function(self):
        def method(input3: list, input2: dict, in1: set, param1: str,
                   p2: int=2) -> tuple:
            pass

        inputs = {
            'in1': IntSequence1,
            'input2': IntSequence1,
            'input3': IntSequence1
        }
        exp_inputs = collections.OrderedDict([
            ('input3', (IntSequence1, list)),
            ('input2', (IntSequence1, dict)),
            ('in1', (IntSequence1, set))
        ])

        parameters = {
            'param1': Int,
            'p2': Int
        }
        exp_parameters = collections.OrderedDict([
            ('param1', (Int, str)),
            ('p2', (Int, int))
        ])

        outputs = [
            ('out', IntSequence1)
        ]
        exp_outputs = collections.OrderedDict([
            ('out', (IntSequence1, tuple))
        ])

        exp_defaults = {
            'p2': 2
        }

        sig = MethodSignature.from_function(
            method, inputs, parameters, outputs)

        self.assertIsInstance(sig.inputs, collections.OrderedDict)
        self.assertEqual(sig.inputs, exp_inputs)

        self.assertIsInstance(sig.parameters, collections.OrderedDict)
        self.assertEqual(sig.parameters, exp_parameters)

        self.assertIsInstance(sig.outputs, collections.OrderedDict)
        self.assertEqual(sig.outputs, exp_outputs)

        self.assertEqual(sig.defaults, exp_defaults)


class TestVisualizerSignature(unittest.TestCase):
    def test_from_function(self):
        def visualizer(output_dir, input3: list, input2: dict, in1: set,
                       param1: str, p2: int=2) -> None:
            pass

        inputs = {
            'in1': IntSequence1,
            'input2': IntSequence1,
            'input3': IntSequence1
        }
        exp_inputs = collections.OrderedDict([
            ('input3', (IntSequence1, list)),
            ('input2', (IntSequence1, dict)),
            ('in1', (IntSequence1, set))
        ])

        parameters = {
            'param1': Int,
            'p2': Int
        }
        exp_parameters = collections.OrderedDict([
            ('param1', (Int, str)),
            ('p2', (Int, int))
        ])

        exp_outputs = collections.OrderedDict([
            ('visualization', (Visualization, None))
        ])

        exp_defaults = {
            'p2': 2
        }

        sig = VisualizerSignature.from_function(
            visualizer, inputs, parameters)

        self.assertIsInstance(sig.inputs, collections.OrderedDict)
        self.assertEqual(sig.inputs, exp_inputs)

        self.assertIsInstance(sig.parameters, collections.OrderedDict)
        self.assertEqual(sig.parameters, exp_parameters)

        self.assertIsInstance(sig.outputs, collections.OrderedDict)
        self.assertEqual(sig.outputs, exp_outputs)

        self.assertEqual(sig.defaults, exp_defaults)


if __name__ == "__main__":
    unittest.main()
