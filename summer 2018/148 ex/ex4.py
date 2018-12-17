"""
Provided is a LinkedList and LinkedListNode class.

Implement the LinkedList method 'swap_front_back'.
"""

from typing import Union, Any


class LinkedListNode:
    """
    A Node to be used in a LinkedList.

    next_ - The successor to this LinkedListNode
    value - The data represented by this LinkedListNode.
    """
    next_: Union["LinkedListNode", None]
    value: object

    def __init__(self, value: object,
                 next_: Union["LinkedListNode", None] = None) -> None:
        """
        Initialize this LinkedListNode with the value value and successor next.

        >>> LinkedListNode(3).value
        3
        >>> LinkedListNode(3).next_ is None
        True
        """
        self.value = value
        self.next_ = next_

    def __str__(self) -> str:
        """
        Return a string representation of this LinkedListNode.

        >>> print(LinkedListNode(3))
        3 ->
        """
        return "{} -> ".format(self.value)


class LinkedList:
    """
    Collection of LinkedListNodes.

    front - first node of this LinkedList
    back - last node of this LinkedList
    size - the number of nodes in this LinkedList (>= 0)
    """
    front: Union[LinkedListNode, None]
    back: Union[LinkedListNode, None]
    size: int

    def __init__(self) -> None:
        """
        Initialize an empty LinkedList.

        >>> lnk = LinkedList()
        >>> lnk.size
        0
        """
        self.front = None
        self.back = None
        self.size = 0

    def prepend(self, value: Any) -> None:
        """
        Insert value to the start of this LinkedList (before self.front).

        >>> lnk = LinkedList()
        >>> lnk.prepend(0)
        >>> lnk.prepend(1)
        >>> print(lnk)
        1 -> 0 -> |
        """
        self.front = LinkedListNode(value, self.front)
        if self.back is None:
            self.back = self.front
        self.size += 1

    def __str__(self) -> str:
        """
        Return a string representation of this LinkedList.

        >>> lnk = LinkedList()
        >>> lnk.prepend(0)
        >>> lnk.prepend(1)
        >>> print(lnk)
        1 -> 0 -> |
        """
        cur_node = self.front
        result = ''
        while cur_node is not None:
            result += str(cur_node)
            cur_node = cur_node.next_
        return result + '|'

    def swap_front_back(self) -> None:
        """
        Swap the LinkedListNodes of the front and back of this linked list.

        Do not create any new LinkedListNodes.
        Do not swap the values of the LinkedListNodes.

        >>> lnk = LinkedList()
        >>> lnk.prepend(3)
        >>> lnk.prepend(2)
        >>> lnk.prepend(1)
        >>> print(lnk)
        1 -> 2 -> 3 -> |
        >>> front_id = id(lnk.front)
        >>> back_id = id(lnk.back)
        >>> lnk.swap_front_back()
        >>> print(lnk)
        3 -> 2 -> 1 -> |
        >>> front_id == id(lnk.back)
        True
        >>> back_id == id(lnk.front)
        True
        """
        temp = self.front
        prev = None
        while temp:
            nxt = temp.next_
            temp.next_ = prev
            prev = temp
            temp = nxt
        self.front, self.back = self.back, self.front


# Import the student solution
from ex4 import *
import unittest


class ExerciseTests(unittest.TestCase):
    def test_client_code(self):
        """
        Tests the client code to make sure the exercise passes it.
        """
        lnk = LinkedList()
        lnk.prepend(3)
        lnk.prepend(2)
        lnk.prepend(1)

        front_id = id(lnk.front)
        back_id = id(lnk.back)
        lnk.swap_front_back()

        self.assertEqual(str(lnk), "3 -> 2 -> 1 -> |")
        self.assertEqual(front_id, id(lnk.back))
        self.assertEqual(back_id, id(lnk.front))

        lnk2 = LinkedList()
        lnk2.prepend(2)
        lnk2.prepend(1)

        front_id2 = id(lnk2.front)
        back_id2 = id(lnk2.back)
        lnk2.swap_front_back()

        self.assertEqual(str(lnk2), "2 -> 1 -> |")
        self.assertEqual(front_id2, id(lnk2.back))
        self.assertEqual(back_id2, id(lnk2.front))

    def test_hidden(self):
        """
        The hidden test for students.
        """
        # Swap with a linkedlist with 5 items
        lnk = LinkedList()
        lnk.prepend(5)
        lnk.prepend(4)
        lnk.prepend(3)
        lnk.prepend(2)
        lnk.prepend(1)

        front_id = id(lnk.front)
        back_id = id(lnk.back)
        lnk.swap_front_back()

        self.assertEqual(str(lnk), "5 -> 2 -> 3 -> 4 -> 1 -> |")
        self.assertEqual(front_id, id(lnk.back))
        self.assertEqual(back_id, id(lnk.front))

        # Swap with an empty linkedlist
        lnk2 = LinkedList()
        lnk2.swap_front_back()

        self.assertEqual(str(lnk2), "|")

        # Swap with a linkedlist with duplicate elements in it
        lnk3 = LinkedList()
        lnk3.prepend(3)
        lnk3.prepend(4)
        lnk3.prepend(3)
        lnk3.prepend(2)
        lnk3.prepend(1)

        front_id3 = id(lnk3.front)
        back_id3 = id(lnk3.back)
        lnk3.swap_front_back()

        self.assertEqual(str(lnk3), "3 -> 2 -> 3 -> 4 -> 1 -> |")
        self.assertEqual(front_id3, id(lnk3.back))
        self.assertEqual(back_id3, id(lnk3.front))


if __name__ == "__main__":
    unittest.main(exit=False)
