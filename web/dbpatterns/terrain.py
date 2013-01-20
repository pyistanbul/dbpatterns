import os, sys

def setup_test_directory():
    sys.path.append(os.path.join(os.path.dirname(__file__), "../../tests"))
    __import__("steps")

setup_test_directory()