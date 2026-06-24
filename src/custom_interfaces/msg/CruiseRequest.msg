# DriverEvent represents a single driver intent action in the system.
# It is used as a unified event stream from driver inputs (CAN, buttons, HMI).

# Primary Message Fields
uint8 cruise_event  # Event type, use the constants above (e.g. CRUISE_NONE)
uint8 increment_type  # Type of increment for cruise control (e.g. SMALL_INCREMENT)
uint64 timestamp  	# Timestamp in nanoseconds since epoch (optional)

# CRUISE EVENT Fields
uint8 CRUISE_NONE=0
uint8 CRUISE_TOGGLE=1
uint8 CRUISE_CANCEL=2
uint8 CRUISE_RESUME=3
uint8 CRUISE_SET=4

# INCREMENT TYPE Fields
uint8 NO_CHANGE=0
uint8 SMALL_INCREMENT=1
uint8 LARGE_INCREMENT=2
uint8 SMALL_DECREMENT=3
uint8 LARGE_DECREMENT=4



