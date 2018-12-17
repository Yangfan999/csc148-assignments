"""
The Character classes for A2.

See a2_skills for how skills are handled.
Character, Mage, and Rogue have all been provided to you, with full
documentation.

You are responsible for creating classes for the Vampire and Sorcerer outlined
in a2.pdf, as well as writing all documentation for them.

Sorcerers must have a method called set_skill_decision_tree which takes in
a SkillDecisionTree to be used whenever the Sorcerer attacks.
"""
from typing import List
from a2_skills import MageAttack, MageSpecial, RogueAttack, RogueSpecial,\
    VampireAttack, VampireSpecial, SorcererAttack, SorcererSpecial

class Character:
    """
    An abstract superclass for all Characters.

    battle_queue - the BattleQueue that this Character will add to.
    playstyle - the Playstyle that this Character uses to pick actions.
    enemy - the Character that this Character attacks.
    """
    battle_queue: 'BattleQueue'
    playstyle: 'Playstyle'

    def __init__(self, name: str, bq: 'BattleQueue', ps: 'Playstyle') -> None:
        """
        Initialize this Character with the name name, battle_queue bq, and
        playstyle ps.
        """
        self._name = name
        self.battle_queue = bq
        self.playstyle = ps
        self._hp = 100
        self._sp = 100
        self._defense = 0
        self.enemy = None

        self._character_type = ''
        self._current_state = 'idle'
        self._current_frame = 0

        self._skills = {'A': None,
                        'S': None
                       }

    def get_name(self) -> str:
        """
        Return the name of this Character.
        """
        return self._name

    def get_hp(self) -> int:
        """
        Return the HP of this Character.
        """
        return self._hp

    def get_sp(self) -> int:
        """
        Return the SP of this Character.
        """
        return self._sp

    def get_next_sprite(self) -> str:
        """
        Return the next sprite that needs to be drawn for this Character.
        """
        sprite_to_return = "{}_{}_{}".format(self._character_type,
                                             self._current_state,
                                             self._current_frame)

        self._current_frame += 1

        if self._current_frame == 10:
            self._current_state = 'idle'
            self._current_frame = 0

        return sprite_to_return

    def get_available_actions(self) -> List[str]:
        """
        Return a list of all actions that this Character can perform.
        'A' means that the character can attack().
        'S' means that the character can special_attack().
        """
        available = []

        for skill in self._skills:
            if self.is_valid_action(skill):
                available.append(skill)

        return available


    def is_valid_action(self, action: str) -> bool:
        """
        Return True if the character can perform the skill corresponding to
        action.
        'A' corresponds to whether the character can use attack().
        'S' corresponds to whether the character can use special_attack().
        """
        if action in self._skills:
            return self._skills[action].get_sp_cost() <= self._sp

        return False

    def attack(self) -> None:
        """
        Perform an attack on this Character's enemy.
        """
        self._current_state = 'attack'
        self._current_frame = 0
        self._skills['A'].use(self, self.enemy)

    def special_attack(self) -> None:
        """
        Perform a special attack on this Character's enemy.
        """
        self._current_state = 'special'
        self._current_frame = 0
        self._skills['S'].use(self, self.enemy)

    def reduce_sp(self, cost: int) -> None:
        """
        Reduce this Character's SP by cost.
        """
        self._sp -= cost

    def apply_damage(self, damage: int) -> None:
        """
        Reduce this Character's HP by damage modified by this Character's
        defense.
        """
        damage -= self._defense
        self._hp -= damage
        self._hp = max(self._hp, 0)

    def set_sp(self, new_sp: int) -> None:
        """
        Sets this Character's SP to new_sp.
        """
        self._sp = new_sp

    def set_hp(self, new_hp: int) -> None:
        """
        Sets this Character's HP to new_hp.
        """
        self._hp = new_hp

    def __repr__(self):
        """
        Return a representation of this Character in the format:
        name (Type): HP/SP
        """
        class_name = self._character_type[0].upper() + self._character_type[1:]

        return "{} ({}): {}/{}".format(self._name, class_name, self._hp,
                                       self._sp)

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Character':
        """
        Return a copy of this Character whose BattleQueue is new_battle_queue.
        """
        raise NotImplementedError

    def _set_copy_attributes(self, other: 'Character') -> None:
        """
        Set other's attributes to match this Character's.
        """
        other.set_hp(self._hp)
        other.set_sp(self._sp)

