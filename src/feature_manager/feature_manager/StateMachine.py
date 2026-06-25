"""Finite state machine implementation with state enumeration and transitions."""

from enum import Enum, auto
from typing import Callable, Tuple


class State(Enum):
    """States for the finite state machine."""
    OFF = auto()
    STBY = auto()
    ON = auto()
    FAULTED = auto()

# Instances of Types
Condition = Callable[[], bool]
TransitionKey = Tuple[State, State]


class StateMachine:
    """Manages state transitions based on conditions."""

    def __init__(self, initial_state: State):
        self.state = initial_state
        self.transitions = {}  # from_state -> list of (to_state, condition)

    def add_transition(self, from_state: State, to_state: State, condition: Condition):
        """Add a transition between two states with a condition.

        Args:
            from_state: Source State.
            to_state: Destination State.
            condition: True when transition should occur.
        """
        if from_state not in self.transitions:
            self.transitions[from_state] = []

        self.transitions[from_state].append((to_state, condition))

    def step(self):
        """Evaluate conditions and perform any applicable state transition.

        Returns:
            Current state after evaluation.
        """
        for to_state, condition in self.transitions.get(self.state, []):
            if condition():
                self.state = to_state
                return self.state
        return self.state