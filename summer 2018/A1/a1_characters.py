"""
The characters classes for A1.
"""
from typing import List


class Character:
    """
    The character super class.
    """
    _hp: int
    _sp: int
    _name: str
    playstyle: 'Playstyle'
    _battleQueue: 'BattleQueue'
    _animation_state: int
    _character: str
    _defense: int
    _skill: int
    _attack: int
    enemy: 'Character'

    def __init__(self, name: str, playstyle: 'Playstyle',
                 battle_queue: 'BattleQueue', character: str):
        """
        Initialize this character.
        """
        self._hp = 100
        self._sp = 100
        self._name = name
        self.playstyle = playstyle
        self._battle_queue = battle_queue
        self.enemy = None
        self._defense = 0
        self._skill = 0
        self._attack = 0
        self._animation_state = 0
        self._character = character

    def set_defense(self, defense: int):
        """
        Set the defense this character has.
        """
        self._defense = defense

    def set_skill(self, skill: int):
        """
        Set the SP needed to use a special skill.
        """
        self._skill = skill

    def set_attack(self, attack: int):
        """
        Set the SP needed to use a basic attack.
        """
        self._attack = attack

    def get_hp(self) -> int:
        """
        Getter for hp.
        """
        return self._hp

    def get_sp(self) -> int:
        """
        Getter for sp.
        """
        return self._sp

    def get_name(self) -> str:
        """
        Getter for name.
        """
        return self._name

    def attack(self) -> None:
        """
        Perform a basic attack.
        """
        raise NotImplementedError

    def special_attack(self) -> None:
        """
        Perform a special skill.
        """
        raise NotImplementedError

    def taken_damage(self, taken: int) -> None:
        """
        Take care of under attack.

        >>> from A1.a1_battle_queue import *
        >>> bq = BattleQueue()
        >>> from A1.a1_playstyle import *
        >>> ps = ManualPlaystyle(bq)
        >>> r = Rogue('xx', bq, ps)
        >>> m = Mage('xxxx', bq, ps)
        >>> r.enemy = m
        >>> m.get_hp()
        100
        >>> r.attack()
        >>> m.get_hp()
        93
        """
        self._hp -= (taken - self._defense)
        if self._hp <= 0:
            self._hp = 0

    def is_valid_action(self, action: str) -> bool:
        """
        Check if this action is valid.

        >>> from A1.a1_battle_queue import *
        >>> bq = BattleQueue()
        >>> from A1.a1_playstyle import *
        >>> ps = ManualPlaystyle(bq)
        >>> r = Rogue('xx', bq, ps)
        >>> r.is_valid_action('A')
        True
        >>> r.is_valid_action('X')
        False
        """
        return action in self.get_available_actions()

    def get_next_sprite(self) -> str:
        """
        Return next sprite to be drawn.

        >>> from A1.a1_battle_queue import *
        >>> bq = BattleQueue()
        >>> from A1.a1_playstyle import *
        >>> ps = ManualPlaystyle(bq)
        >>> r = Rogue('xx', bq, ps)
        >>> m = Mage('xxxx', bq, ps)
        >>> r.enemy = m
        >>> r.get_next_sprite()
        'rogue_idle_0'
        >>> r.attack()
        >>> r.get_next_sprite()
        'rogue_attack_0'
        """
        if 0 <= self._animation_state <= 9:
            action = "_idle_"
        elif 10 <= self._animation_state <= 19:
            action = "_attack_"
        else:
            action = "_special_"
        sprite = self._character + action + str(self._animation_state % 10)
        if (self._animation_state + 1) % 10 == 0:
            self._animation_state = 0
        else:
            self._animation_state += 1
        return sprite

    def get_available_actions(self) -> List[str]:
        """
        Return available actions.

        >>> from A1.a1_battle_queue import *
        >>> bq = BattleQueue()
        >>> from A1.a1_playstyle import *
        >>> ps = ManualPlaystyle(bq)
        >>> r = Rogue('xx', bq, ps)
        >>> r.get_available_actions()
        ['S', 'A']
        """
        actions = []
        if self._sp >= self._skill:
            actions.append("S")
        if self._sp >= self._attack:
            actions.append("A")
        return actions

    def __repr__(self) -> str:
        """
        Return a string representation of this Character.

        >>> from A1.a1_battle_queue import *
        >>> bq = BattleQueue()
        >>> from A1.a1_playstyle import *
        >>> ps = ManualPlaystyle(bq)
        >>> r = Rogue('xx', bq, ps)
        >>> r
        xx (Rogue): 100/100
        """
        return "{} ({}): {}/{}"\
            .format(self._name, self._character.title(), self._hp, self._sp)


