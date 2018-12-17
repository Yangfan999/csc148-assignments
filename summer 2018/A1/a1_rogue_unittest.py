"""
Basic Unittests for your implementation of a rogue for A1.

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
from A1.a1_game import CHARACTER_CLASSES
from A1.a1_playstyle import ManualPlaystyle
from A1.a1_battle_queue import BattleQueue
RogueConstructor = CHARACTER_CLASSES['r']

class RogueUnitTests(unittest.TestCase):
    def setUp(self):
        """
        Sets up a Battle Queue containing 2 Rogues for all of the unittests.
        """
        self.battle_queue = BattleQueue()
        playstyle = ManualPlaystyle(self.battle_queue)

        self.p1 = RogueConstructor("P1", self.battle_queue, playstyle)
        self.p2 = RogueConstructor("P2", self.battle_queue, playstyle)

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

    def test_attack_sp(self):
        """
        Test to make sure a single attack reduces _sp correctly.
        """
        self.p1.attack()

        remaining_sp = self.p1.get_sp()
        expected_sp = 100 - 3
        self.assertEqual(remaining_sp, expected_sp,
                         ("After using an 'A' attack, a rogue should have {} " +
                          "_sp left over but got {} instead.").format(
                              expected_sp, remaining_sp))

    def test_special_attack_sp(self):
        """
        Test to make sure a single special attack reduces _sp correctly.
        """
        self.p1.special_attack()

        remaining_sp = self.p1.get_sp()
        expected_sp = 100 - 10
        self.assertEqual(remaining_sp, expected_sp,
                         ("After using an 'S' attack, a rogue should have {} " +
                          "_sp left over but got {} instead.").format(
                              expected_sp, remaining_sp))

    def test_attack_hp(self):
        """
        Test to make sure a single attack reduces _hp correctly when the enemy
        is a rogue.
        """
        self.p1.attack()

        remaining_hp = self.p2.get_hp()
        expected_hp = 100 - (15 - 10)
        self.assertEqual(remaining_hp, expected_hp,
                         ("After using an 'A' attack, a rogue's target (which " +
                          "is also a rogue) should have {} " +
                          "_hp left over but got {} instead.").format(
                              expected_hp, remaining_hp))

    def test_special_attack_hp(self):
        """
        Test to make sure a single special attack reduces _hp correctly when the
        enemy is a rogue.
        """
        self.p1.special_attack()

        remaining_hp = self.p2.get_hp()
        expected_hp = 100 - (20 - 10)
        self.assertEqual(remaining_hp, expected_hp,
                         ("After using an 'S' attack, a rogue's target (which " +
                          "is also a rogue) should have {} " +
                          "_hp left over but got {} instead.").format(
                              expected_hp, remaining_hp))

    def test_is_valid_action(self):
        """
        Test to make sure is_valid_action returns True for both 'A' and 'S'
        for a newly created character.
        """
        self.assertTrue(self.p1.is_valid_action('A'),
                        ("Calling is_valid_action('A') on a newly created " +
                         "rogue should return True but got False."))

        self.assertTrue(self.p1.is_valid_action('S'),
                        ("Calling is_valid_action('S') on a newly created " +
                         "rogue should return True but got False."))

    def test_is_valid_action_false(self):
        """
        Test to make sure is_valid_action returns False when passed a skill
        and when there's not enough sp to use that skill.
        """
        for i in range(9):
            self.p1.special_attack()
        # 10 _sp left

        self.p1.attack() # 7 sp left

        remaining_sp = self.p1.get_sp()

        self.assertEqual(remaining_sp, 7,
                         ("After using an 'S' attack 3 times, a rogue " +
                          "should have {} _sp left over but got {} " +
                          " instead.").format(7, remaining_sp))

        self.assertFalse(self.p1.is_valid_action('S'),
                         ("Calling is_valid_action('S') on a rogue which has " +
                          "7 _sp should return True but got False."))


    def test_get_available_actions(self):
        """
        Test to make sure get_available_actions returns both 'A' and 'S'
        for a newly created character.
        """
        actions = self.p1.get_available_actions()
        actions.sort()

        self.assertEqual(actions, ['A', 'S'],
                         ("Calling get_available_actions() on a newly created" +
                          " rogue should return both 'A' and 'S' but got " +
                          "{} instead.").format(actions))

    def test_get_available_actions_only_a(self):
        """
        Test to make sure get_available_actions returns pnly 'A' for a rogue
        who should only have 10 _sp remaining.
        """
        for i in range(9):
            self.p1.special_attack()
        # 10 _sp left

        self.p1.attack() # 7 sp left

        remaining_sp = self.p1.get_sp()

        self.assertEqual(remaining_sp, 7,
                         ("After using an 'S' attack 3 times, a rogue " +
                          "should have {} _sp left over but got {} " +
                          " instead.").format(7, remaining_sp))

        actions = self.p1.get_available_actions()
        actions.sort()

        self.assertEqual(actions, ['A'],
                         ("Calling get_available_actions() on a rogue which " +
                          "has 7 _sp should return ['A'] but got " +
                          "{} instead.").format(actions))

    def test_repr(self):
        """
        Test to make sure the repr is in the correct format.
        """
        actual = repr(self.p1)
        self.assertEqual(actual, "P1 (Rogue): 100/100",
                         ("Calling repr on a rogue should give a repr in the " +
                          "form Name (Character): _hp/_sp but got " +
                          "{} instead.").format(actual))

    def test_hp_drops_to_0(self):
        """
        Test to make sure _hp drops to 0 after 10 special attacks
        """
        for i in range(10):
            self.p1.special_attack()

        remaining_hp = self.p2.get_hp()

        self.assertEqual(remaining_hp, 0,
                         ("After using 'S' attacks 10 times on another " +
                          "rogue, that rogue should be at " +
                          "0 _hp but got {} instead.").format(remaining_hp))


    def test_special_attack_battle_queue(self):
        """
        Test to make sure the special attack correctly adds the enemy into
        the Queue before an attacking rogue's special attack.
        """
        self.battle_queue.remove()
        self.p1.special_attack()

        # The _queue should be P2 -> P1 -> P1
        queue_order = []
        for i in range(3):
            queue_order.append(self.battle_queue.remove().get_name())

        self.assertEqual(queue_order, ['P2', 'P1', 'P1'],
                         ("After using a special attack, expected the battle " +
                          "_queue to be in the order P2 -> P1 -> P1 but got " +
                          "{} instead.").format(" -> ".join(queue_order)))

    def test_get_next_sprite_idle(self):
        """
        Test to make sure get_next_sprite gives the correct sprites when in
        idle pose.
        """
        expected_sprites = ["rogue_idle_0",
                            "rogue_idle_1",
                            "rogue_idle_2",
                            "rogue_idle_3",
                            "rogue_idle_4",
                            "rogue_idle_5",
                            "rogue_idle_6",
                            "rogue_idle_7",
                            "rogue_idle_8",
                            "rogue_idle_9",
                            "rogue_idle_0",
                            ]

        obtained_sprites = []
        for i in range(11):
            obtained_sprites.append(self.p1.get_next_sprite())

        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the rogue was " +
                          "in idle pose should have given us sprites in the " +
                          "order:\n{}\bBut got:\n{}\ninstead.").format(
                              ", ".join(expected_sprites),
                              ", ".join(obtained_sprites)))

    def test_get_next_sprite_attack(self):
        """
        Test to make sure get_next_sprite gives the correct sprites when in
        attack pose.
        """
        self.p1.attack()

        expected_sprites = ["rogue_attack_0",
                            "rogue_attack_1",
                            "rogue_attack_2",
                            "rogue_attack_3",
                            "rogue_attack_4",
                            "rogue_attack_5",
                            "rogue_attack_6",
                            "rogue_attack_7",
                            "rogue_attack_8",
                            "rogue_attack_9",
                            "rogue_idle_0",
                            ]

        obtained_sprites = []
        for i in range(11):
            obtained_sprites.append(self.p1.get_next_sprite())

        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the rogue was " +
                          "in attack pose should have given us sprites in the" +
                          " order:\n{}\bBut got:\n{}\ninstead.").format(
                              ", ".join(expected_sprites),
                              ", ".join(obtained_sprites)))

    def test_get_next_sprite_special_attack(self):
        """
        Test to make sure get_next_sprite gives the correct sprites when in
        special attack pose.
        """
        self.p1.special_attack()

        expected_sprites = ["rogue_special_0",
                            "rogue_special_1",
                            "rogue_special_2",
                            "rogue_special_3",
                            "rogue_special_4",
                            "rogue_special_5",
                            "rogue_special_6",
                            "rogue_special_7",
                            "rogue_special_8",
                            "rogue_special_9",
                            "rogue_idle_0",
                            ]

        obtained_sprites = []
        for i in range(11):
            obtained_sprites.append(self.p1.get_next_sprite())

        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the rogue was " +
                          "in special pose should have given us sprites " +
                          "in the order:\n{}\bBut got:\n{}\ninstead.").format(
                              ", ".join(expected_sprites),
                              ", ".join(obtained_sprites)))

    def test_get_next_sprite_attack_reset(self):
        """
        Test to make sure get_next_sprite() returns the correct sprite when
        calling attack twice (without finishing the animation)
        """
        self.p1.attack()
        expected_sprites = ["rogue_attack_0",
                            "rogue_attack_1",
                            "rogue_attack_2",
                            "rogue_attack_0",
                            "rogue_attack_1",
                            "rogue_attack_2",
                            "rogue_attack_3",
                            ]

        obtained_sprites = []
        for i in range(3):
            obtained_sprites.append(self.p1.get_next_sprite())

        self.p1.attack()
        for i in range(4):
            obtained_sprites.append(self.p1.get_next_sprite())


        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the rogue was " +
                          "in attack pose and attacking again after calling " +
                          "get_next_sprite 3 times " +
                          "should have given us sprites " +
                          "in the order:\n{}\bBut got:\n{}\ninstead.").format(
                              ", ".join(expected_sprites),
                              ", ".join(obtained_sprites)))


    def test_get_next_sprite_special_reset(self):
        """
        Test to make sure get_next_sprite() returns the correct sprite when
        calling special twice (without finishing the animation)
        """
        self.p1.special_attack()
        expected_sprites = ["rogue_special_0",
                            "rogue_special_1",
                            "rogue_special_2",
                            "rogue_special_0",
                            "rogue_special_1",
                            "rogue_special_2",
                            "rogue_special_3",
                            ]

        obtained_sprites = []
        for i in range(3):
            obtained_sprites.append(self.p1.get_next_sprite())

        self.p1.special_attack()
        for i in range(4):
            obtained_sprites.append(self.p1.get_next_sprite())


        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the rogue was " +
                          "in special attack pose and special attacking again" +
                          " after calling " +
                          "get_next_sprite 3 times " +
                          "should have given us sprites " +
                          "in the order:\n{}\bBut got:\n{}\ninstead.").format(
                              ", ".join(expected_sprites),
                              ", ".join(obtained_sprites)))

if __name__ == "__main__":
    unittest.main(exit = False)
