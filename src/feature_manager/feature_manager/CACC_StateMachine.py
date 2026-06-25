"""State machine for cooperative adaptive cruise control transitions.

This module defines the CACC feature manager state machine and maps cruise
control request messages to driver event inputs.
"""

from feature_manager.StateMachine import State, StateMachine
from custom_interfaces.msg import CruiseRequest

class StateMachineForCACC():
	"""Manages transitions for CACC across OFF, STBY, ON, and FAULTED states."""

	def __init__(self):
		"""Initialize the CACC FSM and default event flags."""
		self.fsm = StateMachine(State.OFF)
		self._build_transitions()

		# Vehicle Conditions
		self.enable_conditions_met = True

		# Driver Events
		self.event_toggle = False
		self.event_cancel = False
		self.event_activate = False

	def _build_transitions(self):
		"""Define the valid state transitions for the CACC state machine.

		Transitions are added to the underlying StateMachine with guard
		conditions based on enablement and driver-input flags.
		"""
		# OFF STATE TRANSITIONS
		self.fsm.add_transition(State.OFF, State.STBY, lambda: self.enable_conditions_met and self.event_toggle)

		# STANDBY STATE TRANSITIONS
		self.fsm.add_transition(State.STBY, State.OFF, lambda: not self.enable_conditions_met)
		self.fsm.add_transition(State.STBY, State.OFF, lambda: self.event_toggle)
		self.fsm.add_transition(State.STBY, State.ON, lambda: self.event_activate)
		self.fsm.add_transition(State.STBY, State.FAULTED, lambda: False)  # Placeholder condition

		# ON STATE TRANSITIONS
		self.fsm.add_transition(State.ON, State.OFF, lambda: not self.enable_conditions_met)
		self.fsm.add_transition(State.ON, State.OFF, lambda: self.event_toggle)
		self.fsm.add_transition(State.ON, State.STBY, lambda: self.event_cancel)
		self.fsm.add_transition(State.ON, State.FAULTED, lambda: False)	 # Placeholder condition

		# FAULTED STATE TRANSITIONS
		self.fsm.add_transition(State.FAULTED, State.OFF, lambda: True)  # Placeholder condition to reset from faulted state
	
	@property
	def state(self):
		"""Current state of the CACC feature.

		Returns:
			State: The current state of the underlying state machine.
		"""
		return self.fsm.state
	
	def step(self):
		"""Advance the state machine by one evaluation cycle.

		The FSM evaluates all enabled transitions once and then clears one-shot
		command events so that they do not persist into the next step.
		"""
		self.fsm.step()
		self.reset_events() # Reset events after processing to ensure they are only active for one step

	def reset_events(self):
		"""Clear one-shot driver event flags.

		This ensures a cruise request event is only acted upon during the step in
		which it was received.
		"""
		self.event_toggle = False
		self.event_cancel = False
		self.event_activate = False

	def update_fields_with_cruise_request(self, msg: CruiseRequest):
		"""Translate a CruiseRequest message into internal event flags.

		Args:
			msg (CruiseRequest): Incoming cruise control request message.
		"""
		self.event_toggle = (msg.cruise_event == CruiseRequest.CRUISE_TOGGLE)
		self.event_cancel = (msg.cruise_event == CruiseRequest.CRUISE_CANCEL)
		self.event_activate = (msg.cruise_event == CruiseRequest.CRUISE_SET) or (msg.cruise_event == CruiseRequest.CRUISE_RESUME)
