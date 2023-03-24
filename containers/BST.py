'''
CHange.
This file implements the Binary Search Tree data structure.
The functions in this file are considerably harder than the functions in the BinaryTree file.
'''

from containers.BinaryTree import BinaryTree, Node


class BST(BinaryTree):
    '''
    The BST is a superclass of BinaryTree.
    That means that the BST class "inherits" all of the methods from BinaryTree,
    and we don't have to reimplement them.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the BST.
        '''
        super().__init__()
        if xs:
            for x in xs:
                self.insert(x)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string that can be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command BST([1,2,3])
        it's __repr__ will return "BST([1,2,3])"

        For the BST, type(self).__name__ will be the string "BST",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of BST will have a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def __iter__(self, traversal_type = 'inorder'):
        yield from self.to_list(traversal_type)
        
    def is_bst_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether insert/delete functions
        are actually working.
        '''
        if self.root:
            return BST._is_bst_satisfied(self.root)
        return True

        return ret

    def insert(self, value):
        '''
        Inserts value into the BST.

        FIXME:
        Implement this function.

        HINT:
        Create a staticmethod helper function following the pattern of _is_bst_satisfied.
        '''
        if self.root:
            return BST._insert(self.root, value)
        else:
            self.root = Node(value)

    @staticmethod
    def _insert(node, value):
        if value <= node.value:
            if node.left:
                BST._insert(node.left, value)
            else:
                node.left = Node(value)
        elif value > node.value:
            if node.right:
                BST._insert(node.right, value)
            else:
                node.right = Node(value)


    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.

        HINT:
        Repeatedly call the insert method.
        You cannot get this method to work correctly until you have gotten insert to work correctly.
        '''
        for x in xs:
            self.insert(x)

    def __contains__(self, value):
        '''
        Recall that `x in tree` desugars to `tree.__contains__(x)`.
        '''
        return self.find(value)

    def find(self, value):
        '''
        Returns whether value is contained in the BST.

        FIXME:
        Implement this function.
        '''
        if self.root:
            return BST._find(value, self.root)
        else:
            return False

    @staticmethod
    def _find(value, node):
        '''
        FIXME:
        Implement this function.
        '''
        ret = False
        if node.value == value:
            return True
        if node.left:
            if value < node.value:
                return BST._find(value, node.left)
            elif value == node.value:
                return True
        if node.right:
            if value > node.value:
                return BST._find(value, node.right)
            elif value == node.value:
                return True

    def find_smallest(self):
        '''
        Returns the smallest value in the tree.
        '''
        if self.root is None:
            raise ValueError('Nothing in tree')
        else:
            return BST._find_smallest(self.root)

    @staticmethod
    def _find_smallest(node):
        '''
        This is a helper function for find_smallest and not intended to be called directly by the user.
        '''
        assert node is not None
        if node.left is None:
            return node.value
        else:
            return BST._find_smallest(node.left)

    def find_largest(self):
        '''
        Returns the largest value in the tree.

        FIXME:
        Implement this function.

        HINT:
        Follow the pattern of the _find_smallest function.
        '''
        if self.root is None:
            raise ValueError('Nothing in tree')
        else:
            return BST._find_largest(self.root)

    @staticmethod
    def _find_largest(node):
        assert node is not None
        if node.right is None:
            return node.value
        else:
            return BST._find_largest(node.right)

    def remove(self, value):
        '''
        Removes value from the BST.
        If value is not in the BST, it does nothing.

        FIXME:
        Implement this function.

        HINT:
        You should have everything else working before you implement this function.

        HINT:
        Use a recursive helper function.
        '''
        if self.root == None:
            return
        if self.root.value == value and not self.root.left and not self.root.right:
            self.root = None
        if self.__contains__(value):
            BST._remove(self.root, value)

    @staticmethod
    def _remove(node, value):
        print('in remove')
        print(value)
        print(node)
        new_node = BST._remove_helper(node, value)
        print(new_node)
        node.value = new_node.value
        node.left = new_node.left
        node.right = new_node.right
        
    
    @staticmethod
    def _remove_helper(node, value):
        if node.value == value:
            print('in if 1')
            if node.left == None and node.right == None:
                print('in if none')
                return
            elif node.left and node.right == None:
                print('in elif left')
                return node.left
            elif node.right and node.left == None:
                print('in elif right')
                print(node.right)
                return node.right
            else:
                print('in else')
                succ = BST.find_successor(node)
                if succ == value:
                    node.right = BST._remove_helper(node.right, value)
                else: 
                    BST._remove(node, succ)
                new_node = Node(succ)
                new_node.left = node.left
                new_node.right = node.right
                return new_node
        if node.left:
            print('left')
            if value < node.value:
                print('recur left')
                node.left = BST._remove_helper(node.left, value)
                return node
        if node.right:
            print('right')
            if value > node.value:
                print('recur')
                node.right = BST._remove_helper(node.right, value)
                return node

    @staticmethod
    def find_successor(node):
        succ = None
        if node.right:
            succ = BST.find_del_smallest(node.right)
        return succ

    @staticmethod
    def find_del_smallest(node):
        if node.left is None:
            succ = node.value
            return succ
        else:
            return BST.find_del_smallest(node.left)

    def remove_list(self, xs):
        '''
        Given a list xs, remove each element of xs from self.

        FIXME:
        Implement this function.

        HINT:
        See the insert_list function.
        '''
        if xs:
            for x in xs:
                self.remove(x)


    @staticmethod
    def _is_bst_satisfied(node):
        '''
        FIXME:
        The current implementation has a bug:
        it only checks if the children of the current node are less than/greater than,
        rather than ensuring that all nodes to the left/right are less than/greater than.

        HINT:
        Use the _find_smallest and _find_largest functions to fix the bug.
        You should use the _ prefixed methods because those are static methods just like this one.
        '''
        ret = True
        if node.value == None:
            if node.left or node.right:
                return False
            else:
                return True
        if node.left:
            if node.value >= BST._find_largest(node.left):
                ret &= BST._is_bst_satisfied(node.left)
            else:
                ret = False
        if node.right:
            if node.value == None:
                raise ValueError('value is none')
            if BST._find_smallest(node.right) == None:
                raise ValueError('find smallest is none', str(node.right))
            if node.value <= BST._find_smallest(node.right):
                ret &= BST._is_bst_satisfied(node.right)
            else:
                ret = False
        return ret
