"""
The Playstyle classes for A2.
Docstring examples are not required for Playstyles.

You are responsible for implementing the get_state_score function, as well as
creating classes for both Iterative Minimax and Recursive Minimax.
"""
from typing import Any
import random

class Playstyle:
    """
    The Playstyle superclass.

    is_manual - Whether the class is a manual Playstyle or not.
    battle_queue - The BattleQueue corresponding to the game this Playstyle is
                   being used in.
    """
    is_manual: bool
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this Playstyle with BattleQueue as its battle queue.
        """
        self.battle_queue = battle_queue
        self.is_manual = True

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        raise NotImplementedError

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Playstyle which uses the BattleQueue
        new_battle_queue.
        """
        raise NotImplementedError

class ManualPlaystyle(Playstyle):
    """
    The ManualPlaystyle. Inherits from Playstyle.
    """

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        parameter represents a key pressed by a player.

        Return 'X' if a valid move cannot be found.
        """
        if parameter in ['A', 'S']:
            return parameter

        return 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this ManualPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return ManualPlaystyle(new_battle_queue)

class RandomPlaystyle(Playstyle):
    """
    The Random playstyle. Inherits from Playstyle.
    """
    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RandomPlaystyle with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        actions = self.battle_queue.peek().get_available_actions()

        if not actions:
            return 'X'

        return random.choice(actions)

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this RandomPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return RandomPlaystyle(new_battle_queue)


def get_state_score(battle_queue: 'BattleQueue') -> int:
    """
    Return an int corresponding to the highest score that the next player in
    battle_queue can guarantee.

    For a state that's over, the score is the HP of the character who still has
    HP if the next player who was supposed to act is the winner. If the next
    player who was supposed to act is the loser, then the score is -1 * the
    HP of the character who still has HP. If there is no winner (i.e. there's
    a tie) then the score is 0.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> m = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = m
    >>> m.enemy = r
    >>> bq.add(r)
    >>> bq.add(m)
    >>> m.set_hp(3)
    >>> get_state_score(bq)
    100
    >>> r.set_hp(40)
    >>> get_state_score(bq)
    40
    >>> bq.remove()
    r (Rogue): 40/100
    >>> bq.add(r)
    >>> get_state_score(bq)
    -10
    """
    bq = battle_queue.copy()
    if bq.is_over():
        if not bq.get_winner():
            return 0
        if bq.peek() == bq.get_winner():
            return bq.get_winner().get_hp()
        return -1 * bq.get_winner().get_hp()
    best = []
    action = bq.peek().get_available_actions()
    for a in action:
        bq = battle_queue.copy()
        player = bq.remove()
        if a == 'S':
            player.special_attack()
        else:
            player.attack()
        if bq.peek() == player:
            best.append(get_state_score(bq))
        else:
            best.append(-1 * get_state_score(bq))
    return max(best)


class MinimaxRecPlaystyle(Playstyle):
    """
    The Minimax playstyle. Inherits from Playstyle.
    """
    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this MinimaxPlaystyle with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, MinimaxIterPlaystyle(bq))
        >>> m = Mage("m", bq, MinimaxIterPlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(1)
        >>> r.playstyle.select_attack()
        'A'
        """
        actions = self.battle_queue.peek().get_available_actions()

        if not actions:
            return 'X'

        best = []
        for a in actions:
            bq = self.battle_queue.copy()
            if a == 'S':
                bq.remove().special_attack()
            else:
                bq.remove().attack()
            if bq.peek() == self.battle_queue.peek():
                best.append(get_state_score(bq))
            else:
                best.append(-1 * get_state_score(bq))
        return actions[best.index(max(best))]

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this MinimaxPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return MinimaxRecPlaystyle(new_battle_queue)


class MinimaxIterPlaystyle(Playstyle):
    """
       The Minimax playstyle. Inherits from Playstyle.
       """

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this MinimaxIterPlaystyle with BattleQueue as
        its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False
        self.fake_stack = None
        self.states = None

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, MinimaxIterPlaystyle(bq))
        >>> m = Mage("m", bq, MinimaxIterPlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(1)
        >>> r.playstyle.select_attack()
        'A'
        """
        self.fake_stack = []
        self.states = []
        self.states.append(StateNode("X", self.battle_queue.peek(),
                                     self.battle_queue.peek().enemy,
                                     self.battle_queue))
        self.fake_stack.append(self.states[0])
        while self.fake_stack:
            state = self.fake_stack.pop()
            if state.bq.is_over():
                state.score = state.current.get_hp() \
                              - state.target.get_hp() \
                    if state.bq.get_winner() else 0
            else:
                if state.children:
                    state.score = self._calculate_score(state)
                else:
                    self.fake_stack.append(state)
                    for a in state.current.get_available_actions():
                        if a == 'A':
                            abq = state.bq.copy()
                            abq.remove().attack()
                            child_state = StateNode\
                                ("A", abq.peek(), abq.peek().enemy, abq)
                        else:
                            sbq = state.bq.copy()
                            sbq.remove().special_attack()
                            child_state = StateNode\
                                ("S", sbq.peek(), sbq.peek().enemy, sbq)
                        self.states.append(child_state)
                        state.add_child(child_state)
                        self.fake_stack.append(child_state)
        return self._find_action()

    def _find_action(self) -> str:
        """Helper to find action.
        """
        init = self.states[0]
        for c in init.children:
            if (c.current == init.current
                    and c.score == init.score) or \
                    (c.current != init.current and c.score == init.score * -1):
                return c.type
        return ""

    def _calculate_score(self, state: 'StateNode') -> int:
        """ Helper to calculate score.
        """

        score = None
        for c in state.children:
            sc = c.score
            if c.current.get_name() != state.current.get_name():
                sc *= -1
            if not score or sc > score:
                score = sc
        return score

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this MinimaxIterPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return MinimaxIterPlaystyle(new_battle_queue)


class StateNode:
    """ A state node class.
    """

    def __init__(self, atype: str, cplayer: 'Character',
                 tplayer: 'Character', bq: "BattleQueue") -> None:
        """ Init this state node.
        """
        self.type = atype
        self.bq = bq
        self.score = None
        self.children = None
        self.current = cplayer
        self.target = tplayer

    def add_child(self, state: 'StateNode') -> None:
        """ Add a child to this state.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, MinimaxIterPlaystyle(bq))
        >>> m = Mage("m", bq, MinimaxIterPlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> a = StateNode('S', r, m, bq)
        >>> a.add_child(StateNode('A', m, r, bq))
        >>> len(a.children)
        1
        """

        if not self.children:
            self.children = []
        self.children.append(state)

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