class Rogue(Character):
    """
    The Rogue. Inherits from Character.
    """

    def __init__(self, name: str, battle_queue: 'BattleQueue',
                 playstyle: 'Playstyle'):
        """
        Initialize this Rogue.
        """
        super().__init__(name, playstyle, battle_queue, "rogue")
        super().set_defense(10)
        super().set_attack(3)
        super().set_skill(10)

    def attack(self) -> None:
        """
         Perform basic attack of Rogue.

        >>> from A1.a1_battle_queue import *
        >>> bq = BattleQueue()
        >>> from A1.a1_playstyle import *
        >>> ps = ManualPlaystyle(bq)
        >>> r = Rogue('xx', bq, ps)
        >>> m = Mage('xxxx', bq, ps)
        >>> r.enemy = m
        >>> r.attack()
        >>> m.get_hp()
        93
        >>> r.get_sp()
        97
        >>> r.get_next_sprite()
        'rogue_attack_0'
        """
        self.enemy.taken_damage(15)
        self._battle_queue.add(self)
        self._sp -= self._attack
        self._animation_state = 10

    def special_attack(self) -> None:
        """
         Perform special skill of rogue.

        >>> from A1.a1_battle_queue import *
        >>> bq = BattleQueue()
        >>> from A1.a1_playstyle import *
        >>> ps = ManualPlaystyle(bq)
        >>> r = Rogue('xx', bq, ps)
        >>> m = Mage('xxxx', bq, ps)
        >>> r.enemy = m
        >>> r.special_attack()
        >>> m.get_hp()
        88
        >>> r.get_sp()
        90
        >>> r.get_next_sprite()
        'rogue_special_0'
        """
        self.enemy.taken_damage(20)
        self._battle_queue.add(self)
        self._battle_queue.add(self)
        self._sp -= self._skill
        self._animation_state = 20


class Mage(Character):
    """
    The Mage class. Inherits from Character.
    """

    def __init__(self, name: str, battle_queue: 'BattleQueue',
                 playstyle: 'Playstyle'):
        """
        Initialize this Mage.
        """
        super().__init__(name, playstyle, battle_queue, "mage")
        super().set_defense(8)
        super().set_attack(5)
        super().set_skill(30)

    def attack(self) -> None:
        """
        Perform basic attack of Mage.

        >>> from A1.a1_battle_queue import *
        >>> bq = BattleQueue()
        >>> from A1.a1_playstyle import *
        >>> ps = ManualPlaystyle(bq)
        >>> r = Rogue('xx', bq, ps)
        >>> m = Mage('xxxx', bq, ps)
        >>> m.enemy = r
        >>> m.attack()
        >>> r.get_hp()
        90
        >>> m.get_sp()
        95
        >>> m.get_next_sprite()
        'mage_attack_0'
        """
        self.enemy.taken_damage(20)
        self._battle_queue.add(self)
        self._sp -= self._attack
        self._animation_state = 10

    def special_attack(self) -> None:
        """
        Perform special skill of Mage.

        >>> from A1.a1_battle_queue import *
        >>> bq = BattleQueue()
        >>> from A1.a1_playstyle import *
        >>> ps = ManualPlaystyle(bq)
        >>> r = Rogue('xx', bq, ps)
        >>> m = Mage('xxxx', bq, ps)
        >>> m.enemy = r
        >>> m.special_attack()
        >>> r.get_hp()
        70
        >>> m.get_sp()
        70
        >>> m.get_next_sprite()
        'mage_special_0'
        """
        self.enemy.taken_damage(40)
        self._battle_queue.add(self.enemy)
        self._battle_queue.add(self)
        self._sp -= self._skill
        self._animation_state = 20


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a1_pyta.txt')
    import doctest
    doctest.testmod()