class Mage(Character):
    """
    A class representing a Mage.

    battle_queue - the BattleQueue that this Mage will add to.
    playstyle - the Playstyle that this Mage uses to pick actions.
    enemy - the Mage that this Mage attacks.
    """
    battle_queue: 'BattleQueue'
    playstyle: 'Playstyle'

    def __init__(self, name: str, bq: 'BattleQueue', ps: 'Playstyle') -> None:
        """
        Initialize this Mage with the name name, battle_queue bq, and
        playstyle ps.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> bq = BattleQueue()
        >>> c = Mage("m", bq, ManualPlaystyle(bq))
        >>> c2 = Mage("m2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> c
        m (Mage): 100/100
        """
        super().__init__(name, bq, ps)
        self._character_type = 'mage'
        self._skills['A'] = MageAttack()
        self._skills['S'] = MageSpecial()
        self._defense = 8

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Mage':
        """
        Return a copy of this Mage whose BattleQueue is new_battle_queue.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> bq = BattleQueue()
        >>> c = Mage("m", bq, ManualPlaystyle(bq))
        >>> c2 = Mage("m2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> c
        m (Mage): 100/100
        >>> new_bq = BattleQueue()
        >>> c_copy = c.copy(new_bq)
        >>> c2_copy = c2.copy(new_bq)
        >>> c_copy.enemy = c2_copy
        >>> c2_copy.enemy = c_copy
        >>> c_copy.attack()
        >>> c
        m (Mage): 100/100
        >>> c_copy
        m (Mage): 100/95
        >>> c2
        m2 (Mage): 100/100
        >>> c2_copy
        m2 (Mage): 88/100
        """
        copy = Mage(self._name, new_battle_queue,
                    self.playstyle.copy(new_battle_queue))
        self._set_copy_attributes(copy)
        return copy

class Rogue(Character):
    """
    A class representing a Rogue.

    battle_queue - the BattleQueue that this Rogue will add to.
    playstyle - the Playstyle that this Rogue uses to pick actions.
    enemy - the Rogue that this Rogue attacks.
    """
    battle_queue: 'BattleQueue'
    playstyle: 'Playstyle'

    def __init__(self, name: str, bq: 'BattleQueue', ps: 'Playstyle') -> None:
        """
        Initialize this Rogue with the name name, battle_queue bq, and
        playstyle ps.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> bq = BattleQueue()
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> c
        r (Rogue): 100/100
        """
        super().__init__(name, bq, ps)
        self._character_type = 'rogue'
        self._skills['A'] = RogueAttack()
        self._skills['S'] = RogueSpecial()
        self._defense = 10

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Rogue':
        """
        Return a copy of this Rogue whose BattleQueue is new_battle_queue.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> bq = BattleQueue()
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> c
        r (Rogue): 100/100
        >>> new_bq = BattleQueue()
        >>> c_copy = c.copy(new_bq)
        >>> c2_copy = c2.copy(new_bq)
        >>> c_copy.enemy = c2_copy
        >>> c2_copy.enemy = c_copy
        >>> c_copy.attack()
        >>> c
        r (Rogue): 100/100
        >>> c_copy
        r (Rogue): 100/97
        >>> c2
        r2 (Rogue): 100/100
        >>> c2_copy
        r2 (Rogue): 95/100
        """
        copy = Rogue(self._name, new_battle_queue,
                     self.playstyle.copy(new_battle_queue))
        self._set_copy_attributes(copy)
        return copy


