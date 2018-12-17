"""
Implement the get_largest_height_difference method.
"""
from typing import Any, Union

class BinaryTree:
    """
    A class representing a BinaryTree.

    value - The value of the BinaryTree's root
    left - The root node of this BinaryTree's left subtree.
    right - The root node of this BinaryTree's right subtree.
    """
    value: Any
    left: 'BinaryTree'
    right: 'BinaryTree'

    def __init__(self, value: Any, left: 'BinaryTree' = None,
                 right: 'BinaryTree' = None) -> None:
        """
        Initialize this BinaryTree with the root value value, left subtree left,
        and right subtree right.
        """
        self.value = value
        self.left = left
        self.right = right

    def __str__(self) -> str:
        """
        Return the string representation of this BinaryTree, such that the root
        node is at the top, and all subtrees are below it. Every line of
        the string has the same length (being padded with spaces if needed).

        >>> t1 = BinaryTree(1, BinaryTree(3, BinaryTree(4), BinaryTree(6)))
        >>> print(t1)
          1
          3
        4   6
        >>> t2 = BinaryTree(9, BinaryTree(7), BinaryTree(5))
        >>> print(t2)
          9
        7   5
        >>> t = BinaryTree(0, t1, t2)
        >>> print(t)
              0
          1       9
          3     7   5
        4   6
        """
        children = []
        if self.left:
            children.append(self.left)

        if self.right:
            children.append(self.right)

        child_strings = [str(child).split('\n') for child in children]

        # Get the maximum number of lines from a child's string
        max_lines = 0
        if child_strings:
            max_lines = max([len(child) for child in child_strings])

        # Create a list with max_lines empty lists in it
        new_string = [[] for _ in range(max_lines)]

        # Join each line of each child's string
        for i in range(max_lines):
            for child in child_strings:
                child_length = max([len(line) for line in child])

                if i < len(child):
                    padding_needed = child_length - len(child[i])
                    new_string[i].append(child[i] + " " * padding_needed)
                else:
                    # If there is no such line, just pad it with spaces
                    new_string[i].append(" " * child_length)

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

        new_string_joined = [line.rstrip() for line in new_string_joined]

        # Return the new string
        return "\n".join(new_string_joined)

def get_height(tree: Union[BinaryTree, None]) -> int:
    """
    Return the height of tree.

    >>> t1 = BinaryTree(3, BinaryTree(5, right = BinaryTree(2)))
    >>> t2 = BinaryTree(4, BinaryTree(6), BinaryTree(7))
    >>> t = BinaryTree(1, t1, t2)
    >>> get_height(t)
    4
    """
    if not tree:
        return 0

    return 1 + max(get_height(tree.left), get_height(tree.right))

def get_largest_height_difference(tree: Union[BinaryTree, None]) -> int:
    """
    Return the largest height difference between two children in tree.

    >>> t1 = BinaryTree(3, BinaryTree(5, right = BinaryTree(2)))
    >>> t2 = BinaryTree(4, BinaryTree(6), BinaryTree(7))
    >>> t = BinaryTree(1, t1, t2)
    >>> get_largest_height_difference(t)
    2
    """
    if not tree:
        return 0
    height = [abs(get_height(tree.left) - get_height(tree.right))]
    if tree.left:
        height.append(get_largest_height_difference(tree.left))
    if tree.right:
        height.append(get_largest_height_difference(tree.right))
    return max(height)

if __name__ == '__main__':
    t1 = BinaryTree(3, BinaryTree(5, right=BinaryTree(2)))
    t2 = BinaryTree(4, BinaryTree(6), BinaryTree(7))
    t = BinaryTree(1, t1, t2)

    # t is the Tree from the handout:
    #       1
    #     3     4
    # 5       6   7
    #   2

    assert get_largest_height_difference(None) == 0
    assert get_largest_height_difference(t1) == 2
    assert get_largest_height_difference(t2) == 0
    assert get_largest_height_difference(t) == 2

    import python_ta
    python_ta.check_all(config='ex7_pyta.txt')
