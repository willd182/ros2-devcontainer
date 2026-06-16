from StateMachine import State, StateMachine
from common_interfaces.msg import CruiseRequest

class StateMachineForCACC():
	def __init__(self):
		self.fsm = StateMachine(State.OFF)
		self._build_transitions()

		# Vehicle Conditions
		self.enable_conditions_met = True

		# Driver Events
		self.event_toggle = False
		self.event_cancel = False
		self.event_activate = False

	def _build_transitions(self):
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
		return self.fsm.state
	
	def step(self):
		self.fsm.step()
		self.reset_events() # Reset events after processing to ensure they are only active for one step

	def reset_events(self):
		self.event_toggle = False
		self.event_cancel = False
		self.event_activate = False

	def update_fields_with_cruise_request(self, msg: CruiseRequest):
		self.event_toggle = (msg.cruise_event == CruiseRequest.CRUISE_TOGGLE)
		self.event_cancel = (msg.cruise_event == CruiseRequest.CRUISE_CANCEL)
		self.event_activate = (msg.cruise_event == CruiseRequest.CRUISE_SET) or (msg.cruise_event == CruiseRequest.CRUISE_RESUME)
