"""CSC148 Assignment 2: Autocompleter classes

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This file contains the design of a public interface (Autocompleter) and two
implementation of this interface, SimplePrefixTree and CompressedPrefixTree.
You'll complete both of these subclasses over the course of this assignment.

As usual, be sure not to change any parts of the given *public interface* in the
starter code---and this includes the instance attributes, which we will be
testing directly! You may, however, add new private attributes, methods, and
top-level functions to this file.
"""
from __future__ import annotations
from typing import Any, List, Optional, Tuple


################################################################################
# The Autocompleter ADT
################################################################################
class Autocompleter:
    """An abstract class representing the Autocompleter Abstract Data Type.
    """
    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter."""
        raise NotImplementedError

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this prefix tree
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
            weight > 0
            The given value is either:
                1) not in this Autocompleter
                2) was previously inserted with the SAME prefix sequence
        """
        raise NotImplementedError

    def autocomplete(self, prefix: List,
                     limit: Optional[int] = None) -> List[Tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given prefix.

        Precondition: limit is None or limit > 0.
        """
        raise NotImplementedError

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
        """
        raise NotImplementedError


################################################################################
# SimplePrefixTree (Tasks 1-3)
################################################################################
class SimplePrefixTree(Autocompleter):
    """A simple prefix tree.

    This class follows the implementation described on the assignment handout.
    Note that we've made the attributes public because we will be accessing them
    directly for testing purposes.

    === Attributes ===
    value:
        The value stored at the root of this prefix tree, or [] if this
        prefix tree is empty.
    weight:
        The weight of this prefix tree. If this tree is a leaf, this attribute
        stores the weight of the value stored in the leaf. If this tree is
        not a leaf and non-empty, this attribute stores the *aggregate weight*
        of the leaf weights in this tree.
    subtrees:
        A list of subtrees of this prefix tree.

    === Representation invariants ===
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, this tree is a leaf.
        (self.value is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If len(self.subtrees) > 0, then self.value is a list (*common prefix*),
        and self.weight > 0 (*aggregate weight*).

    - ("prefixes grow by 1")
      If len(self.subtrees) > 0, and subtree in self.subtrees, and subtree
      is non-empty and not a leaf, then

          subtree.value == self.value + [x], for some element x

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of their weights.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a `weight`
      attribute.
    """

    value: Any
    weight: float
    subtrees: List[SimplePrefixTree]
    weight_type: str
    leaf: int

    def __init__(self, weight_type: str) -> None:
        """Initialize an empty simple prefix tree.

        Precondition: weight_type == 'sum' or weight_type == 'average'.

        The given <weight_type> value specifies how the aggregate weight
        of non-leaf trees should be calculated (see the assignment handout
        for details).
        """
        self.weight = 0.0
        self.value = []
        self.subtrees = []
        self.weight_type = weight_type
        self.leaf = 0

    def is_empty(self) -> bool:
        """Return whether this simple prefix tree is empty."""
        return self.weight == 0.0

    def is_leaf(self) -> bool:
        """Return whether this simple prefix tree is a leaf."""
        return self.weight > 0 and self.subtrees == []

    def __str__(self) -> str:
        """Return a string representation of this tree.

        You may find this method helpful for debugging.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + f'{self.value} ({self.weight})\n'
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    def _find_average(self) -> float:
        """ helper to calculate average weight."""
        sum_weight = 0
        for s in self.subtrees:
            if s.is_leaf():
                sum_weight += s.weight
            else:
                sum_weight += s.weight * s.leaf
        return sum_weight / self.leaf

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """ Insert the given value into this SimplePrefixTree.
        """
        if prefix:
            for t in self.subtrees:
                if self.value + [prefix[0]] == t.value:
                    old_weight = t.weight
                    old_leaf = t.leaf
                    t.insert(value, weight, prefix[1:])
                    self.leaf += t.leaf - old_leaf
                    if self.weight_type == 'sum':
                        self.weight += t.weight - old_weight
                    else:
                        self.weight = self._find_average()

                    self.subtrees = \
                        sorted(self.subtrees, key=lambda x: x.weight,
                               reverse=True)
                    return
        # new node.
        tree = SimplePrefixTree(self.weight_type)
        if prefix:
            tree.value = self.value + [prefix[0]]
            tree.insert(value, weight, prefix[1:])
            self.leaf += 1
            self.subtrees.append(tree)
        else:
            # leaf
            duplicate = False
            for t in self.subtrees:
                if t.value == [value]:
                    duplicate = True
                    t.weight += weight
            if not duplicate:
                tree.value = [value]
                tree.weight = weight
                self.leaf += 1
                self.subtrees.append(tree)
        self.subtrees = \
            sorted(self.subtrees, key=lambda x: x.weight, reverse=True)
        if self.weight_type == 'sum':
            self.weight += weight
        else:
            self.weight = self._find_average()

    def __len__(self) -> int:
        """ Return the number of values stored in this SimplePrefixTree.
        """
        return self.leaf

    def autocomplete(self, prefix: List, limit: Optional[int] = None)\
            -> List[Tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix."""
        # find target root first.
        root = self
        while prefix:
            found = False
            for s in root.subtrees:
                if root.value + [prefix[0]] == s.value:
                    root = s
                    prefix = prefix[1:]
                    found = True
                    break
            if not found:
                return []
        result = []

        def helper(r: SimplePrefixTree) -> None:
            """small helper to find leaf."""
            nonlocal limit
            if r.is_leaf():
                if limit:
                    limit -= 1
                result.append((r.value[0], r.weight))
            else:
                for t in r.subtrees:
                    if limit == 0:
                        return
                    helper(t)
        helper(root)
        return sorted(result, key=lambda x: x[1], reverse=True)

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
        """
        if not prefix:
            self.weight = 0
            self.subtrees = []
            self.value = []
            self.leaf = 0
        target = None
        for s in self.subtrees:
            if s.value == self.value + [prefix[0]]:
                old_leaf = s.leaf
                old_weight = s.weight
                s.remove(prefix[1:])
                target = s
                self.leaf += old_leaf - s.leaf
                if self.weight_type == 'sum':
                    self.weight -= old_weight - s.weight
                else:
                    self.weight = self._find_average()
                break
        if target and target.is_empty():
            self.subtrees.remove(target)


################################################################################
# CompressedPrefixTree (Task 6)
################################################################################
class CompressedPrefixTree(Autocompleter):
    """A compressed prefix tree implementation.

    While this class has the same public interface as SimplePrefixTree,
    (including the initializer!) this version follows the implementation
    described on Task 6 of the assignment handout, which reduces the number of
    tree objects used to store values in the tree.

    === Attributes ===
    value:
        The value stored at the root of this prefix tree, or [] if this
        prefix tree is empty.
    weight:
        The weight of this prefix tree. If this tree is a leaf, this attribute
        stores the weight of the value stored in the leaf. If this tree is
        not a leaf and non-empty, this attribute stores the *aggregate weight*
        of the leaf weights in this tree.
    subtrees:
        A list of subtrees of this prefix tree.

    === Representation invariants ===
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, this tree is a leaf.
        (self.value is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If len(self.subtrees) > 0, then self.value is a list (*common prefix*),
        and self.weight > 0 (*aggregate weight*).

    - **NEW**
      This tree does not contain any compressible internal values.
      (See the assignment handout for a definition of "compressible".)

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of their weights.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a `weight`
      attribute.
    """
    value: Any
    weight: float
    subtrees: List[CompressedPrefixTree]
    weight_type: str
    leaf: int

    def __init__(self, weight_type: str) -> None:
        """Initialize an empty simple prefix tree.

        Precondition: weight_type == 'sum' or weight_type == 'average'.

        The given <weight_type> value specifies how the aggregate weight
        of non-leaf trees should be calculated (see the assignment handout
        for details).
        """
        self.weight = 0.0
        self.value = []
        self.subtrees = []
        self.weight_type = weight_type
        self.leaf = 0

    def __len__(self) -> int:
        return self.leaf

    def _find_average(self) -> float:
        """ helper to calculate average weight."""
        sum_weight = 0
        for s in self.subtrees:
            if s.is_leaf():
                sum_weight += s.weight
            else:
                sum_weight += s.weight * s.leaf
        return sum_weight / self.leaf

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """ Insert the given value into this CompressedPrefixTree.
        """

        for t in self.subtrees:
            if not prefix:
                break
            compare = min(len(t.value), len(prefix))
            if t.value[:compare] == prefix[:compare]\
                    and t.value != prefix:
                old_weight, old_leaf = t.weight, t.leaf
                t.insert(value, weight, prefix)
                self.leaf += t.leaf - old_leaf
                if self.weight_type == 'sum':
                    self.weight += t.weight - old_weight
                else:
                    self.weight = self._find_average()
                self.subtrees = \
                    sorted(self.subtrees, key=lambda x: x.weight,
                           reverse=True)
                return
            same_index = 0
            for i in range(compare):
                if t.value[i] != prefix[i]:
                    break
                same_index += 1
            if same_index:
                if t.value == prefix:
                    t.insert(value, weight, [])
                else:
                    tree = CompressedPrefixTree(self.weight_type)
                    tree.value = t.value[:same_index]
                    tree.subtrees.append(t)
                    tree.insert(value, weight, prefix[same_index:])
                    tree.weight = weight + t.weight \
                        if self.weight_type == 'sum' \
                        else tree._find_average()
                    self.subtrees.remove(t)
                    self.subtrees.append(tree)
                    self.leaf += 1
                if self.weight_type == 'sum':
                    self.weight += weight
                else:
                    self.weight = self._find_average()
                self.subtrees = \
                    sorted(self.subtrees, key=lambda x: x.weight,
                           reverse=True)
                return
        # new node.
        tree = CompressedPrefixTree(self.weight_type)
        if prefix:
            tree.value = list(value)
            tree.insert(value, weight, [])
            self.leaf += 1
            self.subtrees.append(tree)
        else:
            # leaf
            duplicate = False
            for t in self.subtrees:
                if t.value == [value]:
                    duplicate = True
                    t.weight += weight
            if not duplicate:
                tree.value = [value]
                tree.weight = weight
                self.leaf += 1
                self.subtrees.append(tree)
        self.subtrees = \
            sorted(self.subtrees, key=lambda x: x.weight, reverse=True)
        if self.weight_type == 'sum':
            self.weight += weight
        else:
            self.weight = self._find_average()

    def autocomplete(self, prefix: List, limit: Optional[int] = None)\
            -> List[Tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix."""
        # find target root first.
        root = self
        while prefix:
            found = False
            for s in root.subtrees:
                compare = min(len(s.value), len(prefix))
                if s.value[:compare] == prefix[:compare]:
                    root = s
                    if compare == len(prefix):
                        prefix = []
                    found = True
                    break
            if not found:
                return []
        result = []

        def helper(r: CompressedPrefixTree) -> None:
            """small helper to find leaf."""
            nonlocal limit
            if r.is_leaf():
                if limit:
                    limit -= 1
                result.append((r.value[0], r.weight))
            else:
                for t in r.subtrees:
                    if limit == 0:
                        return
                    helper(t)

        helper(root)
        return sorted(result, key=lambda x: x[1], reverse=True)

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
        """
        if not prefix:
            self.weight = 0.0
            self.subtrees = []
            self.value = []
            self.leaf = 0
        target = None
        for s in self.subtrees:
            compare = min(len(s.value), len(prefix))
            if s.value[:compare] == prefix[:compare]:
                old_leaf = s.leaf
                old_weight = s.weight
                if compare == len(prefix):
                    s.remove([])
                else:
                    s.remove(prefix)
                target = s
                self.leaf += old_leaf - s.leaf
                if self.weight_type == 'sum':
                    self.weight -= old_weight - s.weight
                else:
                    self.weight = self._find_average()
                break
        if target is not None:
            if target.is_empty():
                self.subtrees.remove(target)
            elif len(target.subtrees) == 1:
                target.value = target.subtrees[0].value
                target.subtrees = target.subtrees[0].subtrees

    def is_leaf(self) -> bool:
        """Return whether this simple prefix tree is a leaf."""
        return self.weight > 0 and self.subtrees == []

    def __str__(self) -> str:
        """Return a string representation of this tree.

        You may find this method helpful for debugging.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + f'{self.value} ({self.weight})\n'
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    def is_empty(self) -> bool:
        """Return whether this simple prefix tree is empty."""
        return self.weight == 0.0

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-nested-blocks': 4
    })
