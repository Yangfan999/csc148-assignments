"""
Basic Unittests for your implementation of a RestrictedBattleQueue for A2.

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
from a2_battle_queue import RestrictedBattleQueue
MageConstructor = CHARACTER_CLASSES['m']
RogueConstructor = CHARACTER_CLASSES['r']

class RestrictedBattleQueueUnitTests(unittest.TestCase):
    def setUp(self):
        """
        Sets up a Restricted Battle Queue for all of the unittests.
        """
        self.battle_queue = RestrictedBattleQueue()
        playstyle = ManualPlaystyle(self.battle_queue)

        self.p1 = RogueConstructor("R", self.battle_queue, playstyle)
        self.p2 = MageConstructor("M", self.battle_queue, playstyle)

        self.p1.enemy = self.p2
        self.p2.enemy = self.p1

        self.battle_queue.add(self.p1)
        self.battle_queue.add(self.p2)

    def tearDown(self):
        """
        Delete the attributes that were created in setUp.
        """
        del self.battle_queue
        del self.p1
        del self.p2

    def test_copy(self):
        """
        Test to make sure copy returns the characters in the right order.
        """
        self.battle_queue.add(self.p2)
        self.battle_queue.add(self.p1)
        self.battle_queue.add(self.p1)

        commands = ["bq.add(r)",
                    "bq.add(m)",
                    "bq.add(m)",
                    "bq.add(r)",
                    "bq.add(r)",
                    "bq = bq.copy()"]

        expected = ["R", "M", "M", "R", "R"]
        actual = []

        bq = self.battle_queue.copy()
        while not bq.is_empty():
            actual.append(bq.remove().get_name())

        self.assertEqual(expected, actual,
                         ("After adding and removing from a " +
                          "RestrictedBattleQueue using the following commands" +
                          " where r is named R and m is named M:\n{}\n"
                          "The RestrictedBattleQueue should be in the order:" +
                          "\n{}\nBut got the following order instead:\n" +
                          "{}").format("\n".join(commands),
                                       " -> ".join(expected),
                                       " -> ".join(actual)))

        self.assertFalse(self.battle_queue.is_empty(),
                         ("After emptying out a copy of a " +
                          "RestrictedBattleQueue, the original should still " +
                          "have elements in it."))

    def test_copy_maintains_add_order(self):
        """
        Test to make sure copy maintains the order in which characters
        can add to the RestrictedBattleQueue.
        """
        self.battle_queue.add(self.p2)
        self.battle_queue.add(self.p1)
        self.battle_queue.add(self.p1)
        bq = self.battle_queue.copy()
        r = bq.remove()

        m = r.enemy

        bq.add(m)
        bq.remove()
        bq.add(m)
        bq.remove()

        bq.add(r)
        bq.remove()
        bq.add(r)


        commands = ["bq.add(r)",
                    "bq.add(m)",
                    "bq.add(m)",
                    "bq.add(r)",
                    "bq.add(r)",
                    "bq = bq.copy()",
                    "bq.remove()",
                    "bq.add(m)",
                    "bq.remove()",
                    "bq.add(m)",
                    "bq.remove()",
                    "bq.add(r)",
                    "bq.remove()",
                    "bq.add(r)"]

        expected = ["R", "M", "R"]

        actual = []

        while not bq.is_empty():
            actual.append(bq.remove().get_name())

        self.assertEqual(expected, actual,
                         ("After adding and removing from a " +
                          "RestrictedBattleQueue using the following commands" +
                          " where r is named R and m is named M:\n{}\n"
                          "The RestrictedBattleQueue should be in the order:" +
                          "\n{}\nBut got the following order instead:\n" +
                          "{}").format("\n".join(commands),
                                       " -> ".join(expected),
                                       " -> ".join(actual)))

        self.assertFalse(self.battle_queue.is_empty(),
                         ("After emptying out a copy of a " +
                          "RestrictedBattleQueue, the original should still " +
                          "have elements in it."))

    def test_add_extra_copies(self):
        """
        Test to make sure when extra copies add they aren't able to add to the
        queue.
        """
        self.battle_queue.add(self.p1)
        self.battle_queue.add(self.p1)
        self.battle_queue.remove()
        self.battle_queue.remove()
        self.battle_queue.add(self.p2)
        self.battle_queue.remove()
        self.battle_queue.add(self.p2)
        self.battle_queue.remove()

        commands = ["bq.add(r)",
                    "bq.add(m)",
                    "bq.add(r)",
                    "bq.add(r)",
                    "bq.remove()",
                    "bq.remove()",
                    "bq.add(m)",
                    "bq.remove()",
                    "bq.add(m)"]

        expected = ["M"]

        actual = []

        while not self.battle_queue.is_empty():
            actual.append(self.battle_queue.remove().get_name())

        self.assertEqual(expected, actual,
                         ("After adding and removing from a " +
                          "RestrictedBattleQueue using the following commands" +
                          " where r is named R and m is named M:\n{}\n"
                          "The RestrictedBattleQueue should be in the order:" +
                          "\n{}\nBut got the following order instead:\n" +
                          "{}").format("\n".join(commands),
                                       " -> ".join(expected),
                                       " -> ".join(actual)))


    def test_add_by_other_character(self):
        """
        Test to make sure a character that's added by another character
        isn't able to add to the queue.
        """
        self.battle_queue.add(self.p2)
        self.battle_queue.remove()
        self.battle_queue.remove()
        self.battle_queue.add(self.p2)

        commands = ["bq.add(r)",
                    "bq.add(m)",
                    "bq.add(m)",
                    "bq.remove()",
                    "bq.remove()",
                    "bq.add(m)"]

        expected = ["M"]

        actual = []

        while not self.battle_queue.is_empty():
            actual.append(self.battle_queue.remove().get_name())

        self.assertEqual(expected, actual,
                         ("After adding and removing from a " +
                          "RestrictedBattleQueue using the following commands" +
                          " where r is named R and m is named M:\n{}\n"
                          "The RestrictedBattleQueue should be in the order:" +
                          "\n{}\nBut got the following order instead:\n" +
                          "{}").format("\n".join(commands),
                                       " -> ".join(expected),
                                       " -> ".join(actual)))


    def test_is_empty_ignores_low_sp(self):
        """
        Test to make sure is_empty correctly ignores characters with low SP.
        """
        self.p1.set_sp(1)
        self.p2.set_sp(1)

        self.assertTrue(self.battle_queue.is_empty(),
                        "When both characters have low SP, is_empty() should " +
                        "return True but got False instead.")

    def test_is_over_no_sp(self):
        """
        Test to make sure is_over works correctly when the characters have
        no SP.
        """
        self.p1.set_sp(1)
        self.p2.set_sp(1)

        self.assertTrue(self.battle_queue.is_over(),
                        "When both characters have low SP, is_over() should " +
                        "return True but got False instead.")

    def test_is_winner_no_hp(self):
        """
        Test to make sure is_winner works correctly when one character has
        no HP.
        """
        self.p1.set_hp(0)
        expected = self.p2
        actual = self.battle_queue.get_winner()

        self.assertEqual(expected, actual,
                         ("When the BattleQueue contains the following " +
                          "characters:\n{}\n{}\nget_winner() should return {} " +
                          "but got {} instead.").format(self.p1,
                                                        self.p2,
                                                        expected,
                                                        actual))


    def test_peek_no_sp(self):
        """
        Test to make sure peek works correctly when the characters have no
        SP.
        """
        self.p1.set_sp(1)

        expected = self.p2
        actual = self.battle_queue.peek()

        self.assertEqual(expected, actual,
                         ("When the BattleQueue contains the following " +
                          "characters:\n{} -> {}\npeek() should return {} " +
                          "but got {} instead.").format(self.p1,
                                                        self.p2,
                                                        expected,
                                                        actual))
    def test_remove_no_sp(self):
        """
        Test to make sure remove works correctly when the characters have no
        SP.
        """
        self.p1.set_sp(1)

        expected = self.p2
        actual = self.battle_queue.remove()

        self.assertEqual(expected, actual,
                         ("When the BattleQueue contains the following " +
                          "characters:\n{} -> {}\nremove() should return {} " +
                          "but got {} instead.").format(self.p1,
                                                        self.p2,
                                                        expected,
                                                        actual))

if __name__ == "__main__":
    unittest.main(exit = False)
