"""
Basic Unittests for your implementation of a Iterative Minimax Playstyle for A2.

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
from a2_game import CHARACTER_CLASSES, PLAYSTYLE_CLASSES
from a2_playstyle import get_state_score, ManualPlaystyle
from a2_battle_queue import BattleQueue
MageConstructor = CHARACTER_CLASSES['m']
RogueConstructor = CHARACTER_CLASSES['r']
Minimax = PLAYSTYLE_CLASSES['mi']

class IterativeMinimaxUnitTests(unittest.TestCase):
    def setUp(self):
        """
        Sets up a Battle Queue containing 2 a Mage and Rogue for all of the
        unittests.
        """
        self.battle_queue = BattleQueue()
        playstyle = ManualPlaystyle(self.battle_queue)

        self.p1 = RogueConstructor("R", self.battle_queue, playstyle)
        self.p2 = MageConstructor("M", self.battle_queue, playstyle)

        self.p1.enemy = self.p2
        self.p2.enemy = self.p1

        self.battle_queue.add(self.p1)
        self.battle_queue.add(self.p2)

        self.minimax_playstyle = Minimax(self.battle_queue)

    def tearDown(self):
        """
        Delete the attributes that were created in setUp.
        """
        del self.battle_queue
        del self.p1
        del self.p2

    def test_select_attack_one_attack(self):
        """
        Test to make sure calling select_attack when only one attack is
        available returns that attack.
        """
        self.p1.set_sp(5)

        bq = repr(self.battle_queue)

        expected = "A"
        actual = self.minimax_playstyle.select_attack()

        self.assertEqual(expected, actual,
                         ("Calling select_attack() on a BattleQueue that " +
                          "looks like:\n{}\nShould return the attack {} " +
                          "but got {} instead.").format(bq,
                                                        expected,
                                                        actual))

    def test_select_attack_to_win(self):
        """
        Test to make sure calling select_attack works when one path runs out
        of SP.
        """
        self.battle_queue.remove()
        self.battle_queue.add(self.p1)
        self.p1.set_hp(40)
        self.p1.set_sp(10)
        self.p2.set_hp(100)
        self.p2.set_sp(30)

        bq = repr(self.battle_queue)

        expected = "A"
        actual = self.minimax_playstyle.select_attack()

        self.assertEqual(expected, actual,
                         ("Calling select_attack() on a BattleQueue that " +
                          "looks like:\n{}\nShould return the attack {} " +
                          "but got {} instead.").format(bq,
                                                        expected,
                                                        actual))

    def test_select_attack_to_win_opponent_can_kill(self):
        """
        Test to make sure calling select_attack when use special attack results
        in a loss but attack results in a win.
        """
        self.battle_queue.remove()
        self.battle_queue.add(self.p1)
        self.p1.set_hp(40)
        self.p1.set_sp(6)
        self.p2.set_hp(14)
        self.p2.set_sp(35)

        bq = repr(self.battle_queue)

        expected = "A"
        actual = self.minimax_playstyle.select_attack()

        self.assertEqual(expected, actual,
                         ("Calling select_attack() on a BattleQueue that " +
                          "looks like:\n{}\nShould return the attack {} " +
                          "but got {} instead.").format(bq,
                                                        expected,
                                                        actual))

    def test_select_special_attack_to_win(self):
        """
        Test to make sure calling select_attack when use special attack results
        in a win but attack results in a loss.
        """
        self.battle_queue.remove()
        self.battle_queue.add(self.p1)
        self.p1.set_hp(30)
        self.p1.set_sp(100)
        self.p2.set_hp(5)
        self.p2.set_sp(30)

        bq = repr(self.battle_queue)

        expected = "S"
        actual = self.minimax_playstyle.select_attack()

        self.assertEqual(expected, actual,
                         ("Calling select_attack() on a BattleQueue that " +
                          "looks like:\n{}\nShould return the attack {} " +
                          "but got {} instead.").format(bq,
                                                        expected,
                                                        actual))

    def test_select_attack_rogue(self):
        """
        Test to make sure calling select_attack can return attack for rogue.
        """
        self.p1.set_hp(100)
        self.p1.set_sp(12)
        self.p2.set_hp(28)
        self.p2.set_sp(100)

        bq = repr(self.battle_queue)

        expected = "A"
        actual = self.minimax_playstyle.select_attack()

        self.assertEqual(expected, actual,
                         ("Calling select_attack() on a BattleQueue that " +
                          "looks like:\n{}\nShould return the attack {} " +
                          "but got {} instead.").format(bq,
                                                        expected,
                                                        actual))

    def test_select_special_attack_rogue(self):
        """
        Test to make sure calling select_attack can return special attack for
        rogue.
        """
        self.p1.set_hp(20)
        self.p1.set_sp(100)
        self.p2.set_hp(27)
        self.p2.set_sp(100)

        bq = repr(self.battle_queue)

        expected = "S"
        actual = self.minimax_playstyle.select_attack()

        self.assertEqual(expected, actual,
                         ("Calling select_attack() on a BattleQueue that " +
                          "looks like:\n{}\nShould return the attack {} " +
                          "but got {} instead.").format(bq,
                                                        expected,
                                                        actual))

    def test_run_full_game(self):
        """
        Test to make sure calling select_attack can return special attack for
        rogue.
        """
        bq = repr(self.battle_queue)

        expected = "S"
        actual = self.minimax_playstyle.select_attack()

        self.assertEqual(expected, actual,
                         ("Calling select_attack() on a BattleQueue that " +
                          "looks like:\n{}\nShould return the attack {} " +
                          "but got {} instead.").format(bq,
                                                        expected,
                                                        actual))


if __name__ == "__main__":
    unittest.main(exit = False)
