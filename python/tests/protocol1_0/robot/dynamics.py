import sympy as sp

# 링크 길이 정의
l1, l2 = sp.symbols('l1'), sp.symbols('l2')

# 질량 정의
m1, m2 = sp.symbols('m1'), sp.symbols('m2')

# 중력가속도 정의
g = sp.symbols('g')

# 시간 정의
t = sp.symbols('t')

# 타우 정의
tou1, tou2 = sp.symbols('tou1'), sp.symbols('tou2')

# 세타는 시간에 대한 함수
# th1 = th1(t), th2 = th2(t)
theta1, theta2 = sp.symbols('th1', cls=sp.Function), sp.symbols('th2', cls=sp.Function)
th1 = theta1(t)
th2 = theta2(t)

# p1(x1,y1) p2(x2,y2) 정의
x1 = l1*sp.cos(th1)
y1 = l1*sp.sin(th1)
x2 = l1*sp.cos(th1) + l2*sp.cos(th1+th2)
y2 = l1*sp.sin(th1) + l2*sp.sin(th1+th2)

# 위치를 시간에 대해 미분 -> 미소 속도
dx1 = sp.diff(x1,t)
dy1 = sp.diff(y1,t)
dx2 = sp.diff(x2,t)
dy2 = sp.diff(y2,t)

# x,y 성분의 미소속도를 평균제곱으로 속도 사용
v1 = sp.sqrt(dx1**2 + dy1**2)
v2 = sp.sqrt(dx2**2 + dy2**2)

# 높이 정의
h1 = y1
h2 = y2

# 라그랑주 방정식을 위한 에너지 정의
K = 0.5*m1*v1**2 + 0.5*m2*v2**2
U = m1*g*h1 + m2*g*h2
L = K - U

# 세타1 = th1 : th1(t)
# 세타1닷 = dth1 : Derivative(th1(t), t)
# 세타2닷 = dth2 : Derivative(th1(t), (t, 2))
dth1 = sp.diff(th1, t)
dth2 = sp.diff(th2, t)
ddth1 = sp.diff(dth1, t)
ddth2 = sp.diff(dth2, t)

# 라그랑지안을 각도에 대해 편미분
RLRth1 = sp.diff(L, th1)
RLRth2 = sp.diff(L, th2)

# 라그랑지안을 각속도에 대해 편미분 후, 시간에 대해 정미분
RLRdth1dt = sp.diff(sp.diff(L, dth1), t)
RLRdth2dt = sp.diff(sp.diff(L, dth2), t)

# 식을 전개함. 묶여있으니까 계수를 잘 못찾음.
# lagrange는 라그랑주 방정식 = 0 
lagrange1 = (RLRdth1dt - RLRth1).expand()
lagrange2 = (RLRdth2dt - RLRth2).expand()

# 질량 matrix의 elements
m11 = (lagrange1.coeff(ddth1)).simplify()
m12 = (lagrange1.coeff(ddth2)).simplify()
m21 = (lagrange2.coeff(ddth1)).simplify()
m22 = (lagrange2.coeff(ddth2)).simplify()

# 중력 matrix의 elements
g1 = (lagrange1.coeff(g)).simplify()
g2 = (lagrange2.coeff(g)).simplify()

# 코리올리 matrix의 elements
v1 = (lagrange1 - (m11*ddth1) - (m12*ddth2) - (g1*g)).simplify()
v2 = (lagrange2 - (m21*ddth1) - (m22*ddth2) - (g2*g)).simplify()

# 질량, 각가속도, 코리올리, 중력, 타우 matrix 정의
M = sp.Matrix(([m11, m12], [m21, m22]))
DDTH = sp.Matrix(([ddth1], [ddth2]))
V = sp.Matrix(([v1], [v2]))
G = sp.Matrix(([g1], [g2]))*g
TOU = sp.Matrix(([tou1], [tou2]))

# 각가속도에 대해 표현
RESULT = M.inv()*(TOU - V - G)

# 각가속도1, 각가속도2 : simplify()
doubleDotTheta1 = (RESULT[0]).simplify()
doubleDotTheta2 = (RESULT[1]).simplify()

print(doubleDotTheta1)
print('\n')
print(doubleDotTheta2)