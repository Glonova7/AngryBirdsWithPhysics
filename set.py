import pygame
import math as m
import time

# 초기화
pygame.init()

# 창 설정
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Angry Bird")
bg = pygame.image.load("image/bg.png")
bg = pygame.transform.scale(bg, (screen_width, screen_height))

bird = pygame.image.load("image/bird.png")
bird = pygame.transform.scale(bird, (30, 30))




# 색상 변수
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
trail = []
hit_pos = []
stop = False


# 물체를 그리는 함수
def draw_object(calc,trail):
    axis = calc[0]
    screen.blit(bird, axis)
    
    highest_point = [calc[4],calc[3][0]]
    font = pygame.font.Font('font/GodoM.ttf',20)
    highest = font.render(f'Max(x,y) : ({round(highest_point[0])},{round(highest_point[1])})', True, (0,0,0))
    
    arrow = pygame.image.load("image/arrow.png")
    arrow = pygame.transform.scale(arrow, (25, 20))
    arrow = pygame.transform.rotate(arrow,calc[2])
    arrow.get_rect().center = (screen_width-230,screen_height-30)
    screen.blit(arrow, (screen_width-180,screen_height-85))
    trail.append(axis)

    if axis[0] > highest_point[0] and axis[1] > (screen_height - highest_point[1]):
        #print('um')
        pygame.draw.circle(screen, BLUE, [highest_point[0],screen_height-highest_point[1]], 7)
        screen.blit(highest, (highest_point[0] + 15, screen_height-highest_point[1]-30))
    
    for i in range(1, len(trail)):
        if i % 2 == 0:
            pygame.draw.line(screen, RED, trail[i-1], trail[i], 2)


# 초기값
sec = 0
v0 = 90
angle = 55
start_pos = (50, screen_height-(150))
g = 9.8


# 물체 위치 계산 함수
def calc(t):
    global start_pos, v0, angle, sec, stop

    theta = m.radians(angle)

    x_pos = start_pos[0] + (v0  * m.cos(theta) * t)
    y_pos = start_pos[1] - ((v0 *  m.sin(theta) * t - (g * t**2)/2))
    v = ((v0 * m.cos(theta))**2 + (v0 * m.sin(theta) - g*t)**2)**0.5
    a = g * t
    angle_radians = m.atan2((v0 * m.sin(m.radians(angle))) - (g * t), v0 * m.cos(m.radians(angle)))
    angle_degrees = m.degrees(angle_radians)
    T_h = v0 * m.sin(theta) / g
    R = start_pos[0] + (v0**2 * 2 * m.sin(theta) * m.cos(theta)) / g
    H = screen_height-start_pos[1]+((v0**2)*(m.sin(theta))**2)/(2*g)
    Max_x = start_pos[0] + (v0  * m.cos(theta) * T_h) # Added this because R/2 is not precise
    
    real_time = t*0.5

    return ((x_pos,y_pos), (v), (angle_degrees), (H, T_h, R), (Max_x))

start_time = time.time()
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if len(trail) > 300:
        trail.pop(0)

    # 시간
    sec = (time.time() - start_time) * 2
    seconds = int(sec)
    time.sleep(0.001)
    
    # 화면 업데이트
    screen.fill(WHITE)
    screen.blit(bg, (0,0))

    data = calc(sec)
    draw_object(data, trail)
 
    # 데이터 랜딩
    font = pygame.font.Font('font/GodoM.ttf',20)
    set_val = font.render(f'Setting Value:', True, (255,255,255))
    axis = font.render(f'(x,y) : ({str(round(data[0][0]))},{str((screen_height - round(data[0][1])))})', True, (0,0,0))
    v = font.render(f'v : {str(round(data[1]))}', True, (0,0,0))
    degree = font.render(f'θ : {str(round(data[2]))}', True, (0,0,0))
    show_angle = font.render(f'angle(θ) : {str(angle)}°', True, (0,0,0))
    show_V0 = font.render(f'v0 : {str(v0)}', True, (0,0,0))
    dist = font.render(f'(R, H, T_H) : ({str(round(data[3][2]))}, {str(round(data[3][0]))}, {round((data[3][1]/2),1)}s)', True, (0,0,0))
    
    # 화면 표시
    screen.blit(set_val, (10,10))
    screen.blit(show_angle, (10,40))
    screen.blit(show_V0, (10,70))
    
    screen.blit(axis, (screen_width-250,screen_height-140))
    screen.blit(dist, (screen_width-250,screen_height-110))
    screen.blit(degree, (screen_width-250,screen_height-80))
    screen.blit(v, (screen_width-250,screen_height-50))
   

    # 시간 업데이트
    

    # 화면 업데이트
    pygame.display.update()
    
    # 0.02초 대기
    pygame.time.wait(20)


# 종료
pygame.quit()