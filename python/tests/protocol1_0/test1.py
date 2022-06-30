# -*- coding: utf-8 -*-
import os

if os.name == 'nt':
    import msvcrt


    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)


    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *  # Uses Dynamixel SDK library

# Control table address
ADDR_MX_TORQUE_ENABLE = 24
ADDR_MX_MOVING_SPEED = 32
ADDR_MX_PRESENT_SPEED = 38
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_PRESENT_POSITION = 36

# Protocol version
PROTOCOL_VERSION = 1.0

# Default setting
DXL_ID0 = 0
DXL_ID2 = 2
DXL_ID3 = 3

# Dynamixel default baudrate : 57600
BAUDRATE = 1000000

# Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
DEVICENAME = '/dev/tty.usbserial-FT66WBIV'

TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixel Torque
packetHandler.write1ByteTxRx(portHandler, DXL_ID0, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
packetHandler.write1ByteTxRx(portHandler, DXL_ID2, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
packetHandler.write1ByteTxRx(portHandler, DXL_ID3, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)

##############################################################
# degree 되나? -150 부터 150까지 입력
def degree(degree3, degree0, degree2):
    # DXL_ID0                     = 0
    # DXL_ID2                     = 2 
    # DXL_ID3                     = 3

    print(51 / 300)

    motor0Temp = degree0 + 150
    motor2Temp = degree2 + 150
    motor3Temp = degree3 + 150

    dxl_goal_position0 = int((motor0Temp / 300.0) * 1023)
    dxl_goal_position2 = int((motor2Temp / 300.0) * 1023)
    dxl_goal_position3 = int((motor3Temp / 300.0) * 1023)

    dxl_present_position0, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID0,
                                                                                    ADDR_MX_PRESENT_POSITION)
    dxl_present_position2, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID2,
                                                                                    ADDR_MX_PRESENT_POSITION)
    dxl_present_position3, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID3,
                                                                                    ADDR_MX_PRESENT_POSITION)

    velocity0 = int(round(abs(dxl_goal_position0 - dxl_present_position0) / 2))
    velocity2 = int(round(abs(dxl_goal_position2 - dxl_present_position2) / 2))
    velocity3 = int(round(abs(dxl_goal_position3 - dxl_present_position3) / 2))

    # Write goal position
    packetHandler.write2ByteTxRx(portHandler, DXL_ID0, ADDR_MX_MOVING_SPEED, velocity0)
    packetHandler.write2ByteTxRx(portHandler, DXL_ID2, ADDR_MX_MOVING_SPEED, velocity2)
    packetHandler.write2ByteTxRx(portHandler, DXL_ID3, ADDR_MX_MOVING_SPEED, velocity3)

    packetHandler.write2ByteTxRx(portHandler, DXL_ID0, ADDR_MX_GOAL_POSITION, dxl_goal_position0)
    packetHandler.write2ByteTxRx(portHandler, DXL_ID2, ADDR_MX_GOAL_POSITION, dxl_goal_position2)
    packetHandler.write2ByteTxRx(portHandler, DXL_ID3, ADDR_MX_GOAL_POSITION, dxl_goal_position3)

    while 1:
        # Read present position

        dxl_present_position0, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID0,
                                                                                        ADDR_MX_PRESENT_POSITION)
        dxl_present_position2, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID2,
                                                                                        ADDR_MX_PRESENT_POSITION)
        dxl_present_position3, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID3,
                                                                                        ADDR_MX_PRESENT_POSITION)

        if ((abs(dxl_goal_position0 - dxl_present_position0) < 20) and (
                abs(dxl_goal_position2 - dxl_present_position2) < 20) and (
                abs(dxl_goal_position3 - dxl_present_position3) < 20)):
            break

        # if abs(dxl_goal_position3 - dxl_present_position3) < 20:
        #     break


############################################################################

# range is    -150 < degree < +150
degree(0, 0, 0)
degree(30, 0, 0)
degree(30, 30, 0)
degree(30, 30, 30)

degree(0, 0, 0)
# degree(40, -30, -100)
# degree(0, 30, 100)
# degree(80, 100, -100)
# degree(0, 0, 0)

########
# Disable Dynamixel Torque
# dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
# if dxl_comm_result != COMM_SUCCESS:
#     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
# elif dxl_error != 0:
#     print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()
