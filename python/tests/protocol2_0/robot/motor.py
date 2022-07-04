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

    BAUDRATE = 1000000
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
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID0, self.ADDR_MX_TORQUE_ENABLE,
                                          self.TORQUE_ENABLE)
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID2, self.ADDR_MX_TORQUE_ENABLE,
                                          self.TORQUE_ENABLE)
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID3, self.ADDR_MX_TORQUE_ENABLE,
                                          self.TORQUE_ENABLE)

    def __del__(self) -> None:
        # 토크 인가전류 해제
        # self.packetHandler.write1ByteTxRx(self.portHandler, Motor.DXL_ID0, Motor.ADDR_MX_TORQUE_ENABLE, Motor.TORQUE_DISABLE)
        # self.packetHandler.write1ByteTxRx(self.portHandler, Motor.DXL_ID2, Motor.ADDR_MX_TORQUE_ENABLE, Motor.TORQUE_DISABLE)
        # self.packetHandler.write1ByteTxRx(self.portHandler, Motor.DXL_ID3, Motor.ADDR_MX_TORQUE_ENABLE, Motor.TORQUE_DISABLE)

        # 포트 해제
        self.portHandler.closePort()

    # 모터의 각도를 조절 하는 메서드
    # 순서 대로 4axis, 5axis, 6axis
    def degree(self, degree3, degree0, degree2):

        print('가동중...')

        motor0temp = degree0 + 150
        motor2temp = degree2 + 150
        motor3temp = degree3 + 150

        dxl_goal_position0 = int((motor0temp / 300.0) * 1023)
        dxl_goal_position2 = int((motor2temp / 300.0) * 1023)
        dxl_goal_position3 = int((motor3temp / 300.0) * 1023)

        dxl_present_position0, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID0, self.ADDR_MX_PRESENT_POSITION)
        dxl_present_position2, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID2, self.ADDR_MX_PRESENT_POSITION)
        dxl_present_position3, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID3, self.ADDR_MX_PRESENT_POSITION)

        velocity0 = int(round(abs(dxl_goal_position0 - dxl_present_position0) / 2))
        velocity2 = int(round(abs(dxl_goal_position2 - dxl_present_position2) / 2))
        velocity3 = int(round(abs(dxl_goal_position3 - dxl_present_position3) / 2))

        # Write goal position
        self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID0, self.ADDR_MX_MOVING_SPEED, velocity0)
        self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID2, self.ADDR_MX_MOVING_SPEED, velocity2)
        self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID3, self.ADDR_MX_MOVING_SPEED, velocity3)

        self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID0, self.ADDR_MX_GOAL_POSITION, dxl_goal_position0)
        self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID2, self.ADDR_MX_GOAL_POSITION, dxl_goal_position2)
        self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID3, self.ADDR_MX_GOAL_POSITION, dxl_goal_position3)

        while 1:
            # Read present position
            dxl_present_position0, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID0, self.ADDR_MX_PRESENT_POSITION)
            dxl_present_position2, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID2, self.ADDR_MX_PRESENT_POSITION)
            dxl_present_position3, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID3, self.ADDR_MX_PRESENT_POSITION)

            if ((abs(dxl_goal_position0 - dxl_present_position0) < 20) and (
                    abs(dxl_goal_position2 - dxl_present_position2) < 20) and (
                    abs(dxl_goal_position3 - dxl_present_position3) < 20)):
                break
