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


class Motor:
    # Control table address
    ADDR_TORQUE_ENABLE = 64
    ADDR_GOAL_POSITION = 116
    ADDR_PRESENT_POSITION = 132
    ADDR_GOAL_VELOCITY = 104
    ADDR_PRESENT_VELOCITY = 128

    # Protocol version
    PROTOCOL_VERSION = 2.0

    # Default setting
    DXL_ID1 = 1
    DXL_ID2 = 2
    DXL_ID3 = 3
    DXL_ID4 = 4
    DXL_ID5 = 5
    DXL_ID6 = 6

    BAUDRATE = 57600
    DEVICENAME = '/dev/tty.usbserial-FT66WBIV'

    TORQUE_ENABLE = 1
    TORQUE_DISABLE = 0

    # 포트와 패킷 핸들러 초기화
    def __init__(self) -> None:
        self.portHandler = PortHandler(self.DEVICENAME)
        self.packetHandler = PacketHandler(self.PROTOCOL_VERSION)
        # 포트 열기
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            quit()

        # 포트를 보드와 맞는 전송 속도로 맞춤
        if self.portHandler.setBaudRate(self.BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()

        # 토크 인가
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID1, self.ADDR_TORQUE_ENABLE,
                                          self.TORQUE_ENABLE)
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID2, self.ADDR_TORQUE_ENABLE,
                                          self.TORQUE_ENABLE)
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID3, self.ADDR_TORQUE_ENABLE,
                                          self.TORQUE_ENABLE)

    def __del__(self) -> None:
        # 토크 인가 전류 해제
        # self.packetHandler.write1ByteTxRx(self.portHandler, Motor.DXL_ID1, Motor.ADDR_TORQUE_ENABLE, Motor.TORQUE_DISABLE)

        # 포트 해제
        self.portHandler.closePort()

    # 모터의 각도를 조절 하는 메서드 2147483647 4294967296
    def degree(self, degree1, degree2, degree3):
        print('가동중...')

        # initial present position
        initial_present_position_ID1, _, _ = self.packetHandler.read4ByteTxRx(self.portHandler, self.DXL_ID1, self.ADDR_PRESENT_POSITION)
        if initial_present_position_ID1 > 100000000:
            initial_present_position_ID1 = initial_present_position_ID1 - 4294967296
        initial_present_position_ID2, _, _ = self.packetHandler.read4ByteTxRx(self.portHandler, self.DXL_ID2, self.ADDR_PRESENT_POSITION)
        if initial_present_position_ID2 > 100000000:
            initial_present_position_ID2 = initial_present_position_ID2 - 4294967296
        initial_present_position_ID3, _, _ = self.packetHandler.read4ByteTxRx(self.portHandler, self.DXL_ID3, self.ADDR_PRESENT_POSITION)
        if initial_present_position_ID3 > 100000000:
            initial_present_position_ID3 = initial_present_position_ID3 - 4294967296

        # goal position about input degree
        goal_position_ID1 = int((degree1 / 360.0) * 4095)
        if goal_position_ID1 - initial_present_position_ID1 > 0:
            VELOCITY_ID1 = 5
        else:
            VELOCITY_ID1 = -5
        goal_position_ID2 = int((degree2 / 360.0) * 4095)
        if goal_position_ID2 - initial_present_position_ID2 > 0:
            VELOCITY_ID2 = 5
        else:
            VELOCITY_ID2 = -5
        goal_position_ID3 = int((degree3 / 360.0) * 4095)
        if goal_position_ID3 - initial_present_position_ID3 > 0:
            VELOCITY_ID3 = 5
        else:
            VELOCITY_ID3 = -5
        print(goal_position_ID3)
        print(initial_present_position_ID3)

        # Write goal position
        self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID1, self.ADDR_GOAL_VELOCITY, VELOCITY_ID1)
        self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID2, self.ADDR_GOAL_VELOCITY, VELOCITY_ID2)
        self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID3, self.ADDR_GOAL_VELOCITY, VELOCITY_ID3)

        flag1 = False
        flag2 = False
        flag3 = False
        while 1:
            # Read present position
            present_position_ID1, _, _ = self.packetHandler.read4ByteTxRx(self.portHandler, self.DXL_ID1, self.ADDR_PRESENT_POSITION)
            if present_position_ID1 > 100000000:
                present_position_ID1 = present_position_ID1 - 4294967296
            present_position_ID2, _, _ = self.packetHandler.read4ByteTxRx(self.portHandler, self.DXL_ID2, self.ADDR_PRESENT_POSITION)
            if present_position_ID2 > 100000000:
                present_position_ID2 = present_position_ID2 - 4294967296
            present_position_ID3, _, _ = self.packetHandler.read4ByteTxRx(self.portHandler, self.DXL_ID3, self.ADDR_PRESENT_POSITION)
            if present_position_ID3 > 100000000:
                present_position_ID3 = present_position_ID3 - 4294967296

            print(f'ID1 -> goal angle : {(goal_position_ID1 / 4095) * 360}, present angle : {(present_position_ID1 / 4095) * 360}')
            print(f'ID2 -> goal angle : {(goal_position_ID2 / 4095) * 360}, present angle : {(present_position_ID2 / 4095) * 360}')
            print(f'ID3 -> goal angle : {(goal_position_ID3 / 4095) * 360}, present angle : {(present_position_ID3 / 4095) * 360}')
            print(f'ID3 -> goal : {goal_position_ID3}, present : {present_position_ID3}')

            if abs(goal_position_ID1 - present_position_ID1) < 10:
                self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID1, self.ADDR_GOAL_VELOCITY, 0)
                flag1 = True
            if abs(goal_position_ID2 - present_position_ID2) < 10:
                self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID2, self.ADDR_GOAL_VELOCITY, 0)
                flag2 = True
            if abs(goal_position_ID3 - present_position_ID3) < 10:
                self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID3, self.ADDR_GOAL_VELOCITY, 0)
                flag3 = True
            if flag1 and flag2 and flag3:
                break

