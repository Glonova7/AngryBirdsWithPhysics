import pygame
import math as m
import time

# 초기화
pygame.init()

# 창 설정
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Parameter Graph")
bg = pygame.image.load("image/bg.png")
bg = pygame.transform.scale(bg, (screen_width, screen_height))

bird = pygame.image.load("image/bird.png")
bird = pygame.transform.scale(bird, (30, 30))



# 색상 변수
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
trail = []
hit_pos = []
bugfix = True


# 물체를 그리는 함수
def draw_object(calc,trail):
    axis = calc[0]
    screen.blit(bird, axis)

    highest_point = [calc[3][2],calc[3][0]]
    highest = font.render(f'MAX(x,y) : ({round(highest_point[0])},{round(highest_point[1])})', True, (0,0,0))

    arrow = pygame.image.load("image/arrow.png")
    arrow = pygame.transform.scale(arrow, (30, 35))
    arrow = pygame.transform.rotate(arrow,calc[2])
    screen.blit(arrow, (screen_width-210,screen_height-85))
    trail.append(axis)

    if axis[0] > highest_point[0] and axis[1] > (screen_height - highest_point[1]):
        pygame.draw.circle(screen, BLUE, [highest_point[0],screen_height-highest_point[1]], 7)
        screen.blit(highest, (highest_point[0] + 15, screen_height-highest_point[1]-30))

    
    for i in range(1, len(trail)):
        if i % 2 == 0:
            pygame.draw.line(screen, RED, trail[i-1], trail[i], 2)


# 초기 설정 값
sec = 0
v0 = 0
angle = 0
start_pos = (50, screen_height-(150)) 

pos1_x = 0  # 마우스 첫 클릭시 x 좌표
pos1_y = 0  # 마우스 첫 클릭시 y 좌표
pos2_x = 0  # 마우스 홀딩 풀때 x 좌표
pos2_y = 0  # 마우스 홀딩 풀때 y 좌표
F = 0 # 새총 당기는 힘


# 물체 위치 계산 함수
def calc(t):
    global start_pos, v0, angle, sec

    theta = m.radians(angle)

    x_pos = start_pos[0] + (v0 * t * m.cos(theta))
    y_pos = start_pos[1] - ((v0 * t * m.sin(theta) - (9.8 * t**2)/2))
    v = ((v0 * m.cos(theta))**2 + (v0 * m.sin(theta) - 9.8*t)**2)**0.5
    angle_radians = m.atan2((v0 * m.sin(theta)) - (9.8 * t), v0 * m.cos(theta))
    angle_degrees = m.degrees(angle_radians)
    T_h = (v0 * m.sin(theta) / 9.8) * 0.5
    R = start_pos[0] + (v0**2 * m.sin(theta) * m.cos(theta)) / 9.8
    H = screen_height-start_pos[1]+((v0**2)*(m.sin(theta))**2)/(2*9.8)

    return ((x_pos,y_pos), (v), (angle_degrees), (H, T_h, R))





bugfix = True
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if len(trail) > 300:
        trail.pop(0)

    
    
    # 화면 업데이트
    screen.fill(WHITE)
    screen.blit(bg, (0,0))
    
    data = calc(sec)


    if event.type == pygame.MOUSEBUTTONDOWN:
         pos1_x , pos1_y = pygame.mouse.get_pos()
         pos1_y = -pos1_y 
         

    if event.type == pygame.MOUSEBUTTONUP:
        
        if bugfix == True:
            start_time = time.time()
            bugfix = False
        
        pos2_x , pos2_y = pygame.mouse.get_pos()
        pos2_y = -pos2_y
        dx = pos2_x - pos1_x
        dy = pos2_y - pos1_y
        
        if dx != 0 and pos1_x != 0 :
            
            F = m.sqrt((pos1_x - pos2_x)**2 + (pos1_y - pos2_y)**2)
            if F > 240:
                F = 240
            if F < 30:
                F = 30
            
            v0 = 100 * (F / 120)
            if dx > 0 and dy > 0:
                angle = (m.degrees(m.atan(dy/dx)) + 180 ) % 360 # 1사분면    # abs() --> 절댓값
            if dx < 0 and dy > 0:
                angle = (m.degrees(m.atan(abs(dx)/dy)) + 90 + 180 ) % 360 # 2사분면
            if dx < 0 and dy < 0:
                angle = (m.degrees(m.atan(dy/dx)) + 180 + 180 ) % 360 # 3사분면
            if dx > 0 and dy < 0:
                angle = (m.degrees(m.atan(dx/abs(dy))) + 270 + 180 ) % 360 # 4사분면
            
    
                
  
        
    if angle != 0: 
        
        # 시간      
        sec = (time.time() - start_time) * 2
        seconds = int(sec)
        time.sleep(0.001)
        draw_object(data, trail) # 포물선 메인 함수
        
    
    # 데이터 랜딩
    font = pygame.font.Font('font/GodoM.ttf',20)

    #timer = font.render(f't : {round(sec * 0.5, 1)}', True, (0,0,0))
    set_val = font.render(f'Setting Value:', True, (255,255,255))
    axis = font.render(f'(x,y) : ({str(round(data[0][0]))},{str((screen_height - round(data[0][1])))})', True, (0,0,0))
    v = font.render(f'v : {str(round(data[1]))}', True, (0,0,0))
    degree = font.render(f'θ : {str(round(data[2]))}', True, (0,0,0))
    show_angle = font.render(f'angle(θ) : {str(round(angle))}°', True, (0,0,0))
    show_V0 = font.render(f'v0 : {str(round(v0))}', True, (0,0,0))
    dist = font.render(f'(R, H, T_H) : ({str(round(data[3][2]))}, {str(round(data[3][0]))}, {round((data[3][1]),1)}s)', True, (0,0,0))

    # 화면 표시
    screen.blit(set_val, (10,10))
    screen.blit(show_angle, (10,40))
    screen.blit(show_V0, (10,70))
    
    #screen.blit(timer, (screen_width-280,screen_height-180))
    screen.blit(axis, (screen_width-280,screen_height-140))
    screen.blit(dist, (screen_width-280,screen_height-110))
    screen.blit(degree, (screen_width-280,screen_height-80))
    screen.blit(v, (screen_width-280,screen_height-50))
    
    
    

    # 화면 업데이트
    pygame.display.update()
    
    # 0.02초 대기
    pygame.time.wait(20)

# 종료
pygame.quit()