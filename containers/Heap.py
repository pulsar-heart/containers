'''
This file implements the Heap data structure as a subclass of the BinaryTree.
The book implements Heaps using an *implicit* tree with an *explicit* vector implementation,
so the code in the book is likely to be less helpful than the code for the other data structures.
The book's implementation is the traditional implementation because it has a faster constant factor
(but the same asymptotics).
This homework is using an explicit tree implementation to help you get more practice with OOP-style programming and classes.
'''

from containers.BinaryTree import BinaryTree, Node


class Heap(BinaryTree):
    '''
    FIXME:
    Heap is currently not a subclass of BinaryTree.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the Heap.
        '''
        self.size = 0
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
        Thus, if you create a variable using the command Heap([1,2,3])
        it's __repr__ will return "Heap([1,2,3])"

        For the Heap, type(self).__name__ will be the string "Heap",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of Heap will have a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def is_heap_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether insert/delete functions
        are actually working.
        '''
        if self.root:
            return Heap._is_heap_satisfied(self.root)
        return True

    @staticmethod
    def _is_heap_satisfied(node):
        '''
        FIXME:
        Implement this method.
        '''
        ret = True
        if node is None:
            return True
        if node.right is None or node.left is None:
            ret &= Heap._missing_child(node)
        elif node.left.value is None or node.right.value is None or node.value is None:
            raise ValueError(node)
        elif node.left.value < node.value or node.right.value < node.value:
            return False
        ret &= Heap._is_heap_satisfied(node.left) and Heap._is_heap_satisfied(node.right)
        return ret

    def _missing_child(node):
        if node.right:
            return False
        elif node.left:
            if node.left.value < node.value:
                return False
            if node.left.left or node.left.right:
                return False
        return True

    def insert(self, value):
        '''
        Inserts value into the heap.

        FIXME:
        Implement this function.

        HINT:
        The pseudo code is
        1. Find the next position in the tree using the binary representation of the total number of nodes
            1. You will have to explicitly store the size of your heap in a variable (rather than compute it) to maintain the O(log n) runtime
            1. See https://stackoverflow.com/questions/18241192/implement-heap-using-a-binary-tree for hints
        1. Add `value` into the next position
        1. Recursively swap value with its parent until the heap property is satisfied

        HINT:
        Create a @staticmethod helper function,
        following the same pattern used in the BST and AVLTree insert functions.
        '''
        if self.root is None:
            self.root = Node(value)
            self.size = 1
            return
        self.size = Heap._size(self.root) + 1 
        if not self.is_heap_satisfied():
            raise ValueError('heap not satisfied')
        else:
            binary = bin(self.size)[3:]
            Heap._insert(self.root, binary, value)
            Heap._swap(self.root, binary)
    
    @staticmethod
    def _size(node):
        if node is None:
            return 0
        ret = 1
        if node.left:
            ret += Heap._size(node.left)
        if node.right:
            ret += Heap._size(node.right)
        return ret

    @staticmethod
    def _insert(node, binary, value):
        if len(binary) == 1:
            if binary == '0':
                node.left = Node(value)
            else:
                node.right = Node(value)
            return
        dig = binary[0]
        if dig == '0':
            Heap._insert(node.left, binary[1:], value)
        elif dig == '1':
            Heap._insert(node.right, binary[1:], value)
        else:
            raise ValueError('invalid character in binary')

    @staticmethod
    def _swap(node, binary):
        if Heap._is_heap_satisfied(node):
            return
        if not binary:
            if node.value > node.left.value:
                val1 = node.value
                node.value = node.left.value
                node.left.value = val1
            elif node.value > node.right.value:
                val1 = node.value
                node.value = node.right.value
                node.right.value = val1
            else:
                raise ValueError('binary is empty')
                return
        else:
            new_node = node
            for dig in binary:
                parent = new_node
                if dig == '0':
                    new_node = new_node.left
                else:
                    new_node = new_node.right
            if parent.value > new_node.value:
                val1 = parent.value
                parent.value = new_node.value
                new_node.value = val1
        Heap._swap(node, binary[:-1])

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.
        '''
        for x in xs:
            self.insert(x)
    
    def find_smallest(self):
        '''
        Returns the smallest value in the tree.

        FIXME:
        Implement this function.
        '''
        if self.root is None:
            return
        else:
            return self.root.value
            
    @staticmethod
    def _find_smallest(node, binary):
        if not binary:
            return node.value
        dig = binary[0]
        if dig == '0':
            return Heap._find_smallest(node.left, binary[1:])
        elif dig == '1':
            return Heap._find_smallest(node.right, binary[1:])
        else:
            raise ValueError('invalid character in binary')

    def remove_min(self):
        '''
        Removes the minimum value from the Heap.
        If the heap is empty, it does nothing.

        FIXME:
        Implement this function.

        HINT:
        The pseudocode is
        1. remove the bottom right node from the tree
        2. replace the root node with what was formerly the bottom right
        3. "trickle down" the root node: recursively swap it with its largest child until the heap property is satisfied

        HINT:
        I created two @staticmethod helper functions: _remove_bottom_right and _trickle.
        It's possible to do it with only a single helper (or no helper at all),
        but I personally found dividing up the code into two made the most sense.
        '''
        if self.root is None:
            return
        elif self.root.left is None:
            self.root = None
        else:
            size = Heap._size(self.root)
            binary = bin(size)[3:]
            self.root.value = Heap._remove(self.root, binary)
            Heap._trickle_down(self.root)

    @staticmethod
    def _remove(node, binary):
        if len(binary) == 1:
            if binary == '0':
                val1 = node.left.value
                node.left = None
                return val1
            elif binary == '1':
                val1 = node.right.value
                node.right = None
                return val1
        else:
            dig = binary[0]
            if dig == '0':
                return Heap._remove(node.left, binary[1:])
            elif dig == '1':
                return Heap._remove(node.right, binary[1:])
            else:
                raise ValueError('digit not valid')

    @staticmethod
    def _trickle_down(node):
        if Heap._is_heap_satisfied(node):
            return
        if node.left and not node.right or node.left.value < node.right.value:
            val1 = node.value
            node.value = node.left.value
            node.left.value = val1
            Heap._trickle_down(node.left)
        else:
            val1 = node.value
            node.value = node.right.value
            node.right.value = val1
            Heap._trickle_down(node.right)
