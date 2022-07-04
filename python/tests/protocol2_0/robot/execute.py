import time
import motor
import kinematics

# .py = module
# .py가 포함된 폴더 = package
# from abc import xyz : abc 라는 package(폴더) 에서 xyz 라는 module (파일)을 불러옴

motor = motor.Motor()

for i in range(1, 10):
    print('입장')
    Px = i * 0.1
    Py = 1
    Pz = -1

    result = kinematics.kinematics(Px, Py, Pz)
    print(result)

    # range is -150 < degree < +150
    if (-150 < result[0][3] < 150) and (-150 < result[0][4] < 150) and (-150 < result[0][5] < 150):
        motor.degree(result[0][3], result[0][4], result[0][5])
    elif (-150 < result[1][3] < 150) and (-150 < result[1][4] < 150) and (-150 < result[1][5] < 150):
        motor.degree(result[1][3], result[1][4], result[1][5])
    elif (-150 < result[2][3] < 150) and (-150 < result[2][4] < 150) and (-150 < result[2][5] < 150):
        motor.degree(result[2][3], result[2][4], result[2][5])
    elif (-150 < result[3][3] < 150) and (-150 < result[3][4] < 150) and (-150 < result[3][5] < 150):
        motor.degree(result[3][3], result[3][4], result[3][5])
    else:
        break

    time.sleep(1)
    print('나감')


# range is -150 < degree < +150
# motor.degree(0, 0, 0)
# motor.degree(40, -30, -100)
# motor.degree(0, 30, 100)
# motor.degree(80, 100, -100)
# motor.degree(0, 0, 0)
