class rbnode(object):
    def __init__(self, key):
        self._key = key
        self._red = False
        self._left = None
        self._right = None
        self._p = None

    key = property(fget=lambda self: self._key)
    red = property(fget=lambda self: self._red)
    left = property(fget=lambda self: self._left)
    right = property(fget=lambda self: self._right)
    p = property(fget=lambda self: self._p)


class rbtree(object):
    def __init__(self, create_node=rbnode):
        self._nil = create_node(key=None)
        self._root = self.nil
        self._create_node = create_node
        self.totalCount = 0
        self.insertCount = 0
        self.deleteCount = 0
        self.missCount = 0
        self.blackCount = 0
        self.inorderTraverseList = []

    root = property(fget=lambda self: self._root)
    nil = property(fget=lambda self: self._nil)

    def search(self, key, x=None):
        if None == x:
            x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x


    def minimum(self, x=None):
        if None == x:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x

    def maximum(self, x=None):
        if None == x:
            x = self.root
        while x.right != self.nil:
            x = x.right
        return x

    def inorder_traverse(self, x=None) :
        stack = []
        if x == None:
            x = self.root
        while x != self.nil or len(stack) != 0:
            if x != self.nil:
                stack.append(x)
                x = x.left
            else:
                x = stack.pop()
                self.inorderTraverseList.append(x)
                if not x.red :
                    self.blackCount += 1
                x = x.right

    def get_black_height(self, x=None):
        if None == x:
            x = self.root
        blackHeight = 0
        while x != self.nil:
            if not x.red:
                blackHeight += 1
            x = x.left
        return blackHeight

    def transplant(self, u, v):
        if u.p == self.nil:
            self._root = v
        elif u == u.p.left:
            u.p._left = v
        else :
            u.p._right = v
        v._p = u.p

    def delete_key(self,key):
        node = self.search(key)
        if node != self.nil:
            self.delete_node(node)
            self.deleteCount += 1
            self.totalCount -= 1
        else :
            self.missCount += 1

    def delete_node(self, z):
        y = z
        y_original_color = y.red
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(z,z.left)
        else :
            y = self.minimum(z.right)
            y_original_color = y.red
            x = y.right
            if y.p == z :
                x._p = y
            else :
                self.transplant(y, y.right)
                y._right = z.right
                y.right._p = y
            self.transplant(z,y)
            y._left = z.left
            y.left._p = y
            y._red = z.red
        if y_original_color == False:
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        while x != self.root and x.red == False:
            if x == x.p.left:
                w = x.p.right
                if w.red == True:
                    w._red = False
                    x.p._red = True
                    self._left_rotate(x.p)
                    w = x.p.right
                if w.left.red == False and w.right.red == False:
                    w._red = True
                    x = x.p
                else :
                    if w.right.red == False:
                        w.left._red = False
                        w._red = True
                        self._right_rotate(w)
                        w = x.p.right
                    w._red = x.p.red
                    x.p._red = False
                    w.right._red = False
                    self._left_rotate(x.p)
                    x = self.root
            else :
                w = x.p.left
                if w.red == True:
                    w._red = False
                    x.p._red = True
                    self._right_rotate(x.p)
                    w = x.p.left
                if w.left.red == False and w.right.red == False:
                    w._red = True
                    x = x.p
                else :
                    if w.left.red == False:
                        w.right._red = False
                        w._red = True
                        self._left_rotate(w)
                        w = x.p.left
                    w._red = x.p.red
                    x.p._red = False
                    w.left._red = False
                    self._right_rotate(x.p)
                    x = self.root
        x._red = False


    def insert_key(self, key):
        self.insert_node(self._create_node(key=key))
        self.insertCount += 1
        self.totalCount += 1

    def insert_node(self, z):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z._p = y
        if y == self.nil:
            self._root = z
        elif z.key < y.key:
            y._left = z
        else:
            y._right = z
        z._left = self.nil
        z._right = self.nil
        z._red = True
        self._insert_fixup(z)

    def _insert_fixup(self, z):
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._left_rotate(z.p.p)
        self.root._red = False


    def _left_rotate(self, x):
        "Left rotate x."
        y = x.right
        x._right = y.left
        if y.left != self.nil:
            y.left._p = x
        y._p = x.p
        if x.p == self.nil:
            self._root = y
        elif x == x.p.left:
            x.p._left = y
        else:
            x.p._right = y
        y._left = x
        x._p = y


    def _right_rotate(self, y):
        x = y.left
        y._left = x.right
        if x.right != self.nil:
            x.right._p = y
        x._p = y.p
        if y.p == self.nil:
            self._root = x
        elif y == y.p.right:
            y.p._right = x
        else:
            y.p._left = x
        x._right = y
        y._p = x
