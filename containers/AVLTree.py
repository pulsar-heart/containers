'''
This file implements the AVL Tree data structure.
The functions in this file are considerably harder than the functions in the BinaryTree and BST files,
but there are fewer of them.
'''

from containers.BinaryTree import BinaryTree, Node
from containers.BST import BST
import copy


class AVLTree(BST):
    '''
    FIXME:
    AVLTree is currently not a subclass of BST.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        Implement this function.
        '''
        super().__init__()

    def balance_factor(self):
        '''
        Returns the balance factor of a tree.
        '''
        return AVLTree._balance_factor(self.root)

    @staticmethod
    def _balance_factor(node):
        '''
        Returns the balance factor of a node.
        '''
        if node is None:
            return 0
        if node.left is None:
            height_left = 0
        else:
            height_left = 1 + BinaryTree._height(node.left)
        if node.right is None:
            height_right = 0
        else:
            height_right = 1 + BinaryTree._height(node.right)
        return height_left - height_right

    def is_avl_satisfied(self):
        '''
        Returns True if the avl tree satisfies that all nodes have a balance factor in [-1,0,1].
        '''
        return AVLTree._is_avl_satisfied(self.root)

    @staticmethod
    def _is_avl_satisfied(node):
        '''
        FIXME:
        Implement this function.
        '''
        if node is None:
            return True
        options = [-1, 0, 1]
        if AVLTree._balance_factor(node) not in options:
            return False
        is_left_avl = AVLTree._is_avl_satisfied(node.left)
        is_right_avl = AVLTree._is_avl_satisfied(node.right)
        return is_left_avl and is_right_avl

    @staticmethod
    def _left_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        rot_root = copy.deepcopy(node)
        new_root = rot_root.right
        rot_root.right = new_root.left
        new_root.left = rot_root
        return new_root

    @staticmethod
    def _right_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        rot_root = copy.deepcopy(node)
        new_root = rot_root.left
        rot_root.left = new_root.right
        new_root.right = rot_root
        return new_root

    def insert(self, value):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of how to insert into an AVL tree,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.

        HINT:
        It is okay to add @staticmethod helper functions for this code.
        The code should look very similar to the code for your insert function for the BST,
        but it will also call the left and right rebalancing functions.
        '''
        node = self.root
        if node is None:
            node = Node(value)
            self.root = node
            return
        BST._insert(node, value)
        AVLTree._recurse_children(value, node)

    @staticmethod
    def _recurse_children(value, node):
        if node is None:
            return
        AVLTree._check_balance(node)
        if value == 'do' or BST._find(value, node.left):
            AVLTree._check_balance(node.left)
            AVLTree._recurse_children(value, node.left)
        if value == 'do' or BST._find(value, node.right):
            AVLTree._check_balance(node.right)
            AVLTree._recurse_children(value, node.right)

    @staticmethod
    def _check_balance(node):
        unbalanced = [-2, 2]
        if AVLTree._balance_factor(node) in unbalanced:
            balanced_node = AVLTree._rebalance(node)
            node.value = balanced_node.value
            node.left = balanced_node.left
            node.right = balanced_node.right
            AVLTree._recurse_children('do', node)

    @staticmethod
    def _rebalance(node):
        '''
        There are no test cases for the rebalance function,
        so you do not technically have to implement it.
        But both the insert function needs the rebalancing code,
        so I recommend including that code here.
        '''
        new_node = copy.deepcopy(node)
        if AVLTree._balance_factor(node) < 0:
            if AVLTree._balance_factor(node.right) > 0:
                new_node.right = AVLTree._right_rotate(node.right)
                new_node = AVLTree._left_rotate(new_node)
            else:
                new_node = AVLTree._left_rotate(new_node)
        elif AVLTree._balance_factor(node) > 0:
            if AVLTree._balance_factor(node.left) < 0:
                new_node.left = AVLTree._left_rotate(node.left)
                new_node = AVLTree._right_rotate(new_node)
            else:
                new_node = AVLTree._right_rotate(new_node)
        return new_node
