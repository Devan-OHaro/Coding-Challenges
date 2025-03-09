import unittest
import os
import importlib.util

def load_tests(loader, tests, pattern):
    """Discover and load all test cases in the repository."""
    test_suite = unittest.TestSuite()
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.relpath(module_path, test_dir))[0].replace(os.sep, ".")
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
                        test_suite.addTest(loader.loadTestsFromTestCase(obj))
    
    return test_suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(load_tests(unittest.TestLoader(), [], None))

