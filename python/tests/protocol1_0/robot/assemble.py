import motor
motor = motor.Motor()

# range is    -150 < degree < +150
motor.degree(0, 0, 0)
motor.degree(40, -30, -100)
motor.degree(0, 30, 100)
motor.degree(80, 100, -100)
motor.degree(0, 0, 0)

