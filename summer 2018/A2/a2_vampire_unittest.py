"""
Basic Unittests for your implementation of a vampire for A2.

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
VampireConstructor = CHARACTER_CLASSES['v']

class VampireUnitTests(unittest.TestCase):
    def setUp(self):
        """
        Sets up a Battle Queue containing 2 Vampires for all of the 
        unittests.
        """
        self.battle_queue = BattleQueue()
        playstyle = ManualPlaystyle(self.battle_queue)
        
        self.p1 = VampireConstructor("P1", self.battle_queue, playstyle)
        self.p2 = VampireConstructor("P2", self.battle_queue, playstyle)
        
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
        Test to make sure a single attack reduces SP correctly.
        """
        self.p1.attack()
        
        remaining_sp = self.p1.get_sp()
        expected_sp = 100 - 15
        self.assertEqual(remaining_sp, expected_sp, 
                         ("After using an 'A' attack, a vampire should " +
                          "have {} " +
                          "SP left over but got {} instead.").format(
                              expected_sp, remaining_sp))

    def test_special_attack_sp(self):
        """
        Test to make sure a single special attack reduces SP correctly.
        """
        self.p1.special_attack()
        
        remaining_sp = self.p1.get_sp()
        expected_sp = 100 - 20
        self.assertEqual(remaining_sp, expected_sp, 
                         ("After using an 'S' attack, a vampire should " +
                          "have {} " +
                          "SP left over but got {} instead.").format(
                              expected_sp, remaining_sp))

    def test_attack_hp(self):
        """
        Test to make sure a single attack reduces HP correctly when the enemy
        is a vampire.
        
        Make sure the vampire's HP heals by the amount changed
        """
        self.p1.attack()
        
        remaining_hp = self.p2.get_hp()
        expected_hp = 100 - (20 - 3)
        self.assertEqual(remaining_hp, expected_hp, 
                         ("After using an 'A' attack, a vampire's target " +
                          "(which " +
                          "is also a vampire) should have {} " +
                          "HP left over but got {} instead.").format(
                              expected_hp, remaining_hp))
        
        remaining_hp = self.p1.get_hp()
        expected_hp = 100 + (20 - 3)
        self.assertEqual(remaining_hp, expected_hp, 
                         ("After using an 'A' attack on a vampire target, " +
                          "the attacking vampire should have {} " +
                          "HP but got {} instead.").format(
                              expected_hp, remaining_hp))

    def test_special_attack_hp(self):
        """
        Test to make sure a single special attack reduces HP correctly when the
        enemy is a vampire.
        """
        self.p1.special_attack()
        
        remaining_hp = self.p2.get_hp()
        expected_hp = 100 - (30 - 3)
        self.assertEqual(remaining_hp, expected_hp, 
                         ("After using an 'S' attack, a vampire's target " +
                          "(which " +
                          "is also a vampire) should have {} " +
                          "HP left over but got {} instead.").format(
                              expected_hp, remaining_hp))
        
        remaining_hp = self.p1.get_hp()
        expected_hp = 100 + (30 - 3)
        self.assertEqual(remaining_hp, expected_hp, 
                         ("After using an 'A' attack on a vampire target, " +
                          "the attacking vampire should have {} " +
                          "HP but got {} instead.").format(
                              expected_hp, remaining_hp))

    def test_is_valid_action(self):
        """
        Test to make sure is_valid_action returns True for both 'A' and 'S'
        for a newly created character.
        """
        self.assertTrue(self.p1.is_valid_action('A'),
                        ("Calling is_valid_action('A') on a newly created " + 
                         "vampire should return True but got False."))

        self.assertTrue(self.p1.is_valid_action('S'),
                        ("Calling is_valid_action('S') on a newly created " + 
                         "vampire should return True but got False."))

    def test_is_valid_action_false(self):
        """
        Test to make sure is_valid_action returns False when passed a skill
        and when there's not enough sp to use that skill.
        """
        self.p1.set_sp(19)
        
        self.assertFalse(self.p1.is_valid_action('S'),
                         ("Calling is_valid_action('S') on a vampire " +
                          "which has " + 
                          "19 SP should return False but got True."))        
        

    def test_get_available_actions(self):
        """
        Test to make sure get_available_actions returns both 'A' and 'S'
        for a newly created character.
        """
        actions = self.p1.get_available_actions()
        actions.sort()
        
        self.assertEqual(actions, ['A', 'S'],
                         ("Calling get_available_actions() on a newly created" +
                          " vampire should return both 'A' and 'S' but got " +
                          "{} instead.").format(actions))
    
    def test_repr(self):
        """
        Test to make sure the repr is in the correct format.
        """
        actual = repr(self.p1)
        self.assertEqual(actual, "P1 (Vampire): 100/100",
                         ("Calling repr on a vampire should give a repr in the " +
                          "form Name (Character): HP/SP but got " +
                          "{} instead.").format(actual))
    
    def test_special_attack_battle_queue(self):
        """
        Test to make sure the special attack correctly adds the enemy into
        the Queue before an attacking vampire's special attack.
        """
        self.p1.special_attack()
        self.battle_queue.remove()
        
        # The queue should be P2 -> P1 -> P1 -> P2
        queue_order = []
        for i in range(4):
            queue_order.append(self.battle_queue.remove().get_name())
        
        self.assertEqual(queue_order, ['P2', 'P1', 'P1', 'P2'],
                         ("After using a special attack, expected the battle " +
                          "queue to be in the order P2 -> P1 -> P1 -> P2 but " +
                          "got {} instead.").format(" -> ".join(queue_order)))
    
    def test_get_next_sprite_idle(self):
        """
        Test to make sure get_next_sprite gives the correct sprites when in
        idle pose.
        """
        expected_sprites = ["vampire_idle_0",
                            "vampire_idle_1",
                            "vampire_idle_2",
                            "vampire_idle_3",
                            "vampire_idle_4",
                            "vampire_idle_5",
                            "vampire_idle_6",
                            "vampire_idle_7",
                            "vampire_idle_8",
                            "vampire_idle_9",
                            "vampire_idle_0",
                            ]
        
        obtained_sprites = []
        for i in range(11):
            obtained_sprites.append(self.p1.get_next_sprite())
        
        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the vampire was " +
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
        
        expected_sprites = ["vampire_attack_0",
                            "vampire_attack_1",
                            "vampire_attack_2",
                            "vampire_attack_3",
                            "vampire_attack_4",
                            "vampire_attack_5",
                            "vampire_attack_6",
                            "vampire_attack_7",
                            "vampire_attack_8",
                            "vampire_attack_9",
                            "vampire_idle_0",
                            ]
        
        obtained_sprites = []
        for i in range(11):
            obtained_sprites.append(self.p1.get_next_sprite())
        
        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the vampire was " +
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
        
        expected_sprites = ["vampire_special_0",
                            "vampire_special_1",
                            "vampire_special_2",
                            "vampire_special_3",
                            "vampire_special_4",
                            "vampire_special_5",
                            "vampire_special_6",
                            "vampire_special_7",
                            "vampire_special_8",
                            "vampire_special_9",
                            "vampire_idle_0",
                            ]
        
        obtained_sprites = []
        for i in range(11):
            obtained_sprites.append(self.p1.get_next_sprite())
        
        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the vampire was " +
                          "in special pose should have given us sprites " +
                          "in the order:\n{}\nBut got:\n{}\ninstead.").format(
                              ", ".join(expected_sprites), 
                              ", ".join(obtained_sprites)))
    
    def test_get_next_sprite_attack_reset(self):
        """
        Test to make sure get_next_sprite() returns the correct sprite when
        calling attack twice (without finishing the animation)
        """
        self.p1.attack()
        expected_sprites = ["vampire_attack_0",
                            "vampire_attack_1",
                            "vampire_attack_2",
                            "vampire_attack_0",
                            "vampire_attack_1",
                            "vampire_attack_2",
                            "vampire_attack_3",
                            ]
        
        obtained_sprites = []
        for i in range(3):
            obtained_sprites.append(self.p1.get_next_sprite())
    
        self.p1.attack()
        for i in range(4):
            obtained_sprites.append(self.p1.get_next_sprite())
            
        
        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the vampire was " +
                          "in attack pose and attacking again after calling " +
                          "get_next_sprite 3 times " +
                          "should have given us sprites " +
                          "in the order:\n{}\nBut got:\n{}\ninstead.").format(
                              ", ".join(expected_sprites), 
                              ", ".join(obtained_sprites)))
         

    def test_get_next_sprite_special_reset(self):
        """
        Test to make sure get_next_sprite() returns the correct sprite when
        calling special twice (without finishing the animation)
        """
        self.p1.special_attack()
        expected_sprites = ["vampire_special_0",
                            "vampire_special_1",
                            "vampire_special_2",
                            "vampire_special_0",
                            "vampire_special_1",
                            "vampire_special_2",
                            "vampire_special_3",
                            ]
        
        obtained_sprites = []
        for i in range(3):
            obtained_sprites.append(self.p1.get_next_sprite())
    
        self.p1.special_attack()
        for i in range(4):
            obtained_sprites.append(self.p1.get_next_sprite())
            
        
        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the vampire was " +
                          "in special attack pose and special attacking again" +
                          " after calling " +
                          "get_next_sprite 3 times " +
                          "should have given us sprites " +
                          "in the order:\n{}\bBut got:\n{}\ninstead.").format(
                              ", ".join(expected_sprites), 
                              ", ".join(obtained_sprites)))

if __name__ == "__main__":
    unittest.main(exit = False)