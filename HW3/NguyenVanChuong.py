# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 18:00:51 2017

@author: Nguyen Van Chuong 20161199

"""

import sys

RED = 'R'
BLACK = 'B'
NIL = 'N'


class NODE:
    def __init__(self, key, color, parent, right=None, left=None):
        self.key = key
        self.color = color
        self.parent = parent
        self.right = right
        self.left = left

    # Representatio of a Node to appear, including key and color
    def __repr__(self):
        return '{val} {color}'.format(val=self.key, color=self.color)

    def __iter__(self):
        if self.left.color != NIL:
            yield from self.left.__iter__()

        yield self.key

        if self.right.color != NIL:
            yield from self.right.__iter__()

    def __eq__(self, other):
        if self.parent is None or other.parent is None:
            same_parents = self.parent is None and other.parent is None
        else:
            same_parents = self.parent.key == other.parent.key and self.parent.color == other.parent.color
        return self.key == other.key and self.color == other.color and same_parents

        if self.color == NIL and self.color == other.color:
            return True

    def children_available(self) -> bool:
        """ Returns a boolean indicating if the NODE has children """
        return bool(self.Number_Of_Children())

    def Number_Of_Children(self) -> int:
        """ Returns the number of NOT NIL children the NODE has """
        if self.color == NIL:
            return 0
        return sum([int(self.left.color != NIL), int(self.right.color != NIL)])


class AugmentedRedBlackTree:
    # Initialization a Node with No color, No key value, and no parent
    Leaf = NODE(key=None, color=NIL, parent=None)

    def __init__(self):
        self.count = 0
        self.root = None
        self.ROTATIONS = {
            # Guide to rotation when we delete function
            'L': self._right_rotation,
            'R': self._left_rotation
        }

    def __iter__(self):
        if not self.root:
            return list()
        yield from self.root.__iter__()

    def TREE_INSERT(self, key):
        if not self.root:
            self.root = NODE(key, color=BLACK, parent=None, right=self.Leaf, left=self.Leaf)
            self.count += 1
            return
        parent, Dir_NODE = self._Look_For_Position_Of_PARENT(key)
        if Dir_NODE is None:
            return
        new_NODE = NODE(key=key, color=RED, parent=parent, right=self.Leaf, left=self.Leaf)
        if Dir_NODE == 'R':
            parent.right = new_NODE
        else:
            parent.left = new_NODE

        self._Balance_RBTree(new_NODE)
        self.count += 1

    def _Look_For_Position_Of_PARENT(self, key):
        def loop_find(parent):
            if key == parent.key:
                print('It is parent')
                return None, None
            elif key < parent.key:
                if parent.left.color == NIL:
                    return parent, 'L'
                return loop_find(parent.left)
            elif key > parent.key:
                if parent.right.color == NIL:
                    return parent, 'R'
                return loop_find(parent.right)

        return loop_find(self.root)

    def TREE_DELETE(self, key):
        NODE_to_Delete = self.Look_For_NODE(key)

        if NODE_to_Delete is None:  # NODE is not in the tree
            return
        if NODE_to_Delete.Number_Of_Children() == 2:
            TREE_Successor = self._Look_For_Successor(NODE_to_Delete)
            NODE_to_Delete.key = TREE_Successor.key
            NODE_to_Delete = TREE_Successor

        self._Delete_Node_has_0_or_1_child(NODE_to_Delete)
        self.count -= 1

    def _Look_For_Successor(self, NODE):
        right_NODE = NODE.right
        left_NODE = right_NODE.left
        if left_NODE == self.Leaf:
            return right_NODE
        while left_NODE.left != self.Leaf:
            left_NODE = left_NODE.left
        return left_NODE

    def TREE_PRINT(self, NODE):
        if NODE.key is None:
            return
        print(NODE.key, NODE.color),
        self.TREE_PRINT(NODE.left)
        self.TREE_PRINT(NODE.right)

    def TREE_REPORT(self, NODE, a, b):
        global ct
        ct = 0
        if NODE.key is None:
            return
        if a < NODE.key:
            self.TREE_REPORT(NODE.left, a, b)
        if a <= NODE.key and b >= NODE.key:
            print(NODE.key),
        if b > NODE.key:
            self.TREE_REPORT(NODE.right, a, b)

    def TREE_COUNT(self, NODE, a, b):
        global ct
        if NODE.key is None:
            return 0
        if NODE.key is not None:
            if a < NODE.key:
                self.TREE_COUNT(NODE.left, a, b)
            if a <= NODE.key and b >= NODE.key:
                ct += 1
            if b > NODE.key:
                self.TREE_COUNT(NODE.right, a, b)
        return ct

    def _Find_SIBLINGS(self, NODE):
        parent = NODE.parent
        if NODE.key < parent.key:
            sibling = parent.right
            direction = 'R'
        else:
            sibling = parent.left
            direction = 'L'
        return sibling, direction

    def ceil(self, key) -> int or None:
        
        if self.root is None: return None
        last_found_val = None if self.root.key < key else self.root.key

        def find_ceil(NODE):
            nonlocal last_found_val
            if NODE == self.Leaf:
                return None
            if NODE.key == key:
                last_found_val = NODE.key
                return NODE.key
            elif NODE.key < key:
                return find_ceil(NODE.right)
            else:
                last_found_val = NODE.key

                return find_ceil(NODE.left)
        find_ceil(self.root)
        return last_found_val

    def floor(self, key) -> int or None:

        if self.root is None: return None
        last_found_val = None if self.root.key < key else self.root.key

        def find_floor(NODE):
            nonlocal last_found_val
            if NODE == self.Leaf:
                return None
            if NODE.key == key:
                last_found_val = NODE.key
                return NODE.key
            elif NODE.key < key:
                last_found_val = NODE.key

                return find_floor(NODE.right)
            else:
                return find_floor(NODE.left)

        find_floor(self.root)
        return last_found_val

    def _Delete_Node_has_0_or_1_child(self, NODE):
        left_child = NODE.left
        right_child = NODE.right
        if left_child != self.Leaf:
            child=left_child
        else:
            child=right_child
        if NODE.color == RED:
            if not NODE.children_available():
                self._Delete_leaf(NODE)
            else:
                raise Exception('Invalid')

        if NODE.color == BLACK:
            if right_child.children_available() or left_child.children_available():  # sanity check
                raise Exception('Invalid')
            if child.color == RED:
                NODE.key = child.key
                NODE.left = child.left
                NODE.right = child.right
            else:  
                self.__case_6(NODE)
                self._Delete_leaf(NODE)
        elif NODE == self.root:
            self.root = child
            self.root.parent = None
            self.root.color = BLACK


    def _Delete_leaf(self, leaf):
        if leaf.key < leaf.parent.key:        
            leaf.parent.left = self.Leaf
        else:
            leaf.parent.right = self.Leaf

    def __case_1(self, NODE):
        sibling, direction = self._Find_SIBLINGS(NODE)
        if direction =='L':
            outer_NODE = sibling.left
        else:
            outer_NODE = sibling.right
        def __rotate_case_1(direction):
            parent_color = sibling.parent.color
            self.ROTATIONS[direction](NODE=None, parent=sibling, grandparent=sibling.parent)
            sibling.right.color = BLACK
            sibling.left.color = BLACK
            sibling.color = parent_color

        if outer_NODE.color == RED and sibling.color == BLACK :
            return __rotate_case_1(direction)

        raise Exception('Invalid')

    def __case_2(self, NODE):
        sibling, direction = self._Find_SIBLINGS(NODE)
        if direction == 'L':
            closer_NODE = sibling.right
        else:
            closer_NODE = sibling.left    
        if direction =='R':
            outer_NODE = sibling.right
        else:
            outer_NODE = sibling.left
        if closer_NODE.color == RED and outer_NODE.color != RED and sibling.color == BLACK:
            if direction == 'L':
                self._left_rotation(NODE=None, parent=closer_NODE, grandparent=sibling)
            else:
                self._right_rotation(NODE=None, parent=closer_NODE, grandparent=sibling)
            closer_NODE.color = BLACK
            sibling.color = RED

        self.__case_1(NODE)

    def __case_3(self, NODE):
        parent = NODE.parent
        if parent.color == RED:
            sibling, direction = self._Find_SIBLINGS(NODE)
            if  sibling.left.color != RED and sibling.right.color != RED and sibling.color == BLACK:
                parent.color, sibling.color = sibling.color, parent.color  # switch colors
                return  # Terminating
        self.__case_2(NODE)

    def __case_4(self, NODE):
        parent = NODE.parent
        sibling, _ = self._Find_SIBLINGS(NODE)
        if (sibling.left.color != RED and sibling.right.color != RED and sibling.color == BLACK and parent.color == BLACK):
            sibling.color = RED
            return self.__case_6(parent)
        self.__case_3(NODE)

    def __case_5(self, NODE):
        parent = NODE.parent
        sibling, direction = self._Find_SIBLINGS(NODE)
        if sibling.color == RED and parent.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
            self.ROTATIONS[direction](NODE=None, parent=sibling, grandparent=parent)
            parent.color = RED
            sibling.color = BLACK
            return self.__case_6(NODE)
        self.__case_4(NODE)

    def __case_6(self, NODE):
        if self.root == NODE:
            NODE.color = BLACK
            return
        self.__case_5(NODE)

    def _Balance_RBTree(self, NODE):
        parent = NODE.parent
        key = NODE.key
        if (parent is None
            or parent.parent is None  # parent is the root
            or (NODE.color != RED or parent.color != RED)):  # no need to rebalance
            return
        grandparent = parent.parent
        Dir_NODE = 'L' if parent.key > key else 'R'
        parent_dir = 'L' if grandparent.key > parent.key else 'R'
        uncle = grandparent.right if parent_dir == 'L' else grandparent.left
        general_direction = Dir_NODE + parent_dir

        if uncle == self.Leaf or uncle.color == BLACK:
            if general_direction == 'RR':
                self._left_rotation(NODE, parent, grandparent, to_Change_COLOR=True)
            elif general_direction == 'RL':
                self._left_rotation(NODE=None, parent=NODE, grandparent=parent)
                self._right_rotation(NODE=parent, parent=NODE, grandparent=grandparent, to_Change_COLOR=True)
            elif general_direction == 'LL':
                self._right_rotation(NODE, parent, grandparent, to_Change_COLOR=True)
            elif general_direction == 'LR':
                self._right_rotation(NODE=None, parent=NODE, grandparent=parent)
                self._left_rotation(NODE=parent, parent=NODE, grandparent=grandparent, to_Change_COLOR=True)

            else:
                raise Exception("{}!".format(general_direction))
        else:  
            self._Change_COLOR(grandparent)

    def __update_parent(self, NODE, parent_old_child, new_parent):
        NODE.parent = new_parent
        if new_parent:
            if new_parent.key > parent_old_child.key:
                new_parent.left = NODE
            else:
                new_parent.right = NODE
        else:
            self.root = NODE

    def _right_rotation(self, NODE, parent, grandparent, to_Change_COLOR=False):
        grand_grandparent = grandparent.parent
        self.__update_parent(NODE=parent, parent_old_child=grandparent, new_parent=grand_grandparent)

        old_right = parent.right
        parent.right = grandparent
        grandparent.parent = parent

        grandparent.left = old_right  # save the old right keys
        old_right.parent = grandparent

        if to_Change_COLOR:
            parent.color = BLACK
            NODE.color = RED
            grandparent.color = RED

    def _left_rotation(self, NODE, parent, grandparent, to_Change_COLOR=False):
        grand_grandparent = grandparent.parent
        self.__update_parent(NODE=parent, parent_old_child=grandparent, new_parent=grand_grandparent)

        old_left = parent.left
        parent.left = grandparent
        grandparent.parent = parent

        grandparent.right = old_left  # save the old left keys
        old_left.parent = grandparent

        if to_Change_COLOR:
            parent.color = BLACK
            NODE.color = RED
            grandparent.color = RED

    def _Change_COLOR(self, grandparent):
        grandparent.right.color = BLACK
        grandparent.left.color = BLACK
        if grandparent != self.root:
            grandparent.color = RED
        self._Balance_RBTree(grandparent)

    def Look_For_NODE(self, key):
        def loop_find(root):
            if root is None or root == self.Leaf:
                return None
            if key < root.key:
                return loop_find(root.left)
            elif key > root.key:
                return loop_find(root.right)
            else:
                return root

        found_NODE = loop_find(self.root)
        return found_NODE


if __name__ == '__main__':
    S = AugmentedRedBlackTree()
    filepath = 'Input.txt'
    with open(filepath) as fp:
        cnt = 1
        for line in fp:
            line = fp.readline()
            print("Line {}: {}".format(cnt, line))
            tokens = line.split()
            if tokens[0] == 'I':
                S.TREE_INSERT(tokens[1])
            if tokens[0] == 'P':
                S.TREE_PRINT(S.root)
            if tokens[0] == 'R':
                S.TREE_REPORT(S.root, tokens[1], tokens[2])
            if tokens[0] == 'C':
                S.TREE_COUNT(S.root, tokens[1], tokens[2])
            if tokens[0] == 'D':
                S.TREE_DELETE(tokens[1])
            if tokens[0] == 'E':
                print("End of file")
                break
            cnt += 1




