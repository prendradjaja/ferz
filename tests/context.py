"""
This file is used to give test files access to source files.

From Kenneth Reitz:
    https://github.com/kennethreitz/samplemod/blob/54e0190dc0d0ba6ee16c5036ba58b93ac25075e4/tests/context.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src
