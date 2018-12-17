"""
The BattleQueue class for A1.

A BattleQueue is a _queue that lets our game know in what order various
characters are going to attack. The method headers and descriptions have all
been provided for you, but the implementation will depend on you.

You must replace the 'Any's in the type annotations as well as add in
the constructors for the docstring examples.
"""
# To put a class name without importing it, just wrap the name in ''s.
# For example:
# add(self, character: 'Something') -> None:
#
# If there are multiple return types, import Union and use that. For example:
# Union[str, bool]
from typing import Union, List


class BattleQueue:
    """
    A class representing a BattleQueue.
    """

    _queue: List['Character']

    def __init__(self):
        """
        Initialize this BattleQueue.

        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._queue = []

    def add(self, character: 'Character') -> None:
        """
        Add character to this BattleQueue.

        >>> bq = BattleQueue()
        >>> from A1.a1_playstyle import ManualPlaystyle
        >>> ps = ManualPlaystyle(bq)
        >>> from A1.a1_characters import Mage
        >>> c = Mage('xixi', bq, ps)
        >>> bq.add(c)
        >>> bq.is_empty()
        False
        """
        self._queue.append(character)

    def remove(self) -> Union['Character', None]:
        """
        Remove and return the character at the front of this BattleQueue.

        >>> bq = BattleQueue()
        >>> from A1.a1_playstyle import ManualPlaystyle
        >>> ps = ManualPlaystyle(bq)
        >>> from A1.a1_characters import Rogue
        >>> c = Rogue('Sophia', bq, ps)
        >>> bq.add(c)
        >>> bq.remove()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        True
        """
        for i in range(len(self._queue)):
            if self._queue[i].get_available_actions():
                return self._queue.pop(i)
        return None

    def is_empty(self) -> bool:
        """
        Return whether this BattleQueue is empty (i.e. has no players or
        has no players that can perform any actions).

        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        return len(self._queue) == 0 or all(
            [len(c.get_available_actions()) == 0 for c in self._queue])

    def peek(self) -> Union['Character', None]:
        """
        Return the character at the front of this BattleQueue but does not
        remove them.

        >>> bq = BattleQueue()
        >>> from A1.a1_playstyle import ManualPlaystyle
        >>> ps = ManualPlaystyle(bq)
        >>> from A1.a1_characters import Rogue
        >>> c = Rogue('Sophia', bq, ps)
        >>> bq.add(c)
        >>> bq.peek()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        False
        """
        for c in self._queue:
            if c.get_available_actions():
                return c
        return None

    def is_over(self) -> bool:
        """
        Return whether the game being carried out in this BattleQueue is over
        or not.

        A game is considered over if:
            - Both players have no skills that they can use.
            - One player has 0 _hp
            or
            - The BattleQueue is empty.

        >>> bq = BattleQueue()
        >>> bq.is_over()
        True

        >>> from A1.a1_playstyle import ManualPlaystyle
        >>> ps = ManualPlaystyle(bq)
        >>> from A1.a1_characters import Rogue
        >>> c = Rogue('Sophia', bq, ps)
        >>> bq.add(c)
        >>> bq.is_over()
        False
        """
        return self.is_empty() or any([c.get_hp() == 0 for c in self._queue])

    def get_winner(self) -> Union['Character', None]:
        """
        Return the winner of the game being carried out in this BattleQueue
        if the game is over. If the game is not over or if there is no winner
        (i.e. there's a tie), return None.

        >>> bq = BattleQueue()
        >>> bq.get_winner()
        """
        if self.is_over():
            for c in self._queue:
                if c.get_hp() != 0 and c.enemy.get_hp() == 0:
                    return c
        return None


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a1_pyta.txt')
