#!/usr/bin/env python3
# encoding: utf-8
"""
bn2problog.py

CONVERSION CODE TAKEN FROM https://github.com/jordn/ProbLog

Created by Wannes Meert on 06-03-2017.
Copyright (c) 2016 KU Leuven. All rights reserved.
"""
from __future__ import print_function

import sys
import os
import argparse
import itertools
import logging
import abc

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from problog.pgm.cpd import PGM

logger = logging.getLogger('be.kuleuven.cs.dtai.problog.bn2problog')


class BNParser:
    def __init__(self, filename):
        """BNParser abstract base class."""
        self.fn = filename
        self.pgm = PGM()

        self.force_bool = False
        self.detect_bool = True
        self.drop_zero = False
        self.use_neglit = False

    @abc.abstractmethod
    def parse(self):
        pass

    def run(self):
        pgm = self.parse()
        return pgm.to_problog(drop_zero=self.drop_zero, use_neglit=self.use_neglit)


def main(filename):
    logger.addHandler(logging.StreamHandler(sys.stdout))

    parser = None
    input_format = None
    # try to infer input_format
    _, ext = os.path.splitext(filename)
    if ext in ['.uai']:
        input_format = 'uai'
    elif ext in ['.net']:
        input_format = 'hugin'
    elif ext in ['.xdsl']:
        input_format = 'smile'
    elif ext in ['.xml']:
        input_format = 'xmlbif'

    if input_format is None:
        logger.error('No supported file format detected for bayesian network (.uai, .net, .xdsl, .xml).')
        sys.exit(1)

    if input_format in ['uai', 'uai08']:
        from .uai2problog import UAIParser
        parser = UAIParser(filename)
    elif input_format in ['hugin', 'net']:
        from .hugin2problog import HuginParser
        parser = HuginParser(filename)
    elif input_format in ['smile', 'xdsl']:
        from .smile2problog import SmileParser
        parser = SmileParser(filename)
    elif input_format in ['xml', 'xmlbif']:
        from .xmlbif2problog import XMLBIFParser
        parser = XMLBIFParser(filename)
    else:
        logger.error("Unknown input format: {}".format(input_format))
        sys.exit(1)

    if parser:
        return parser.run()
