
## Desired Trajectory 로부터 값이 들어옴.
# Desired 각도
th1d, th2d = 1, 1

# Desired 각속도
dth1d, dth2d = 1, 1

# Desired 각가속도
ddth1d, ddth2d = 1, 1

## Dynamixel 로부터 값이 들어옴.
# Observable 각도
th1, th2 = 1, 1

# Observable 각속도
dth1, dth2 = 1, 1

# 슬라이딩 라인의 기울기 C
# 채터링 폭의 계수 K
c1, c2 = 1, 1
k1, k2 = 20, 20

# 에러 정의
e1 = th1d - th1
e2 = dth1d - dth1

e3 = th2d - th2
e4 = dth2d - dth2

# 에러를 기반으로 슬라이딩 라인 정의
# 해당 라인이 0으로 미끄러진다면 에러는 0에 수렴하고
# Observable 값이 Desired 값을 잘 따라간다는 의미
s1 = c1*e1 + e2 
s2 = c2*e3 + e4 

print('s1 : ', s1)
print('s2 : ', s2)

# 슬라이딩 라인 시그넘?
if abs(s1) <= 1:
    sgn1 = s1
elif s1 > 1:
    sgn1 = 1
else:
    sgn1 = -1

if abs(s2) <= 1:
    sgn2 = s2
elif s2 > 1:
    sgn2 = 1
else:
    sgn2 = -1


print('signum1 : ', sgn1)