class Vampire(Character):
    """
    An subclass of Character representing Vampire.

    battle_queue - the BattleQueue that this Character will add to.
    playstyle - the Playstyle that this Character uses to pick actions.
    enemy - the Character that this Character attacks.
    """

    battle_queue: 'BattleQueue'
    playstyle: 'Playstyle'

    def __init__(self, name: str, bq: 'BattleQueue', ps: 'Playstyle') -> None:
        """
        Initialize this Vampire with the name name, battle_queue bq, and
        playstyle ps.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> bq = BattleQueue()
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> c
        r (Rogue): 100/100
        """
        super().__init__(name, bq, ps)
        self._character_type = 'vampire'
        self._skills['A'] = VampireAttack()
        self._skills['S'] = VampireSpecial()
        self._defense = 3

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Vampire':
        """
        Return a copy of this Rogue whose BattleQueue is new_battle_queue.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> bq = BattleQueue()
        >>> c = Vampire("r", bq, ManualPlaystyle(bq))
        >>> c2 = Vampire("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> c
        r (Vampire): 100/100
        >>> new_bq = BattleQueue()
        >>> c_copy = c.copy(new_bq)
        >>> c2_copy = c2.copy(new_bq)
        >>> c_copy.enemy = c2_copy
        >>> c2_copy.enemy = c_copy
        >>> c_copy.attack()
        >>> c
        r (Vampire): 100/100
        >>> c_copy
        r (Vampire): 117/85
        >>> c2
        r2 (Vampire): 100/100
        >>> c2_copy
        r2 (Vampire): 83/100
        """
        copy = Vampire(self._name, new_battle_queue,
                       self.playstyle.copy(new_battle_queue))
        self._set_copy_attributes(copy)
        return copy


class Sorcerer(Character):
    """
    An subclass of Character representing Vampire.

    battle_queue - the BattleQueue that this Character will add to.
    playstyle - the Playstyle that this Character uses to pick actions.
    enemy - the Character that this Character attacks.
    """

    def __init__(self, name: str, bq: 'BattleQueue', ps: 'Playstyle') -> None:
        """
        Initialize this Vampire with the name name, battle_queue bq, and
        playstyle ps.

        """
        super().__init__(name, bq, ps)
        self._character_type = 'sorcerer'
        self._skills['A'] = SorcererAttack()
        self._skills['S'] = SorcererSpecial()
        self._defense = 10
        self.skill_decision_tree = None

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Sorcerer':
        """
        Return a copy of this Rogue whose BattleQueue is new_battle_queue.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> bq = BattleQueue()
        >>> c = Sorcerer("r", bq, ManualPlaystyle(bq))
        >>> c2 = Sorcerer("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> c
        r (Sorcerer): 100/100
        >>> new_bq = BattleQueue()
        >>> c_copy = c.copy(new_bq)
        >>> c2_copy = c2.copy(new_bq)
        >>> c_copy.enemy = c2_copy
        >>> c2_copy.enemy = c_copy
        >>> c
        r (Sorcerer): 100/100
        >>> c_copy
        r (Sorcerer): 100/100
        >>> c2
        r2 (Sorcerer): 100/100
        >>> c2_copy
        r2 (Sorcerer): 100/100
        """
        copy = Sorcerer(self._name, new_battle_queue,
                        self.playstyle.copy(new_battle_queue))
        self._set_copy_attributes(copy)
        return copy

    def set_skill_decision_tree(self, tree: 'SkillDecisionTree') -> None:
        """ Setter for decision tree.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_skill_decision_tree import SkillDecisionTree
        >>> from a2_skills import MageAttack
        >>> def f(caster, target):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> bq = BattleQueue()
        >>> c = Sorcerer("r", bq, ManualPlaystyle(bq))
        >>> c.set_skill_decision_tree(t)
        >>> c.skill_decision_tree == t
        True
        """

        self.skill_decision_tree = tree


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
