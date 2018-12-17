"""
Implement the get_all_evens() method below.
"""

from typing import Union, List


def get_all_evens(x: Union[list, int]) -> List[int]:
    """
    Return a list of all of the even ints in x or in any sublists within x.

    Order doesn't matter.
    """
    if isinstance(x, int):
        if x % 2 == 0:
            return [x]
        return []
    result = []
    for i in x:
        result.extend(get_all_evens(i))
    return result


if __name__ == '__main__':
    single_int = 1
    assert get_all_evens(single_int) == []

    lst = [1, 2, 3, 4]
    assert sorted(get_all_evens(lst)) == [2, 4]

    nested_lst = [1, [2, 3, [4]], [[4], 6]]
    assert sorted(get_all_evens(nested_lst)) == [2, 4, 4, 6]

    import python_ta
    python_ta.check_all(config="ex5_pyta.txt")
