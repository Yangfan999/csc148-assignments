"""
Basic Unittests for your implementation of SkillDecisionTree for A2.

Passing these tests ensures that our test scripts can run on your code, and will
determine a portion of your mark (see Grading Scheme).

Passing these tests does NOT mean your code is flawless. These tests just
check for all of the basic functionality, without searching too deeply for logic
errors.

Try playing your game through multiple times and trying various combinations of
actions.
"""
import unittest

# Import the student solution
from a2_game import CHARACTER_CLASSES
from a2_playstyle import ManualPlaystyle
from a2_battle_queue import BattleQueue
from a2_skill_decision_tree import SkillDecisionTree, create_default_tree
from a2_skills import MageAttack, RogueAttack, MageSpecial
from a2_characters import Rogue

class SkillDecisionTreeUnitTests(unittest.TestCase):
    def create_basic_tree(self):
        """
        Creates a very basic SkillDecisionTree.
        """
        def caster_hp_lt_20(caster, _):
            """
            Return True if the caster's HP is < 20
            """
            return caster.get_hp() < 20

        priority_1 = SkillDecisionTree(MageAttack(), caster_hp_lt_20, 1)

        def target_hp_lt_20(_, target):
            """
            Return True if the target's HP is < 20
            """
            return target.get_hp() < 20

        priority_2 = SkillDecisionTree(RogueAttack(), target_hp_lt_20, 2)

        def caster_sp_gt_20(caster, _):
            """
            Return True if the caster's SP is > 20
            """
            return caster.get_sp() > 20

        priority_3 = SkillDecisionTree(MageSpecial(), caster_sp_gt_20, 3,
                                       [priority_2, priority_1])
        return priority_3

    def setUp(self):
        """
        Sets up 2 SkillDecisionTrees for use in the test cases.
        """
        self.default_tree = create_default_tree()

        self.basic_tree = self.create_basic_tree()

        lines = ["                [3, Caster SP > 20, MageSpecial]",
                 "                    /                    \\",
                 "[2, Target HP < 20, RogueAttack]    [1, Caster HP < 20, MageAttack]"]
        self.basic_tree_format = "\n".join(lines)

        bq = BattleQueue()

        self.caster = Rogue("Caster", bq, ManualPlaystyle(bq))
        self.target = Rogue("Target", bq, ManualPlaystyle(bq))

    def tearDown(self):
        """
        Delete the attributes that were created in setUp.
        """
        del self.default_tree
        del self.basic_tree

    def test_default_has_correct_priorities(self):
        """
        Test whether the default tree has the correct priorities or not.
        """
        expected_order = [5, 3, 2, 1, 4, 8, 7, 6]
        actual_order = []
        q = [self.default_tree]

        # Do a level-order traversal of the SkillDecisionTree
        while q != []:
            current = q.pop(0)
            actual_order.append(current.priority)
            for child in current.children:
                q.append(child)

        self.assertEqual(expected_order, actual_order,
                         ("Doing a level-order traversal of the Tree returned" +
                          " by calling create_default_tree() should return " +
                          "the priorities in the order {} " +
                          "but got {} instead.").format(expected_order,
                                                        actual_order))

    def test_default_has_correct_skills(self):
        """
        Test whether the default tree has the correct priorities or not.
        """
        expected_order = ['MageAttack', 'MageAttack', 'MageSpecial',
                          'RogueAttack', 'RogueSpecial', 'RogueAttack',
                          'RogueSpecial', 'RogueAttack']
        actual_order = []
        q = [self.default_tree]

        # Do a level-order traversal of the SkillDecisionTree
        while q != []:
            current = q.pop(0)
            actual_order.append(type(current.value).__name__)
            for child in current.children:
                q.append(child)

        self.assertEqual(expected_order, actual_order,
                         ("Doing a level-order traversal of the Tree returned" +
                          " by calling create_default_tree() should return " +
                          "the skills in the order {} " +
                          "but got {} instead.").format(expected_order,
                                                        actual_order))

    def test_basic_tree_gets_root(self):
        """
        Test to make sure we can get the root when using our basic tree.
        """
        self.caster.set_sp(15)
        actual = type(self.basic_tree.pick_skill(self.caster, self.target)).__name__
        expected = 'MageSpecial'

        self.assertEqual(expected, actual,
                         ("When calling pick_skill on a SkillDecisionTree " +
                          "that looks like:\n{}\nWith the characters:\n{}\n{}" +
                          "\nExpected to get the skill {} back but got " +
                          "{} instead.").format(self.basic_tree_format,
                                                self.caster,
                                                self.target,
                                                expected,
                                                actual))

    def test_basic_tree_gets_highest_priority_leaf(self):
        """
        Test to make sure we can get the root when using our basic tree.
        """
        actual = type(self.basic_tree.pick_skill(self.caster, self.target)).__name__
        expected = 'MageAttack'

        self.assertEqual(expected, actual,
                         ("When calling pick_skill on a SkillDecisionTree " +
                          "that looks like:\n{}\nWith the characters:\n{}\n{}" +
                          "\nExpected to get the skill {} back but got " +
                          "{} instead.").format(self.basic_tree_format,
                                                self.caster,
                                                self.target,
                                                expected,
                                                actual))

    def test_default_tree_matches_scenario_1(self):
        """
        Test to make sure the default tree works as expected for the scenario
        described in the handout.
        """
        self.caster.set_sp(40)
        self.target.set_hp(50)
        self.target.set_sp(30)

        actual = type(self.default_tree.pick_skill(self.caster, self.target)).__name__
        expected = 'MageSpecial'

        self.assertEqual(expected, actual,
                         ("When calling pick_skill on a SkillDecisionTree " +
                          "returned by create_default_tree (which should " +
                          "match the tree in a2.pdf) using the characters:" +
                          "\n{}\n{}\nExpected to get the skill {} back but got " +
                          "{} instead.").format(self.caster,
                                                self.target,
                                                expected,
                                                actual))

    def test_default_tree_matches_scenario_2(self):
        """
        Test to make sure the default tree works as expected for the scenario
        described in the handout.
        """
        self.caster.set_hp(80)
        self.caster.set_sp(40)
        self.target.set_hp(20)
        self.target.set_sp(50)

        actual = type(self.default_tree.pick_skill(self.caster, self.target)).__name__
        expected = 'RogueAttack'

        self.assertEqual(expected, actual,
                         ("When calling pick_skill on a SkillDecisionTree " +
                          "returned by create_default_tree (which should " +
                          "match the tree in a2.pdf) using the characters:" +
                          "\n{}\n{}\nExpected to get the skill {} back but got " +
                          "{} instead.").format(self.caster,
                                                self.target,
                                                expected,
                                                actual))

    def test_default_tree_returns_highest_priority_leaf(self):
        """
        Test to make sure the default tree works as expected for the scenario
        described.
        """
        self.caster.set_hp(95)
        self.caster.set_sp(30)
        self.target.set_hp(20)
        self.target.set_sp(50)

        actual = type(self.default_tree.pick_skill(self.caster, self.target)).__name__
        expected = 'RogueAttack'

        self.assertEqual(expected, actual,
                         ("When calling pick_skill on a SkillDecisionTree " +
                          "returned by create_default_tree (which should " +
                          "match the tree in a2.pdf) using the characters:" +
                          "\n{}\n{}\nExpected to get the skill {} back but got " +
                          "{} instead.").format(self.caster,
                                                self.target,
                                                expected,
                                                actual))

    def test_default_tree_returns_mixed_levels(self):
        """
        Test to make sure the default tree works as expected for the scenario
        described.
        """
        self.caster.set_hp(95)
        self.caster.set_sp(30)
        self.target.set_hp(50)
        self.target.set_sp(30)

        actual = type(self.default_tree.pick_skill(self.caster, self.target)).__name__
        expected = 'MageSpecial'

        self.assertEqual(expected, actual,
                         ("When calling pick_skill on a SkillDecisionTree " +
                          "returned by create_default_tree (which should " +
                          "match the tree in a2.pdf) using the characters:" +
                          "\n{}\n{}\nExpected to get the skill {} back but got " +
                          "{} instead.").format(self.caster,
                                                self.target,
                                                expected,
                                                actual))

    def test_default_tree_returns_root(self):
        """
        Test to make sure the default tree works as expected for the scenario
        described.
        """
        self.caster.set_hp(20)

        actual = type(self.default_tree.pick_skill(self.caster, self.target)).__name__
        expected = 'MageAttack'

        self.assertEqual(expected, actual,
                         ("When calling pick_skill on a SkillDecisionTree " +
                          "returned by create_default_tree (which should " +
                          "match the tree in a2.pdf) using the characters:" +
                          "\n{}\n{}\nExpected to get the skill {} back but got " +
                          "{} instead.").format(self.caster,
                                                self.target,
                                                expected,
                                                actual))

if __name__ == "__main__":
    unittest.main(exit = False)
