"""CSC148 Assignment 1 - Algorithms

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains two sets of algorithms: ones for generating new arrivals to
the simulation, and ones for making decisions about how elevators should move.

As with other files, you may not change any of the public behaviour (attributes,
methods) given in the starter code, but you can definitely add new attributes
and methods to complete your work here.

See the 'Arrival generation algorithms' and 'Elevator moving algorithsm'
sections of the assignment handout for a complete description of each algorithm
you are expected to implement in this file.
"""
import csv
from enum import Enum
import random
from typing import Dict, List, Optional

from entities import Person, Elevator


###############################################################################
# Arrival generation algorithms
###############################################################################
class ArrivalGenerator:
    """An algorithm for specifying arrivals at each round of the simulation.

    === Attributes ===
    max_floor: The maximum floor number for the building.
               Generated people should not have a starting or target floor
               beyond this floor.
    num_people: The number of people to generate, or None if this is left
                up to the algorithm itself.

    === Representation Invariants ===
    max_floor >= 2
    num_people is None or num_people >= 0
    """
    max_floor: int
    num_people: Optional[int]

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.

        Preconditions:
            max_floor >= 2
            num_people is None or num_people >= 0
        """
        self.max_floor = max_floor
        self.num_people = num_people

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        raise NotImplementedError


class RandomArrivals(ArrivalGenerator):
    """Generate a fixed number of random people each round.

    Generate 0 people if self.num_people is None.

    For our testing purposes, this class *must* have the same initializer header
    as ArrivalGenerator. So if you choose to to override the initializer, make
    sure to keep the header the same!

    Hint: look up the 'sample' function from random.
    """

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """ Implement the abstruct method in parent class,
        generate people at the given round.
        """
        result = {}
        floor = [i + 1 for i in range(self.max_floor)]
        for _ in range(self.num_people):
            starting = random.choice(floor)
            floor.remove(starting)
            target = random.choice(floor)
            floor.append(starting)
            result[starting] = \
                result.get(starting, []) + [Person(starting, target)]
        return result


class FileArrivals(ArrivalGenerator):
    """Generate arrivals from a CSV file.
    """

    arrival_dic: dict

    def __init__(self, max_floor: int, filename: str) -> None:
        """Initialize a new FileArrivals algorithm from the given file.

        The num_people attribute of every FileArrivals instance is set to None,
        since the number of arrivals depends on the given file.

        Precondition:
            <filename> refers to a valid CSV file, following the specified
            format and restrictions from the assignment handout.
        """
        ArrivalGenerator.__init__(self, max_floor, None)

        # We've provided some of the "reading from csv files" boilerplate code
        # for you to help you get started.
        self.arrival_dic = {}
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                roundn = int(line[0])
                self.arrival_dic[roundn] = {}
                for i in range(1, len(line), 2):
                    start = int(line[i])
                    target = int(line[i+1])
                    self.arrival_dic[roundn][start] = \
                        self.arrival_dic[roundn]\
                            .get(start, []) + [Person(start, target)]

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """
        Implement the abstruct method in parent class,
        generate people at the given round.
        """
        return self.arrival_dic.get(round_num, {})


###############################################################################
# Elevator moving algorithms
###############################################################################
class Direction(Enum):
    """
    The following defines the possible directions an elevator can move.
    This is output by the simulation's algorithms.

    The possible values you'll use in your Python code are:
        Direction.UP, Direction.DOWN, Direction.STAY
    """
    UP = 1
    STAY = 0
    DOWN = -1


class MovingAlgorithm:
    """An algorithm to make decisions for moving an elevator at each round.
    """
    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        raise NotImplementedError


class RandomAlgorithm(MovingAlgorithm):
    """A moving algorithm that picks a random direction for each elevator.
    """

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.
        """
        directions = []
        choices = [Direction.UP, Direction.STAY, Direction.DOWN]
        for e in elevators:
            if e.floor == max_floor:
                directions.append(random.choice(choices[1:]))
            elif e.floor == 1:
                directions.append(random.choice(choices[:-1]))
            else:
                directions.append(random.choice(choices))
        return directions


class PushyPassenger(MovingAlgorithm):
    """A moving algorithm that preferences the first passenger on each elevator.

    If the elevator is empty, it moves towards the *lowest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the target floor of the
    *first* passenger who boarded the elevator.
    """

    def move_elevators(self, elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.
        """
        directions = []
        for e in elevators:
            if e.fullness():
                target = e.passengers[0].target
            else:
                target = e.floor
                for floor in sorted(waiting.keys()):
                    if waiting[floor]:
                        target = floor
                        break
            if target > e.floor:
                directions.append(Direction.UP)
            elif target == e.floor:
                directions.append(Direction.STAY)
            else:
                directions.append(Direction.DOWN)
        return directions


class ShortSighted(MovingAlgorithm):
    """A moving algorithm that preferences the closest possible choice.

    If the elevator is empty, it moves towards the *closest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the closest target floor of
    all passengers who are on the elevator.

    In this case, the order in which people boarded does *not* matter.
    """

    def move_elevators(self, elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.
        """
        directions = []
        for e in elevators:
            if e.fullness():
                distance = sorted(
                    [(abs(p.target - e.floor), p.target - e.floor)
                     for p in e.passengers])
            else:
                distance = sorted(
                    [(abs(f - e.floor), f - e.floor)
                     for f in waiting.keys() if waiting[f]])
            if not distance:
                directions.append(Direction.STAY)
            elif len(distance) > 1\
                    and distance[0][0] == distance[1][0]\
                    and distance[0][1] != distance[1][1]:
                # moves towards lower in case of ties
                directions.append(Direction.DOWN)
            else:
                if distance[0][1] > 0:
                    directions.append(Direction.UP)
                else:
                    directions.append(Direction.DOWN)
        return directions


if __name__ == '__main__':
    # Don't forget to check your work regularly with python_ta!
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['__init__'],
        'extra-imports': ['entities', 'random', 'csv', 'enum'],
        'max-nested-blocks': 4,
        'disable': ['R0201']
    })
