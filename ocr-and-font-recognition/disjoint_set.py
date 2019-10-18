class Label(object):
    def __init__(self, value):
        self.value = value
        self.parent = self
        self.rank = 0
    def __eq__(self, other):
        if type(other) is type(self):
            return self.value == other.value
        else:
            return False
    def __ne__(self, other):
        return not self.__eq__(other)


class DisjointSet:
    def __init__(self):
        self.labelSets = {}


    def MakeSet(self, x):
        try:
            return self.labelSets[x]
        except KeyError:
            item = Label(x)
            self.labelSets[x] = item
            return item


    def Find(self, item):
        if item.parent != item:
            item.parent = self.Find(item.parent)
        return item.parent


    def Union(self, x, y):
        """
        :param x:
        :param y:
        :return: root node of new union tree
        """
        x_root = self.Find(x)
        y_root = self.Find(y)
        if x_root == y_root:
            return x_root

        if x_root.rank < y_root.rank:
            x_root.parent = y_root
            return y_root
        elif x_root.rank > y_root.rank:
            y_root.parent = x_root
            return x_root
        else:
            y_root.parent = x_root
            x_root.rank += 1
            return x_root


