"""
Basic Unittests for your implementation of a sorcerer for A2.

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
from a2_skill_decision_tree import create_default_tree
SorcererConstructor = CHARACTER_CLASSES['s']

class SorcererUnitTests(unittest.TestCase):    
    def setUp(self):
        """
        Sets up a Battle Queue containing 2 Sorcerer for all of the 
        unittests.
        """
        self.battle_queue = BattleQueue()
        playstyle = ManualPlaystyle(self.battle_queue)
        
        self.p1 = SorcererConstructor("P1", self.battle_queue, playstyle)
        self.p2 = SorcererConstructor("P2", self.battle_queue, playstyle)
        
        self.p1.enemy = self.p2
        self.p2.enemy = self.p1
        
        self.p1.set_skill_decision_tree(create_default_tree())
        self.p2.set_skill_decision_tree(create_default_tree())

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
                         ("After using an 'A' attack, a sorcerer should " +
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
                         ("After using an 'S' attack, a sorcerer should " +
                          "have {} " +
                          "SP left over but got {} instead.").format(
                              expected_sp, remaining_sp))

    def test_attack_hp(self):
        """
        Test to make sure a single attack reduces HP correctly when the enemy
        is a sorcerer.
        
        Make sure the sorcerer's HP heals by the amount changed
        """
        self.p1.attack()
        
        remaining_hp = self.p2.get_hp()
        expected_hp = 100 - (20 - 10)
        self.assertEqual(remaining_hp, expected_hp, 
                         ("After using an 'A' attack, a sorcerer's target " +
                          "(which " +
                          "is also a sorcerer) should have {} " +
                          "HP left over but got {} instead.").format(
                              expected_hp, remaining_hp))

    def test_special_attack_hp(self):
        """
        Test to make sure a single special attack reduces HP correctly when the
        enemy is a sorcerer.
        """
        self.p1.special_attack()
        
        remaining_hp = self.p2.get_hp()
        expected_hp = 100 - (25 - 10)
        self.assertEqual(remaining_hp, expected_hp, 
                         ("After using an 'S' attack, a sorcerer's target " +
                          "(which " +
                          "is also a sorcerer) should have {} " +
                          "HP left over but got {} instead.").format(
                              expected_hp, remaining_hp))

    def test_is_valid_action(self):
        """
        Test to make sure is_valid_action returns True for both 'A' and 'S'
        for a newly created character.
        """
        self.assertTrue(self.p1.is_valid_action('A'),
                        ("Calling is_valid_action('A') on a newly created " + 
                         "sorcerer should return True but got False."))

        self.assertTrue(self.p1.is_valid_action('S'),
                        ("Calling is_valid_action('S') on a newly created " + 
                         "sorcerer should return True but got False."))

    def test_is_valid_action_false(self):
        """
        Test to make sure is_valid_action returns False when passed a skill
        and when there's not enough sp to use that skill.
        """
        self.p1.set_sp(19)
        
        self.assertFalse(self.p1.is_valid_action('S'),
                         ("Calling is_valid_action('S') on a sorcerer " +
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
                          " sorcerer should return both 'A' and 'S' but got " +
                          "{} instead.").format(actions))
    
    def test_repr(self):
        """
        Test to make sure the repr is in the correct format.
        """
        actual = repr(self.p1)
        self.assertEqual(actual, "P1 (Sorcerer): 100/100",
                         ("Calling repr on a sorcerer should give a repr in the " +
                          "form Name (Character): HP/SP but got " +
                          "{} instead.").format(actual))
    
    def test_special_attack_battle_queue(self):
        """
        Test to make sure the special attack correctly adds the enemy into
        the Queue before an attacking sorcerer's special attack.
        """
        self.battle_queue.add(self.p1)
        self.battle_queue.add(self.p2)
        self.battle_queue.add(self.p2)
        self.battle_queue.add(self.p1)
        self.p1.special_attack()
        self.battle_queue.remove()
        
        # The queue should be P2 -> P1 -> P1 -> P2
        queue_order = []
        while not self.battle_queue.is_empty():
            queue_order.append(self.battle_queue.remove().get_name())
        
        self.assertEqual(queue_order, ['P2', 'P1'],
                         ("After using a special attack, expected the battle " +
                          "queue to be in the order P2 -> P1 but " +
                          "got {} instead.").format(" -> ".join(queue_order)))
    
    def test_get_next_sprite_idle(self):
        """
        Test to make sure get_next_sprite gives the correct sprites when in
        idle pose.
        """
        expected_sprites = ["sorcerer_idle_0",
                            "sorcerer_idle_1",
                            "sorcerer_idle_2",
                            "sorcerer_idle_3",
                            "sorcerer_idle_4",
                            "sorcerer_idle_5",
                            "sorcerer_idle_6",
                            "sorcerer_idle_7",
                            "sorcerer_idle_8",
                            "sorcerer_idle_9",
                            "sorcerer_idle_0",
                            ]
        
        obtained_sprites = []
        for i in range(11):
            obtained_sprites.append(self.p1.get_next_sprite())
        
        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the sorcerer was " +
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
        
        expected_sprites = ["sorcerer_attack_0",
                            "sorcerer_attack_1",
                            "sorcerer_attack_2",
                            "sorcerer_attack_3",
                            "sorcerer_attack_4",
                            "sorcerer_attack_5",
                            "sorcerer_attack_6",
                            "sorcerer_attack_7",
                            "sorcerer_attack_8",
                            "sorcerer_attack_9",
                            "sorcerer_idle_0",
                            ]
        
        obtained_sprites = []
        for i in range(11):
            obtained_sprites.append(self.p1.get_next_sprite())
        
        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the sorcerer was " +
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
        
        expected_sprites = ["sorcerer_special_0",
                            "sorcerer_special_1",
                            "sorcerer_special_2",
                            "sorcerer_special_3",
                            "sorcerer_special_4",
                            "sorcerer_special_5",
                            "sorcerer_special_6",
                            "sorcerer_special_7",
                            "sorcerer_special_8",
                            "sorcerer_special_9",
                            "sorcerer_idle_0",
                            ]
        
        obtained_sprites = []
        for i in range(11):
            obtained_sprites.append(self.p1.get_next_sprite())
        
        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the sorcerer was " +
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
        expected_sprites = ["sorcerer_attack_0",
                            "sorcerer_attack_1",
                            "sorcerer_attack_2",
                            "sorcerer_attack_0",
                            "sorcerer_attack_1",
                            "sorcerer_attack_2",
                            "sorcerer_attack_3",
                            ]
        
        obtained_sprites = []
        for i in range(3):
            obtained_sprites.append(self.p1.get_next_sprite())
    
        self.p1.attack()
        for i in range(4):
            obtained_sprites.append(self.p1.get_next_sprite())
            
        
        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the sorcerer was " +
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
        expected_sprites = ["sorcerer_special_0",
                            "sorcerer_special_1",
                            "sorcerer_special_2",
                            "sorcerer_special_0",
                            "sorcerer_special_1",
                            "sorcerer_special_2",
                            "sorcerer_special_3",
                            ]
        
        obtained_sprites = []
        for i in range(3):
            obtained_sprites.append(self.p1.get_next_sprite())
    
        self.p1.special_attack()
        for i in range(4):
            obtained_sprites.append(self.p1.get_next_sprite())
            
        
        self.assertEqual(obtained_sprites, expected_sprites,
                         ("Calling get_next_sprite when the sorcerer was " +
                          "in special attack pose and special attacking again" +
                          " after calling " +
                          "get_next_sprite 3 times " +
                          "should have given us sprites " +
                          "in the order:\n{}\bBut got:\n{}\ninstead.").format(
                              ", ".join(expected_sprites), 
                              ", ".join(obtained_sprites)))

if __name__ == "__main__":
    unittest.main(exit = False)