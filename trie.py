import os
from parser_html import Parser

class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.children = {}
        self.counter = 0
        self.index_list = []



class Trie(object):

    def __init__(self):
        self.root = TrieNode("")

    def add(self, word, ind):
        node = self.root

        for char in word:
            char = char.lower()
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        node.is_end = True
        node.counter += 1
        node.index_list.append(ind)


    def has_word(self, word):
        exists = True
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                exists = False
                break
        if exists == True and node.is_end == True:
            return True, node.counter
        else:
            return False, 0

    def get_index(self, word):
        exists = True
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                exists = False
                break
        if exists == True and node.is_end == True:
            return node.index_list
        else:
            return None