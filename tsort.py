# CPE 202 lab 8 
# Name: Ashley Sutter
# Student ID: 011278952
# Date (last modified): 3/11/2019
#
# Lab 8
# Section 5
# Purpose of Lab: Implement Tsort algorithm
# additional comments

from sys import argv
from stack_array import *

def tsort(vertices):
    '''
    * Performs a topological sort of the specified directed acyclic graph.  The
    * graph is given as a list of vertices where each pair of vertices represents
    * an edge in the graph.  The resulting string return value will be formatted
    * identically to the Unix utility {@code tsort}.  That is, one vertex per
    * line in topologically sorted order.
    *
    * Raises a ValueError if:
    *   - vertices is emtpy with the message "input contains no edges"
    *   - vertices has an odd number of vertices (incomplete pair) with the
    *     message "input contains an odd number of tokens"
    *   - the graph contains a cycle (isn't acyclic) with the message 
    *     "input contains a cycle"'''
    if len(vertices) == 0:
        raise ValueError("input contains no edges")
    elif len(vertices) % 2 != 0:
        raise ValueError("input contains an odd number of tokens")
     # check errors
    stack = Stack(len(vertices))
    output = []
    # { 5: { in-degree: 0, a-list: [11] } }
    (adjacency_dictionary, ordered_list) = get_adjacency_dictionary_and_ordered_list(vertices)

    for vertex in ordered_list:
        if adjacency_dictionary[vertex]["in-degree"] == 0:
            stack.push(vertex) # vertex = 5
    while stack.size() != 0: # or !isEmpty()
        vertex = stack.pop()
        output.append(vertex)
        for vertex2 in adjacency_dictionary[vertex]["a-list"]:
            adjacency_dictionary[vertex2]["in-degree"] -= 1
            if adjacency_dictionary[vertex2]["in-degree"] == 0:
                stack.push(vertex2)
    if len(ordered_list) != len(output):
        raise ValueError('input contains a cycle')
    return '\n'.join(output) # output each result on a newline


#list of vertices → dictionary of vertexes and orderedlist
def get_adjacency_dictionary_and_ordered_list(vertices):
    adjacency_dictionary = {}
    ordered_list = []
    for i in range(0, len(vertices), 2):
        source = vertices[i]
        destination = vertices[i + 1]
        if source not in adjacency_dictionary:
            adjacency_dictionary[source] = {"in-degree": 0, "a-list": [destination]}
            ordered_list.append(source)
        else:
            adjacency_dictionary[source]["a-list"].append(destination)
        if destination not in adjacency_dictionary:
            adjacency_dictionary[destination] = {"in-degree": 1, "a-list": []}
            ordered_list.append(destination)
        else:
            adjacency_dictionary[destination]["in-degree"] += 1
    return (adjacency_dictionary, ordered_list)

def main(argv = argv):
    '''Entry point for the tsort utility allowing the user to specify
       a file containing the edge of the DAG'''
    if len(argv) != 2:
        print("Usage: python3 tsort.py <filename>")
        exit()
    try:
        f = open(argv[1], 'r')
    except FileNotFoundError as e:
        print(argv[1], 'could not be found or opened')
        exit()
    
    vertices = []
    for line in f:
        vertices += line.split()
       
    try:
        result = tsort(vertices)
        print(result)
    except Exception as e:
        print(e)
 
if __name__ == '__main__': 
    main()
