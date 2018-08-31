# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 18:00:51 2017

@author: Nguyen Van Chuong 20161199

"""

# The possible NODE colors

RED = 'R'
BLACK = 'B'
NIL = 'N'


class NODE:
    def __init__(self, key, color, parent, right=None, left=None):
        self.key = key
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return '{color} {val} NODE'.format(color=self.color, val=self.key)

    def __iter__(self):
        if self.left.color != NIL:
            yield from self.left.__iter__()

        yield self.key

        if self.right.color != NIL:
            yield from self.right.__iter__()

    def __eq__(self, other):
        if self.color == NIL and self.color == other.color:
            return True

        if self.parent is None or other.parent is None:
            parents_are_same = self.parent is None and other.parent is None
        else:
            parents_are_same = self.parent.key == other.parent.key and self.parent.color == other.parent.color
        return self.key == other.key and self.color == other.color and parents_are_same

    def has_children(self) -> bool:
        """ Returns a boolean indicating if the NODE has children """
        return bool(self.get_children_count())

    def get_children_count(self) -> int:
        """ Returns the number of NOT NIL children the NODE has """
        if self.color == NIL:
            return 0
        return sum([int(self.left.color != NIL), int(self.right.color != NIL)])


class AugmentedRedBlackTree:
    # every NODE has null NODEs as children initially, create one such object for easy management
    NIL_LEAF = NODE(key=None, color=NIL, parent=None)

    def __init__(self):
        self.count = 0
        self.root = None
        self.ROTATIONS = {
            # Used for deletion and uses the sibling's relationship with his parent as a guide to the rotation
            'L': self._right_rotation,
            'R': self._left_rotation
        }

    def __iter__(self):
        if not self.root:
            return list()
        yield from self.root.__iter__()

    def Insert(self, key):
        if not self.root:
            self.root = NODE(key, color=BLACK, parent=None, right=self.NIL_LEAF, left=self.NIL_LEAF)
            self.count += 1
            return
        parent, NODE_dir = self._find_parent(key)
        if NODE_dir is None:
            return  # key is in the tree
        new_NODE = NODE(key=key, color=RED, parent=parent, right=self.NIL_LEAF, left=self.NIL_LEAF)
        if NODE_dir == 'L':
            parent.left = new_NODE
        else:
            parent.right = new_NODE

        self._try_rebalance(new_NODE)
        self.count += 1

    def Delete(self, key):
        """
        Try to get a NODE with 0 or 1 children.
        Either the NODE we're given has 0 or 1 children or we get its successor.
        """
        NODE_to_Delete = self.find_NODE(key)
        if NODE_to_Delete is None:  # NODE is not in the tree
            return
        if NODE_to_Delete.get_children_count() == 2:
            # find the in-order successor and replace its key.
            # then, Delete the successor
            successor = self._find_in_order_successor(NODE_to_Delete)
            NODE_to_Delete.key = successor.key  # switch the key
            NODE_to_Delete = successor

        # has 0 or 1 children!
        self._Delete(NODE_to_Delete)
        self.count -= 1

    def Print(self, NODE):
        if NODE.key is None:
            return
        self.Print(NODE.left)
        print(NODE.key, NODE.color),
        self.Print(NODE.right)

    def Report(self, NODE, a, b):
        if NODE.key is None:
            return
        if a < NODE.key:
            self.Report(NODE.left, a, b)
        if a <= NODE.key and b >= NODE.key:
            print(NODE.key),
        if b > NODE.key:
            self.Report(NODE.right, a, b)

    def Count(self, NODE, a, b):
        global ct
        if NODE.key is None:
            return 0
        if NODE.key is not None:
            if a < NODE.key:
                self.Count(NODE.left, a, b)
            if a <= NODE.key and b >= NODE.key:
                ct += 1
            if b > NODE.key:
                self.Count(NODE.right, a, b)
        return ct

    def ResetCount(self):
        global ct
        ct = 0

    def contains(self, key) -> bool:
        """ Returns a boolean indicating if the given key is present in the tree """
        return bool(self.find_NODE(key))

    def ceil(self, key) -> int or None:
        """
        Given a key, return the closest key that is equal or bigger than it,
        returning None when no such exists
        """
        if self.root is None: return None
        last_found_val = None if self.root.key < key else self.root.key

        def find_ceil(NODE):
            nonlocal last_found_val
            if NODE == self.NIL_LEAF:
                return None
            if NODE.key == key:
                last_found_val = NODE.key
                return NODE.key
            elif NODE.key < key:
                # go right
                return find_ceil(NODE.right)
            else:
                # this NODE is bigger, save its key and go left
                last_found_val = NODE.key

                return find_ceil(NODE.left)

        find_ceil(self.root)
        return last_found_val

    def floor(self, key) -> int or None:
        """
        Given a key, return the closest key that is equal or less than it,
        returning None when no such exists
        """
        if self.root is None: return None
        last_found_val = None if self.root.key < key else self.root.key

        def find_floor(NODE):
            nonlocal last_found_val
            if NODE == self.NIL_LEAF:
                return None
            if NODE.key == key:
                last_found_val = NODE.key
                return NODE.key
            elif NODE.key < key:
                # this NODE is smaller, save its key and go right, trying to find a cloer one
                last_found_val = NODE.key

                return find_floor(NODE.right)
            else:
                return find_floor(NODE.left)

        find_floor(self.root)
        return last_found_val

    def _Delete(self, NODE):
        """
        Receives a NODE with 0 or 1 children (typically some sort of successor)
        and Deletes it according to its color/children
        :param NODE: NODE with 0 or 1 children
        """
        left_child = NODE.left
        right_child = NODE.right
        not_nil_child = left_child if left_child != self.NIL_LEAF else right_child
        if NODE == self.root:
            if not_nil_child != self.NIL_LEAF:
                # if we're removing the root and it has one valid child, simply make that child the root
                self.root = not_nil_child
                self.root.parent = None
                self.root.color = BLACK
            else:
                self.root = None
        elif NODE.color == RED:
            if not NODE.has_children():
                # Red NODE with no children, the simplest Delete
                self._Delete_leaf(NODE)
            else:
                """
                Since the NODE is red he cannot have a child.
                If he had a child, it'd need to be black, but that would mean that
                the black height would be bigger on the one side and that would make our tree invalid
                """
                raise Exception('Unexpected behavior')
        else:  # NODE is black!
            if right_child.has_children() or left_child.has_children():  # sanity check
                raise Exception('The red child of a black NODE with 0 or 1 children'
                                ' cannot have children, otherwise the black height of the tree becomes invalid! ')
            if not_nil_child.color == RED:
                """
                Swap the keys with the red child and Delete it  (basically un-link it)
                Since we're a NODE with one child only, we can be sure that there are no NODEs below the red child.
                """
                NODE.key = not_nil_child.key
                NODE.left = not_nil_child.left
                NODE.right = not_nil_child.right
            else:  # BLACK child
                # 6 cases :o
                self._Delete_black_NODE(NODE)

    def _Delete_leaf(self, leaf):
        """ Simply Deletes a leaf NODE by making it's parent point to a NIL LEAF"""
        if leaf.key >= leaf.parent.key:
            # in those weird cases where they're equal due to the successor swap
            leaf.parent.right = self.NIL_LEAF
        else:
            leaf.parent.left = self.NIL_LEAF

    def _Delete_black_NODE(self, NODE):
        """
        Loop through each case recursively until we reach a terminating case.
        What we're left with is a leaf NODE which is ready to be deleted without consequences
        """
        self.__case_1(NODE)
        self._Delete_leaf(NODE)

    def __case_1(self, NODE):
        """
        Case 1 is when there's a double black NODE on the root
        Because we're at the root, we can simply Delete it
        and reduce the black height of the whole tree.

            __|10B|__                  __10B__
           /         \      ==>       /       \
          9B         20B            9B        20B
        """
        if self.root == NODE:
            NODE.color = BLACK
            return
        self.__case_2(NODE)

    def __case_2(self, NODE):
        """
        Case 2 applies when
            the parent is BLACK
            the sibling is RED
            the sibling's children are BLACK or NIL
        It takes the sibling and rotates it

                         40B                                              60B
                        /   \       --CASE 2 ROTATE-->                   /   \
                    |20B|   60R       LEFT ROTATE                      40R   80B
    DBL BLACK IS 20----^   /   \      SIBLING 60R                     /   \
                         50B    80B                                |20B|  50B
            (if the sibling's direction was left of it's parent, we would RIGHT ROTATE it)
        Now the original NODE's parent is RED
        and we can apply case 4 or case 6
        """
        parent = NODE.parent
        sibling, direction = self._get_sibling(NODE)
        if sibling.color == RED and parent.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
            self.ROTATIONS[direction](NODE=None, parent=sibling, grandfather=parent)
            parent.color = RED
            sibling.color = BLACK
            return self.__case_1(NODE)
        self.__case_3(NODE)

    def __case_3(self, NODE):
        """
        Case 3 deletion is when:
            the parent is BLACK
            the sibling is BLACK
            the sibling's children are BLACK
        Then, we make the sibling red and
        pass the double black NODE upwards

                            Parent is black
               ___50B___    Sibling is black                       ___50B___
              /         \   Sibling's children are black          /         \
           30B          80B        CASE 3                       30B        |80B|  Continue with other cases
          /   \        /   \        ==>                        /  \        /   \
        20B   35R    70B   |90B|<---Delete                   20B  35R     70R   X
              /  \                                               /   \
            34B   37B                                          34B   37B
        """
        parent = NODE.parent
        sibling, _ = self._get_sibling(NODE)
        if (sibling.color == BLACK and parent.color == BLACK
            and sibling.left.color != RED and sibling.right.color != RED):
            # color the sibling red and forward the double black NODE upwards
            # (call the cases again for the parent)
            sibling.color = RED
            return self.__case_1(parent)  # start again

        self.__case_4(NODE)

    def __case_4(self, NODE):
        """
        If the parent is red and the sibling is black with no red children,
        simply swap their colors
        DB-Double Black
                __10R__                   __10B__        The black height of the left subtree has been incremented
               /       \                 /       \       And the one below stays the same
             DB        15B      ===>    X        15R     No consequences, we're done!
                      /   \                     /   \
                    12B   17B                 12B   17B
        """
        parent = NODE.parent
        if parent.color == RED:
            sibling, direction = self._get_sibling(NODE)
            if sibling.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
                parent.color, sibling.color = sibling.color, parent.color  # switch colors
                return  # Terminating
        self.__case_5(NODE)

    def __case_5(self, NODE):
        """
        Case 5 is a rotation that changes the circumstances so that we can do a case 6
        If the closer NODE is red and the outer BLACK or NIL, we do a left/right rotation, depending on the orientation
        This will showcase when the CLOSER NODE's direction is RIGHT

              ___50B___                                                    __50B__
             /         \                                                  /       \
           30B        |80B|  <-- Double black                           35B      |80B|        Case 6 is now
          /  \        /   \      Closer NODE is red (35R)              /   \      /           applicable here,
        20B  35R     70R   X     Outer is black (20B)               30R    37B  70R           so we redirect the NODE
            /   \                So we do a LEFT ROTATION          /   \                      to it :)
          34B  37B               on 35R (closer NODE)           20B   34B
        """
        sibling, direction = self._get_sibling(NODE)
        closer_NODE = sibling.right if direction == 'L' else sibling.left
        outer_NODE = sibling.left if direction == 'L' else sibling.right
        if closer_NODE.color == RED and outer_NODE.color != RED and sibling.color == BLACK:
            if direction == 'L':
                self._left_rotation(NODE=None, parent=closer_NODE, grandfather=sibling)
            else:
                self._right_rotation(NODE=None, parent=closer_NODE, grandfather=sibling)
            closer_NODE.color = BLACK
            sibling.color = RED

        self.__case_6(NODE)

    def __case_6(self, NODE):
        """
        Case 6 requires
            SIBLING to be BLACK
            OUTER NODE to be RED
        Then, does a right/left rotation on the sibling
        This will showcase when the SIBLING's direction is LEFT

                            Double Black
                    __50B__       |                               __35B__
                   /       \      |                              /       \
      SIBLING--> 35B      |80B| <-                             30R       50R
                /   \      /                                  /   \     /   \
             30R    37B  70R   Outer NODE is RED            20B   34B 37B    80B
            /   \              Closer NODE doesn't                           /
         20B   34B                 matter                                   70R
                               Parent doesn't
                                   matter
                               So we do a right rotation on 35B!
        """
        sibling, direction = self._get_sibling(NODE)
        outer_NODE = sibling.left if direction == 'L' else sibling.right

        def __case_6_rotation(direction):
            parent_color = sibling.parent.color
            self.ROTATIONS[direction](NODE=None, parent=sibling, grandfather=sibling.parent)
            # new parent is sibling
            sibling.color = parent_color
            sibling.right.color = BLACK
            sibling.left.color = BLACK

        if sibling.color == BLACK and outer_NODE.color == RED:
            return __case_6_rotation(direction)  # terminating

        raise Exception('We should have ended here, something is wrong')

    def _try_rebalance(self, NODE):
        """
        Given a red child NODE, determine if there is a need to rebalance (if the parent is red)
        If there is, rebalance it
        """
        parent = NODE.parent
        key = NODE.key
        if (parent is None  # what the fuck? (should not happen)
            or parent.parent is None  # parent is the root
            or (NODE.color != RED or parent.color != RED)):  # no need to rebalance
            return
        grandfather = parent.parent
        NODE_dir = 'L' if parent.key > key else 'R'
        parent_dir = 'L' if grandfather.key > parent.key else 'R'
        uncle = grandfather.right if parent_dir == 'L' else grandfather.left
        general_direction = NODE_dir + parent_dir

        if uncle == self.NIL_LEAF or uncle.color == BLACK:
            # rotate
            if general_direction == 'LL':
                self._right_rotation(NODE, parent, grandfather, to_recolor=True)
            elif general_direction == 'RR':
                self._left_rotation(NODE, parent, grandfather, to_recolor=True)
            elif general_direction == 'LR':
                self._right_rotation(NODE=None, parent=NODE, grandfather=parent)
                # due to the prev rotation, our NODE is now the parent
                self._left_rotation(NODE=parent, parent=NODE, grandfather=grandfather, to_recolor=True)
            elif general_direction == 'RL':
                self._left_rotation(NODE=None, parent=NODE, grandfather=parent)
                # due to the prev rotation, our NODE is now the parent
                self._right_rotation(NODE=parent, parent=NODE, grandfather=grandfather, to_recolor=True)
            else:
                raise Exception("{} is not a valid direction!".format(general_direction))
        else:  # uncle is RED
            self._recolor(grandfather)

    def __update_parent(self, NODE, parent_old_child, new_parent):
        """
        Our NODE 'switches' places with the old child
        Assigns a new parent to the NODE.
        If the new_parent is None, this means that our NODE becomes the root of the tree
        """
        NODE.parent = new_parent
        if new_parent:
            # Determine the old child's position in order to put NODE there
            if new_parent.key > parent_old_child.key:
                new_parent.left = NODE
            else:
                new_parent.right = NODE
        else:
            self.root = NODE

    def _right_rotation(self, NODE, parent, grandfather, to_recolor=False):
        grand_grandfather = grandfather.parent
        self.__update_parent(NODE=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_right = parent.right
        parent.right = grandfather
        grandfather.parent = parent

        grandfather.left = old_right  # save the old right keys
        old_right.parent = grandfather

        if to_recolor:
            parent.color = BLACK
            NODE.color = RED
            grandfather.color = RED

    def _left_rotation(self, NODE, parent, grandfather, to_recolor=False):
        grand_grandfather = grandfather.parent
        self.__update_parent(NODE=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_left = parent.left
        parent.left = grandfather
        grandfather.parent = parent

        grandfather.right = old_left  # save the old left keys
        old_left.parent = grandfather

        if to_recolor:
            parent.color = BLACK
            NODE.color = RED
            grandfather.color = RED

    def _recolor(self, grandfather):
        grandfather.right.color = BLACK
        grandfather.left.color = BLACK
        if grandfather != self.root:
            grandfather.color = RED
        self._try_rebalance(grandfather)

    def _find_parent(self, key):
        """ Finds a place for the key in our binary tree"""

        def inner_find(parent):
            """
            Return the appropriate parent NODE for our new NODE as well as the side it should be on
            """
            if key == parent.key:
                return None, None
            elif parent.key < key:
                if parent.right.color == NIL:  # no more to go
                    return parent, 'R'
                return inner_find(parent.right)
            elif key < parent.key:
                if parent.left.color == NIL:  # no more to go
                    return parent, 'L'
                return inner_find(parent.left)

        return inner_find(self.root)

    def find_NODE(self, key):
        def inner_find(root):
            if root is None or root == self.NIL_LEAF:
                return None
            if key > root.key:
                return inner_find(root.right)
            elif key < root.key:
                return inner_find(root.left)
            else:
                return root

        found_NODE = inner_find(self.root)
        return found_NODE

    def _find_in_order_successor(self, NODE):
        right_NODE = NODE.right
        left_NODE = right_NODE.left
        if left_NODE == self.NIL_LEAF:
            return right_NODE
        while left_NODE.left != self.NIL_LEAF:
            left_NODE = left_NODE.left
        return left_NODE

    def _get_sibling(self, NODE):
        """
        Returns the sibling of the NODE, as well as the side it is on
        e.g

            20 (A)
           /     \
        15(B)    25(C)

        _get_sibling(25(C)) => 15(B), 'R'
        """
        parent = NODE.parent
        if NODE.key >= parent.key:
            sibling = parent.left
            direction = 'L'
        else:
            sibling = parent.right
            direction = 'R'
        return sibling, direction



