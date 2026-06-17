import pytest
from feature_manager.CACC_StateMachine import StateMachineForCACC
from feature_manager.StateMachine import State
from common_interfaces.msg import CruiseRequest

@pytest.fixture
def fsm():
    return StateMachineForCACC()

def test_initial_state(fsm):
    fsm.step()
    assert fsm.state == State.OFF

def test_off_to_stby(fsm):
    fsm.update_fields_with_cruise_request(CruiseRequest(cruise_event=CruiseRequest.CRUISE_TOGGLE))
    fsm.step()
    assert fsm.state == State.STBY

def test_consumption(fsm):
    fsm.update_fields_with_cruise_request(CruiseRequest(cruise_event=CruiseRequest.CRUISE_TOGGLE))
    fsm.step()
    fsm.step()  # Step again without new event
    assert fsm.state == State.STBY  # Should remain in STBY, event should not trigger again without new input

def test_stby_to_on_through_set(fsm):
    fsm.update_fields_with_cruise_request(CruiseRequest(cruise_event=CruiseRequest.CRUISE_TOGGLE))
    fsm.step()  # OFF -> STBY
    fsm.update_fields_with_cruise_request(CruiseRequest(cruise_event=CruiseRequest.CRUISE_SET))
    fsm.step()  # STBY -> ON
    assert fsm.state == State.ON

def test_stby_to_on_through_resume(fsm):
    fsm.update_fields_with_cruise_request(CruiseRequest(cruise_event=CruiseRequest.CRUISE_TOGGLE))
    fsm.step()  # OFF -> STBY
    fsm.update_fields_with_cruise_request(CruiseRequest(cruise_event=CruiseRequest.CRUISE_RESUME))
    fsm.step()  # STBY -> ON
    assert fsm.state == State.ON

def test_on_to_stby_through_cancel(fsm):
    fsm.update_fields_with_cruise_request(CruiseRequest(cruise_event=CruiseRequest.CRUISE_TOGGLE))
    fsm.step()  # OFF -> STBY
    fsm.update_fields_with_cruise_request(CruiseRequest(cruise_event=CruiseRequest.CRUISE_SET))
    fsm.step()  # STBY -> ON
    fsm.update_fields_with_cruise_request(CruiseRequest(cruise_event=CruiseRequest.CRUISE_CANCEL))
    fsm.step()  # ON -> STBY
    assert fsm.state == State.STBY

def test_on_to_off_through_toggle(fsm):
    fsm.update_fields_with_cruise_request(CruiseRequest(cruise_event=CruiseRequest.CRUISE_TOGGLE))
    fsm.step()  # OFF -> STBY
    fsm.update_fields_with_cruise_request(CruiseRequest(cruise_event=CruiseRequest.CRUISE_SET))
    fsm.step()  # STBY -> ON
    fsm.update_fields_with_cruise_request(CruiseRequest(cruise_event=CruiseRequest.CRUISE_TOGGLE))
    fsm.step()  # ON -> OFF
    assert fsm.state == State.OFF