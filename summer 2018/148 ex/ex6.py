"""
Implement the get_nodes_connecting method.
"""
from typing import Any, List

class Tree:
    """
    A class representing a Tree.

    value - The value of the Tree's root
    children - The root nodes of the children of this Tree.
    """
    value: Any
    children: List['Tree']

    def __init__(self, value: Any, children: List['Tree'] = None) -> None:
        """
        Initialize this Tree with the root value value and children children.
        """
        self.value = value

        # We make this a copy of the list children, in case it gets modified
        # at some point elsewhere.
        self.children = children[:] if children else []

    def contains(self, value: Any) -> bool:
        """
        Return whether value appears anywhere in this Tree.

        >>> t1 = Tree(1, [Tree(3, [Tree(4), Tree(6)])])
        >>> t2 = Tree(2, [Tree(8)])
        >>> t3 = Tree(9, [Tree(7), Tree(5)])
        >>> children = [t1, t2, t3]
        >>> t = Tree(0, children)
        >>> t.contains(5)
        True
        >>> t.contains(20)
        False
        """
        if self.value == value:
            return True

        return any([child.contains(value) for child in self.children])

    def __str__(self) -> str:
        """
        Return the string representation of this Tree, such that the root
        node is at the top, and all subtrees are below it. Every line of
        the string has the same length (being padded with spaces if needed).

        >>> t1 = Tree(1, [Tree(3, [Tree(4), Tree(6)])])
        >>> print(t1)
          1
          3
        4   6
        >>> t2 = Tree(2, [Tree(8)])
        >>> print(t2)
        2
        8
        >>> t3 = Tree(9, [Tree(7), Tree(5)])
        >>> print(t3)
          9
        7   5
        >>> children = [t1, t2, t3]
        >>> t = Tree(0, children)
        >>> print(t)
                0
          1     2     9
          3     8   7   5
        4   6
        """
        child_strings = [str(child).split('\n') for child in self.children]

        # Get the maximum number of lines from a child's string
        max_lines = 0
        if child_strings:
            max_lines = max([len(child) for child in child_strings])

        # Create a list with max_lines empty lists in it
        new_string = [[] for _ in range(max_lines)]

        # Join each line of each child's string
        for i in range(max_lines):
            for child in child_strings:
                if i < len(child):
                    new_string[i].append(child[i])
                else:
                    # If there is no such line, just pad it with spaces
                    new_string[i].append(" " * len(child[0]))

        # Put 3 spaces between each subtree
        new_string_joined = [(' ' * 3).join(child) for child in new_string]

        # Add in the value of the current Tree
        str_width = 0
        if new_string_joined:
            str_width = len(new_string_joined[0])

        left_padding = str_width // 2
        right_padding = (str_width - str_width // 2) - 1

        new_string_joined.insert(0, "{}{}{}".format(" " * left_padding,
                                                    self.value,
                                                    " " * right_padding))

        # Return the new string
        return "\n".join(new_string_joined)

    def get_nodes_connecting(self, value1: Any, value2: Any) -> list:
        """
        Return the values of nodes that connect value1 and value. If value1
        and value2 don't appear in this Tree, return an empty list.

        >>> t1 = Tree(2, [Tree(5)])
        >>> t2 = Tree(3)
        >>> t3 = Tree(4, [Tree(6), Tree(7)])
        >>> t = Tree(1, [t1, t2, t3])
        >>> print(t)
              1
        2   3     4
        5       6   7
        3 4    1 3
                  2 3
        >>> t.get_nodes_connecting(1, 2)
        [1, 2]
        >>> t.get_nodes_connecting(2, 2)
        [2]
        >>> t.get_nodes_connecting(5, 4)
        [5, 2, 1, 4]
        >>> t.get_nodes_connecting(6, 7)
        [6, 4, 7]
        """
        result = []
        if self.contains(value1):
            result = self.get_path(value1)[::-1]
        if self.contains(value2):
            result = result[:-1]
            result += self.get_path(value2)
        for c in self.children:
            if c.contains(value1) and c.contains(value2):
                return c.get_nodes_connecting(value1, value2)
        return result

    def get_path(self, value):
        """
        Return the values of nodes that connect value1 and value. If value1
        and value2 don't appear in this Tree, return an empty list.

        >>> t1 = Tree(2, [Tree(5)])
        >>> t2 = Tree(3)
        >>> t3 = Tree(4, [Tree(6), Tree(7)])
        >>> t = Tree(1, [t1, t2, t3])
        >>> print(t)
              1
        2   3     4
        5       6   7
        >>> t.get_path(5)
        [1, 2, 5]
        """
        if self.value == value:
            return [value]
        for c in self.children:
            if c.contains(value):
                return [self.value] + c.get_path(value)


if __name__ == '__main__':
    t1 = Tree(2, [Tree(5)])
    t2 = Tree(3)
    t3 = Tree(4, [Tree(6), Tree(7)])
    t = Tree(1, [t1, t2, t3])

    # t is the Tree from the handout:
    #       1
    # 2   3     4
    # 5       6   7

    assert t.get_nodes_connecting(1, 2) == [1, 2]
    assert t.get_nodes_connecting(2, 1) == [2, 1]
    assert t.get_nodes_connecting(2, 2) == [2]
    assert t.get_nodes_connecting(5, 4) == [5, 2, 1, 4]
    assert t.get_nodes_connecting(6, 7) == [6, 4, 7]

    import python_ta
    python_ta.check_all(config='ex6_pyta.txt')
