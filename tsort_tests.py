import unittest
from tsort import *
import imp
from tsort import main as tsort_main

class TestTsort(unittest.TestCase):
        
    def test_01(self):
        input = ['101', '102', '102', '103', '103', '315', '225', '315', '103', '357', '315', '357', '141', '102', '102', '225']
        expect = "141\n101\n102\n225\n103\n315\n357"
        actual = tsort(input)
        self.assertEqual(actual.strip(), expect)        

    def test_02(self):
        input = ['blue', 'black', 'red', 'blue', 'red', 'green', 'green', 'blue', 'green', 'purple', 'purple', 'blue']
        expect = "red\ngreen\npurple\nblue\nblack"
        actual = tsort(input)
        self.assertEqual(actual.strip(), expect)

    def test_03(self):
        input = ['1', '2', '1', '9', '1', '8', '9', '8', '9', '10', '8', '11', '10', '11', '2', '3', '3', '11', '3', '4', '4', '7', '4', '5', '7', '5', '7', '13', '7', '6', '6', '14', '6', '12']
        expect = "1\n9\n10\n8\n2\n3\n4\n7\n6\n12\n14\n13\n5\n11"
        actual = tsort(input)
        self.assertEqual(actual.strip(), expect)

    def test_04(self):
        input = ['3', '8', '3', '10', '5', '11', '7', '8', '7', '11', '8', '9', '11', '2', '11', '9', '11', '10']
        expect = "7\n5\n11\n2\n3\n10\n8\n9"
        actual = tsort(input)
        self.assertEqual(actual.strip(), expect)

    def test_05(self):
        input = []
        try:
            tsort(input)
        except ValueError as e:
            self.assertEqual(str(e), "input contains no edges")

    def test_06(self):
        input = ['1']
        try:
            tsort(input)
        except ValueError as e:
            self.assertEqual(str(e), "input contains an odd number of tokens")

    def test_get_adjacency_and_order_list_01(self):
        test = ['a', 'b', 'b', 'c']
        (adjacency_list, order_list) = get_adjacency_dictionary_and_ordered_list(test)
        self.assertEqual(adjacency_list['a']['in-degree'], 0) 
        self.assertEqual(adjacency_list['a']['a-list'], ['b'])
        self.assertEqual(adjacency_list['b']['in-degree'], 1) 
        self.assertEqual(adjacency_list['b']['a-list'], ['c'])
        self.assertEqual(adjacency_list['c']['in-degree'], 1)
        self.assertEqual(adjacency_list['c']['a-list'], [])
        self.assertEqual(order_list, ['a', 'b', 'c'])
    
    def test_get_adjacency_and_order_list_02(self):
        test = ['a', 'b', 'c', 'd', 'e', 'f', 'b', 'c', 'd', 'e']
        (adjacency_list, order_list) = get_adjacency_dictionary_and_ordered_list(test)
        self.assertEqual(adjacency_list['a']['in-degree'], 0) 
        self.assertEqual(adjacency_list['a']['a-list'], ['b'])
        self.assertEqual(adjacency_list['d']['in-degree'], 1) 
        self.assertEqual(adjacency_list['d']['a-list'], ['e'])
        self.assertEqual(adjacency_list['f']['in-degree'], 1) 
        self.assertEqual(adjacency_list['f']['a-list'], [])
        self.assertEqual(order_list, ['a', 'b', 'c', 'd', 'e', 'f'])
    
    def test_get_adjacency_and_order_list_03(self):
        test = ['3', '8', '3', '10', '5', '11', '7', '8', '7', '11', '8', '9', '11', '2', '11', '9', '11', '10']
        (adjacency_list, order_list) = get_adjacency_dictionary_and_ordered_list(test)
        self.assertEqual(adjacency_list['3']['in-degree'], 0) 
        self.assertEqual(adjacency_list['3']['a-list'], ['8','10'])
        self.assertEqual(adjacency_list['10']['in-degree'], 2) 
        self.assertEqual(adjacency_list['10']['a-list'], [])
        self.assertEqual(adjacency_list['11']['in-degree'], 2) 
        self.assertEqual(adjacency_list['11']['a-list'], ['2', '9', '10'])
        self.assertEqual(order_list, ['3', '8', '10', '5', '11', '7', '9', '2'])

    def test_my_tsort_01(self):
        test = ['a', 'b', 'b', 'c']
        expected = '\n'.join(['a', 'b', 'c'])
        actual = tsort(test)
        self.assertEqual(actual.strip(), expected)
    
    def test_my_tsort_02(self):
        test = ['a', 'b', 'c', 'd', 'e', 'f', 'b', 'c', 'd', 'e']
        expected = '\n'.join(['a', 'b', 'c', 'd', 'e', 'f'])
        actual = tsort(test)
        self.assertEqual(actual.strip(), expected)

    def test_my_tsort_03(self):
        test = ['3', '8', '3', '10', '5', '11', '7', '8', '7', '11', '8', '9', '11', '2', '11', '9', '11', '10']
        expected = '\n'.join(['7', '5', '11', '2', '3', '10', '8', '9'])
        actual = tsort(test)
        self.assertEqual(actual.strip(), expected)

    # https://docs.python.org/dev/library/unittest.html#unittest.TestCase.assertRaises
    def test_my_tsort_04(self):
        test = []
        with self.assertRaises(ValueError) as context:
            tsort(test)
        self.assertTrue('input contains no edges' in str(context.exception))
    
    def test_my_tsort_05(self):
        test = ['a', 'b', 'c']
        with self.assertRaises(ValueError) as context:
            tsort(test)
        self.assertTrue('input contains an odd number of tokens' in str(context.exception))

    def test_my_tsort_06(self):
        test = ['a', 'b', 'b', 'c', 'c', 'd', 'd', 'b']
        with self.assertRaises(ValueError) as context:
            print(tsort(test))
        self.assertTrue('input contains a cycle' in str(context.exception))
    
    def test_my_tsort_07(self):
        test = ['a', 'b', 'b', 'c', 'c', 'a']
        with self.assertRaises(ValueError) as context:
            tsort(test)
        self.assertTrue('input contains a cycle' in str(context.exception))

    def test_my_tsort_08(self):
        test = ['a', 'b', 'c', 'd', 'e', 'f', 'b', 'c', 'd', 'e', 'e', 'b']
        with self.assertRaises(ValueError) as context:
            tsort(test)
        self.assertTrue('input contains a cycle' in str(context.exception))
    
    def test_my_tsort_10(self):
        test = ['a', 'a']
        with self.assertRaises(ValueError) as context:
            tsort(test)
        self.assertTrue('input contains a cycle' in str(context.exception))

    #main tests
    def test_my_tsort_11(self):
        with self.assertRaises(SystemExit) as context:
            tsort_main(['tsort.py'])

    def test_my_tsort_12(self):
        with self.assertRaises(SystemExit) as context:
            tsort_main(['tsort.py', 'fake_file.txt'])

    def test_my_tsort_13(self):
        tsort_main(['tsort.py', 'test_file.txt'])

    def test_my_tsort_14(self):
        tsort_main(['tsort.py', 'test_file_2.txt'])

    def test_my_tsort_15(self):
        with self.assertRaises(SystemExit) as context:
            runpy = imp.load_source('__main__', './tsort.py')

#stack_array tests
    def test_simple(self):
        stack = Stack(5)
        stack.push(0)
        self.assertFalse(stack.is_empty())
        self.assertFalse(stack.is_full())
        self.assertEqual(stack.size(),1)
        self.assertEqual(stack.pop(),0)

    def test_empty_pop(self):
        stack = Stack(5)
        with self.assertRaises(IndexError):
           stack.pop()

    def test_push_full(self):
        stack = Stack(5)
        stack.push(1)
        stack.push(2)
        stack.push(3)
        stack.push(4)
        stack.push(5)
        with self.assertRaises(IndexError):
           stack.push(2)

    def test_peek(self):
        stack = Stack(5)
        stack.push(5)
        self.assertEqual(stack.peek(), 5)
        stack.pop()
        with self.assertRaises(IndexError):
           stack.peek()
 
if __name__ == "__main__":
    unittest.main()
