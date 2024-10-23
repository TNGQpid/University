class Node():
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None
    
    def __len__(self):
        size = len(self.values)
        if self.left != None:
            size += len(self.left.values)
        if self.right != None:
            size += len(self.right.values)
        return size
    
    def lookup(self, key):
        if key == self.key:
            return self.values
        if key < self.key and self.left != None:
            return self.left.lookup(key)
        if key > self.key and self.right != None:
            return self.right.lookup(key)
        return []

class BST():
    def __init__(self):
        self.root = None

    def add(self, key, val):
        if self.root == None:
            self.root = Node(key)

        curr = self.root
        while True:
            if key < curr.key:
                # go left
                if curr.left == None:
                    curr.left = Node(key)
                curr = curr.left
            elif key > curr.key:
                 # go right
                if curr.right == None:
                    curr.right = Node(key)
                curr = curr.right
            else:
                # found it!
                assert curr.key == key
                break

        curr.values.append(val)
        
    def __dump(self, node):
        if node == None:
            return
        self.__dump(node.right)            # 1
        print(node.key, ":", node.values)  # 2
        self.__dump(node.left)             # 3

    def dump(self):
        self.__dump(self.root)
    
    def __getitem__(self, key):
        return self.root.lookup(key)
    
    
    def get_height(self, node):
        if node == None:
            return 0
        depthL = self.get_height(node.left)
        depthR = self.get_height(node.right)
        if depthL < depthR:
            return depthR + 1
        else:
            return depthL + 1
    
    def num_nonleaf_nodes(self, node):
        if node == None:
            return 0
        if node.left == None and node.right == None: #no children, it's a leaf
            return 0
        if node.right and node.left: # it has two children, it's a non-leaf
            return 1 + self.num_nonleaf_nodes(node.left) + self.num_nonleaf_nodes(node.right)
        else: #it has one child, it's a non-leaf
            l = self.num_nonleaf_nodes(node.left)
            r = self.num_nonleaf_nodes(node.right)
            return 1+ l + r
    def total(self, node):
        if node == None:
            return 0
        return 1 + self.total(node.right) + self.total(node.left)
        
    def top(self, curr, num, wanted = []):
        if curr != None:
            self.top(curr.right, num)
            self.top(curr.left, num)
            wanted.append(curr.key)
        return sorted(wanted)[-num:]
        
        
            

