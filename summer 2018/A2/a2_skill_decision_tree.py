"""
The SkillDecisionTree class for A2.

You are to implement the pick_skill() method in SkillDecisionTree, as well as
implement create_default_tree() such that it returns the example tree used in
a2.pdf.

This tree will be used during the gameplay of a2_game, but we may test your
SkillDecisionTree with other examples.
"""
from typing import Callable, List
from a2_skills import MageAttack, MageSpecial, RogueAttack, RogueSpecial


class SkillDecisionTree:
    """
    A class representing the SkillDecisionTree used by Sorcerer's in A2.

    value - the skill that this SkillDecisionTree contains.
    condition - the function that this SkillDecisionTree will check.
    priority - the priority number of this SkillDecisionTree.
               You may assume priority numbers are unique (i.e. no two
               SkillDecisionTrees will have the same number.)
    children - the subtrees of this SkillDecisionTree.
    """
    value: 'Skill'
    condition: Callable[['Character', 'Character'], bool]
    priority: int
    children: List['SkillDecisionTree']

    def __init__(self, value: 'Skill',
                 condition: Callable[['Character', 'Character'], bool],
                 priority: int,
                 children: List['SkillDecisionTree'] = None) -> None:
        """
        Initialize this SkillDecisionTree with the value value, condition
        function condition, priority number priority, and the children in
        children, if provided.

        >>> from a2_skills import MageAttack
        >>> def f(caster, target):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> t.priority
        1
        >>> type(t.value) == MageAttack
        True
        """
        self.value = value
        self.condition = condition
        self.priority = priority
        self.children = children[:] if children else []

    def pick_skill(self, caster: 'Character', target: 'Character') -> 'Skill':
        """ Return a skill for Sorcerer to use.

        >>> from a2_skills import MageAttack
        >>> def f(caster, target):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> bq = BattleQueue()
        >>> from a2_characters import Sorcerer
        >>> c = Sorcerer("r", bq, ManualPlaystyle(bq))
        >>> c2 = Sorcerer("r2", bq, ManualPlaystyle(bq))
        >>> type(t.pick_skill(c, c2)) == MageAttack
        True
        """

        def helper(tree: SkillDecisionTree,
                   caster: 'Character', target: 'Character') -> [int, '']:
            """ Little helper for pick_skill.
            """
            if not (tree.children and tree.condition(caster, target)):
                return [tree.priority, tree.value]
            lst = []
            for t in tree.children:
                lst.append(helper(t, caster, target))
            return sorted(lst, key=lambda k: k[0])[0]

        return helper(self, caster, target)[1]


def create_default_tree() -> SkillDecisionTree:
    """
    Return a SkillDecisionTree that matches the one described in a2.pdf.

    >>> t = create_default_tree()
    >>> type(t.value) == MageAttack
    True
    >>> len(t.children)
    3
    """
    root = SkillDecisionTree(MageAttack(), lambda c, t: c.get_hp() > 50, 5)
    root.children = \
        [SkillDecisionTree(MageAttack(),
                           lambda c, t: c.get_sp() > 20, 3,
                           [SkillDecisionTree
                            (RogueSpecial(),
                             lambda c, t: t.get_hp() < 30, 4,
                             [SkillDecisionTree
                              (RogueAttack(),
                               lambda c, t: False, 6)])]),
         SkillDecisionTree(MageSpecial(),
                           lambda c, t: t.get_sp() > 40, 2,
                           [SkillDecisionTree(RogueAttack(),
                                              lambda c, t: False, 8)]),
         SkillDecisionTree(RogueAttack(),
                           lambda c, t: c.get_hp() > 90, 1,
                           [SkillDecisionTree(RogueSpecial(),
                                              lambda c, t: False, 7)])]
    return root


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config='a2_pyta.txt')
