import unittest
import parse

class TestParseFunctions(unittest.TestCase):
    def test_empty(self):
        self.assertEqual({}, parse.parse_functions(''))

    def test_simple(self):
        code = '''def generate_list(size):
    return random.sample(range(1, 5_000_000), size)'''
        out = {'generate_list': {'args': ['size'], 'code': code}}
        self.assertEqual(out, parse.parse_functions(code))

    def test_one_line(self):
        code = '''def hello_world(): return "hello"'''
        out = {'hello_world': {'args': [], 'code': code}}
        self.assertEqual(out, parse.parse_functions(code))

    def test_multiple_indents(self):
        code = '''def hello_world():
    for _ in range(1):
        print("hello")'''
        out = {'hello_world': {'args': [], 'code': code}}
        self.assertEqual(out, parse.parse_functions(code))

    def test_multiple_funcs(self):
        code1 = '''def quicksort(A):
    return quicksort_helper(A, 0, len(A) - 1)\n'''
        code2 = '''def quicksort2(A):
    return quicksort_helper(A, 0, len(A) - 1)'''
        code = code1 + code2
        out = {'quicksort': {'args': ['A'], 'code': code1},
               'quicksort2': {'args': ['A'], 'code': code2}}
        self.assertEqual(out, parse.parse_functions(code))


    def test_args(self):
        code = '''def partition(arr, low, high):
    i = low - 1'''
        out = {'partition': {'args': ['arr', 'low', 'high'], 'code': code}}
        self.assertEqual(out, parse.parse_functions(code))

class TestStandardizeInput(unittest.TestCase):
    def test_empty(self):
        self.assertEqual("", parse.standardize_input(''))

    def test_simple(self):
        self.assertEqual("test", parse.standardize_input('test'))

    def test_multiline_no_empty(self):
        self.assertEqual("test\ntest", parse.standardize_input('test\ntest'))

    def test_multiline_empty(self):
        self.assertEqual("test\ntest", parse.standardize_input('test\n\n\ntest'))

    def test_multiline_space_indent(self):
        self.assertEqual("test\n    test", parse.standardize_input('test\n    test'))

    def test_multiline_tab_indent(self):
        self.assertEqual("test\n    test", parse.standardize_input('test\n\ttest'))

    def test_multiline_complex_indent(self):
        string = "test\n    test\n        test\n            test"
        self.assertEqual(string, parse.standardize_input('test\n\ttest\n\t\ttest\n\t\t\ttest'))

    def test_multiline_mixed_indent(self):
        instr = "test\n\n\n\ttest\n    test\n\ntest\n\t\ttest"
        expected = "test\n    test\n    test\ntest\n        test"
        self.assertEqual(expected, parse.standardize_input(instr))

class TestParseImports(unittest.TestCase):
    def test_empty(self):
        self.assertEqual({}, parse.parse_imports(''))

    def test_simple(self):
        self.assertEqual({}, parse.parse_imports('test'))

    def test_simple_import(self):
        self.assertEqual({'time': {'import': 'import time', 'module': 'time'},
                          'requests': {'import': 'import requests', 'module': 'requests'}},
                         parse.parse_imports('import requests\nimport time'))

    def test_function_import(self):
        self.assertEqual({'date': {'import': 'from time import date', 'module': 'time'},
                          'requests': {'import': 'import requests', 'module': 'requests'}},
                         parse.parse_imports('import requests\nfrom time import date'))

if __name__ == '__main__':
    unittest.main()

