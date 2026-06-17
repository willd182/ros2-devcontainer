from enum import Enum, auto
from typing import Callable, Tuple

# Define States for the FSM
class State(Enum):
    OFF = auto()
    STBY = auto()
    ON = auto()
    FAULTED = auto()

# Instances of Types
Condition = Callable[[], bool]
TransitionKey = Tuple[State, State]

# Simple FSM Implementation
class StateMachine:
    def __init__(self, initial_state: State):
        self.state = initial_state
        self.transitions = {}  # from_state -> list of (to_state, condition)

    def add_transition(self, from_state, to_state, condition):
        if from_state not in self.transitions:
            self.transitions[from_state] = []

        self.transitions[from_state].append((to_state, condition))

    def step(self):
        for to_state, condition in self.transitions.get(self.state, []):
            if condition():
                self.state = to_state
                return self.state
        return self.state