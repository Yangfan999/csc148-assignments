"""
The DictionaryStack class for ex3.
Do NOT change the __init__ method.
Part of the __str__ method has been provided for you.

You need to implement:
    - add
    - remove
    - is_empty
    - __str__
"""


class DictionaryStack:
    """
    A class representing a DictionaryStack.
    """

    def __init__(self) -> None:
        """
        Initialize this DictionaryStack.

        >>> d = DictionaryStack()
        >>> d.is_empty()
        True
        """
        self._content = {}
        self._next_index = 0

    def __str__(self) -> str:
        """
        Return a string representation of this Stack.

        >>> d = DictionaryStack()
        >>> d.add(3)
        >>> d.add("Apple")
        >>> print(d)
        3, Apple <- Top
        """
        list_to_return = []
        for i in range(self._next_index):
            list_to_return.append(str(self._content[i]))
        # TODO: Fill in the rest of the str
        # You should be adding the string version of each item in the stack
        # into the list.
        # They should be in the order they were added (i.e. oldest -> newest)
        # so the last item is the one we're removing last.

        return ", ".join(list_to_return) + " <- Top"

    def add(self, obj: object) -> None:
        """
        Add object to the stack.
        """
        self._content[self._next_index] = obj
        self._next_index += 1

    def remove(self) -> object:
        """
        Remove the item at the top and return it.
        """
        self._next_index -= 1
        return self._content.pop(self._next_index)

    def is_empty(self) -> bool:
        """
        Return True iff the stack is empty.
        """
        return self._next_index == 0


# ---- Everything below this is client code. Do NOT modify anything! ----
if __name__ == '__main__':
    d = DictionaryStack()

    # The format for assert is as follows:
    # assert <thing we want to check>, <error message>

    d.add(3)
    error_message = ("After adding 3 to the DictionaryStack, we " +
                     "expected False to be returned when " +
                     "we called d.is_empty but got {} " +
                     "instead").format(d.is_empty())
    assert not d.is_empty(), error_message

    removed_item = d.remove()
    error_message = ("After adding 3 to the DictionaryStack, we expected " +
                     "3 to be removed when we called d.remove() but got " +
                     "{} instead").format(removed_item)
    assert 3 == removed_item, error_message

    error_message = ("After adding 3 and removing it from the " +
                     "DictionaryStack, we expected True to be returned when " +
                     "we called d.is_empty but got {} " +
                     "instead").format(d.is_empty())
    assert d.is_empty(), error_message

    d.add(1)
    d.add("A")
    d.add(5)

    removed_item = d.remove()
    error_message = ("After adding 5 to the DictionaryStack, we expected " +
                     "5 to be removed when we called d.remove() but got " +
                     "{} instead").format(removed_item)
    assert 5 == removed_item, error_message

    expected_string = "1, A <- Top"
    error_message = ("A DictionaryStack that had 1 added to it and then " +
                     "'A' should return the string {} but got " +
                     "{} instead").format(expected_string, str(d))
    assert expected_string == str(d), error_message

    removed_item = d.remove()
    error_message = ("After removing from a stack containing 1 and 'A'," +
                     " we expected 'A' to be removed when we called " +
                     "d.remove() but we got {} instead").format(removed_item)
    assert 'A' == removed_item, error_message


    expected_string = "1 <- Top"
    error_message = ("A DictionaryStack that has 1 in it " +
                     "should return the string {} but got " +
                     "{} instead").format(expected_string, str(d))
    assert expected_string == str(d), error_message

    # Below is how python_ta (PythonTA/pyTA/etc.) is called.
    # When run, your code should produce no errors from python_ta.
    # You must have python_ta installed for this to work (see Lab 1 and
    # the Software Installation page).
    import python_ta
    python_ta.check_all(config="ex3_pyta.txt")
