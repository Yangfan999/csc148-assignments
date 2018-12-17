"""CSC148 Assignment 1 - Simulation

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This contains the main Simulation class that is actually responsible for
creating and running the simulation. You'll also find the function `sample_run`
here at the bottom of the file, which you can use as a starting point to run
your simulation on a small configuration.

Note that we have provided a fairly comprehensive list of attributes for
Simulation already. You may add your own *private* attributes, but should not
remove any of the existing attributes.
"""
# You may import more things from these modules (e.g., additional types from
# typing), but you may not import from any other modules.
from typing import Dict, List, Any

import algorithms
from entities import Person, Elevator
from visualizer import Visualizer


class Simulation:
    """The main simulation class.

    === Attributes ===
    arrival_generator: the algorithm used to generate new arrivals.
    elevators: a list of the elevators in the simulation
    moving_algorithm: the algorithm used to decide how to move elevators
    num_floors: the number of floors
    visualizer: the Pygame visualizer used to visualize this simulation
    num_people: number of people
    num_iterations: number of rounds that took place
    max_time: the maximum time someone spent before reaching their target floor
    min_time: the minimum time someone spent before reaching their target floor
    avg_time: the time record someone spent before reaching their target floor
    people_completed: the number of people who reached their target destination
    waiting: a dictionary of people waiting for an elevator
             (keys are floor numbers, values are the list of waiting people)
    """
    arrival_generator: algorithms.ArrivalGenerator
    elevators: List[Elevator]
    moving_algorithm: algorithms.MovingAlgorithm
    num_floors: int
    num_people: int
    num_iterations: int
    people_completed: int
    max_time: int
    min_time: int
    avg_time: list
    visualizer: Visualizer
    waiting: Dict[int, List[Person]]

    def __init__(self,
                 config: Dict[str, Any]) -> None:
        """Initialize a new simulation using the given configuration."""

        self.num_iterations = 0
        self.num_people = 0
        self.people_completed = 0
        self.max_time = -1
        self.min_time = -1
        self.avg_time = []
        self.num_floors = config['num_floors']
        self.arrival_generator = config['arrival_generator']
        self.moving_algorithm = config['moving_algorithm']
        self.elevators = [Elevator(config['elevator_capacity'])
                          for _ in range(config['num_elevators'])]
        self.waiting = {}
        for i in range(self.num_floors):
            self.waiting[i+1] = []
        self.visualizer = Visualizer(self.elevators,
                                     self.num_floors,
                                     config['visualize'])

    ############################################################################
    # Handle rounds of simulation.
    ############################################################################
    def run(self, num_rounds: int) -> Dict[str, Any]:
        """Run the simulation for the given number of rounds.

        Return a set of statistics for this simulation run, as specified in the
        assignment handout.

        Precondition: num_rounds >= 1.

        Note: each run of the simulation starts from the same initial state
        (no people, all elevators are empty and start at floor 1).
        """
        self.num_iterations = num_rounds
        self.min_time = self.num_iterations  # set it to a large enough integer
        for i in range(num_rounds):
            self.visualizer.render_header(i)

            # Stage 1: generate new arrivals
            self._generate_arrivals(i)

            # Stage 2: leave elevators
            self._handle_leaving()

            # Stage 3: board elevators
            self._handle_boarding()

            # Stage 4: move the elevators using the moving algorithm
            self._move_elevators()

            # Pause for 1 second
            self.visualizer.wait(1)

        return self._calculate_stats()

    def _generate_arrivals(self, round_num: int) -> None:
        """Generate and visualize new arrivals."""

        dictionary = self.arrival_generator.generate(round_num)
        # update wating time
        for people in self.waiting.values():
            for p in people:
                p.wait_time += 1

        for e in self.elevators:
            for p in e.passengers:
                p.wait_time += 1

        for key in dictionary:
            self.waiting[key].extend(dictionary[key])
            self.num_people += len(dictionary[key])
        self.visualizer.show_arrivals(dictionary)

    def _handle_leaving(self) -> None:
        """Handle people leaving elevators."""
        for e in self.elevators:
            stay_passengers = []
            for p in e.passengers:
                if p.target == e.floor:
                    self.visualizer.show_disembarking(p, e)
                    self.people_completed += 1
                    self.avg_time.append(p.wait_time)
                    if p.wait_time > self.max_time:
                        self.max_time = p.wait_time
                    if p.wait_time < self.min_time:
                        self.min_time = p.wait_time
                else:
                    stay_passengers.append(p)
            e.passengers = stay_passengers

    def _handle_boarding(self) -> None:
        """Handle boarding of people and visualize."""
        for e in self.elevators:
            while e.fullness() != 1 and self.waiting[e.floor]:
                boarding = self.waiting[e.floor].pop(0)
                e.passengers.append(boarding)
                self.visualizer.show_boarding(boarding, e)

    def _move_elevators(self) -> None:
        """Move the elevators in this simulation.
        Use this simulation's moving algorithm to move the elevators.
        """
        directions = self.moving_algorithm.\
            move_elevators(self.elevators, self.waiting, self.num_floors)
        for i in range(len(self.elevators)):
            self.elevators[i].floor += directions[i].value
        self.visualizer.show_elevator_moves(self.elevators, directions)

    ############################################################################
    # Statistics calculations
    ############################################################################
    def _calculate_stats(self) -> Dict[str, int]:
        """Report the statistics for the current run of this simulation.
        """
        return {
            'num_iterations': self.num_iterations,
            'total_people': self.num_people,
            'people_completed': self.people_completed,
            'max_time': self.max_time,
            'min_time': -1 if self.min_time == self.num_iterations
                        else self.min_time,
            'avg_time': -1 if not self.avg_time
                        else int(sum(self.avg_time) / self.people_completed)
        }


def sample_run() -> Dict[str, int]:
    """Run a sample simulation, and return the simulation statistics."""
    config = {
        'num_floors': 6,
        'num_elevators': 6,
        'elevator_capacity': 3,
        'num_people_per_round': 0,
        # Random arrival generator with 6 max floors and 2 arrivals per round.
        'arrival_generator': algorithms.FileArrivals(6, "sample_arrivals.csv"),
        'moving_algorithm': algorithms.PushyPassenger(),
        'visualize': True
    }

    sim = Simulation(config)
    stats = sim.run(15)
    return stats


if __name__ == '__main__':
    # Uncomment this line to run our sample simulation (and print the
    # statistics generated by the simulation).
    # print(sample_run())
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['entities', 'visualizer', 'algorithms', 'time'],
        'max-nested-blocks': 4,
        'max-attributes': 12
    })
