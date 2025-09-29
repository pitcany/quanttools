"""
Conftest to add project src directory to Python path for pytest.
"""
import os
import sys

# ensure the src directory is on sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
