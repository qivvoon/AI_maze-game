import pygame
from pygame.locals import *
import pygame_gui
import argparse
import radiobox
import clickActions
import aStarAlgorithm

# python main.py --M [] --N [] --WallNum [] 입력 시, command에서 인수 값 받을 수 있음
# ex) python main.py --M 20 --N 20
parser = argparse.ArgumentParser(description='command line value')
parser.add_argument('--M', default=10)
parser.add_argument('--N', default=10)
parser.add_argument('--WallNum', default=0.2)

args = parser.parse_args()

M = int(args.M)
N = int(args.N)
wall_num = int(args.WallNum * M * N)  # inc_obstacle_ratio 개수
print("M = ", M)
print("N = ", N)
print("장애물 개수 = ", wall_num)

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0) 
GRAY = (127, 127, 127) 
NAVY = (0, 50, 150) 
YELLOW = (255,255,0)

world_width = 800
world_height = 600

screen = pygame.display.set_mode((world_width, world_height))
pygame.display.set_caption('A* MAZE GAME')
screen.fill(WHITE)

# pygame_gui 사용을 위한 UIManager 생성
manager = pygame_gui.UIManager((world_width, world_height))

maze = [['empty']*M for i in range(N)] # 미로를 empty로 초기화
maze_width = 600 # 미로 가로 길이
maze_height = 400 # 미로 세로 길이
maze_cell_width = maze_width // M # 미로 가로 cell 크기
maze_cell_height = maze_height // N # 미로 세로 cell 크기
print("grid cell 가로 크기 =", maze_cell_width)
print("grid cell 세로 크기 =", maze_cell_height)

x = 20 # 미로의 왼쪽 위 모서리 x 좌표
y = 30 # 미로의 왼쪽 위 모서리 y 좌표

# 버튼 3개 생성
search_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 490, 150, 50), text="Start A* Search", manager=manager)
random_walls_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(240, 490, 150, 50), text="Random walls", manager=manager)
reset_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(430, 490, 150, 50), text="Reset", manager=manager)

# 'Heuristic' 텍스트 생성
font = pygame.font.SysFont(None, 25)
surf = font.render("Heuristic", True, BLACK)
rect = surf.get_rect(x=650, y=45) 
screen.blit(surf, rect)

# radiobox 생성
manhattan_radio = radiobox.Radiobox(screen, 650, 80, 0, caption='Manhattan')
euclidean_radio = radiobox.Radiobox(screen, 650, 100, 0, caption='Eucliden')

radioboxes = []
radioboxes.append(manhattan_radio)
radioboxes.append(euclidean_radio)

# start 지점을 표시하는 box 생성
# x, y 좌표 고정 
start_pos = font.render("S", True, WHITE, NAVY)
start_pos_rec = start_pos.get_rect()
start_pos_rec.x = 20
start_pos_rec.y = 30
maze[0][0] = 'start'

# goal 지점을 표시하는 box 생성
# x, y 좌표 고정 
goal_pos = font.render("G", True, WHITE, NAVY)
goal_pos_rec = goal_pos.get_rect()
goal_pos_rec.x = 620 - maze_cell_width
goal_pos_rec.y = 430 - maze_cell_height
maze[N-1][M-1] = 'goal'


clock = pygame.time.Clock()
running = True
start_pos_drag = False  # start지점을 보여주는 box의 drag 상태를 나타냄
goal_pos_drag = False   # goal지점을 보여주는 box의 drag 상태를 나타냄
heuristic = ''          # 어떤 heuristic을 선택했는 지 보여 줄 변수

while running:
  time_delta = clock.tick(60)/1000.0

  # maze 각각의 칸 상태에 따라 미로의 gui 업데이트
  for i in range(N):
    for j in range(M):
      if maze[i][j] == 'wall':
        pygame.draw.rect(screen, GRAY, [x, y, maze_cell_width, maze_cell_height])
        pygame.draw.rect(screen, BLACK, [x, y, maze_cell_width, maze_cell_height], 2) 
      
      elif maze[i][j] == 'start':
        pygame.draw.rect(screen, WHITE, [x, y, maze_cell_width, maze_cell_height])
        pygame.draw.rect(screen, BLACK, [x, y, maze_cell_width, maze_cell_height], 2)
        screen.blit(start_pos, start_pos_rec)
        
      elif maze[i][j] == 'goal':
        pygame.draw.rect(screen, WHITE, [x, y, maze_cell_width, maze_cell_height])
        pygame.draw.rect(screen, BLACK, [x, y, maze_cell_width, maze_cell_height], 2)
        screen.blit(goal_pos, goal_pos_rec)
      
      elif maze[i][j] == 'path':
        pygame.draw.rect(screen, YELLOW, [x, y, maze_cell_width, maze_cell_height])
        pygame.draw.rect(screen, BLACK, [x, y, maze_cell_width, maze_cell_height], 2)
        screen.blit(start_pos, start_pos_rec)
        screen.blit(goal_pos, goal_pos_rec)
        
      else:
        pygame.draw.rect(screen, WHITE, [x, y, maze_cell_width, maze_cell_height])
        pygame.draw.rect(screen, BLACK, [x, y, maze_cell_width, maze_cell_height], 2)   
          
      x += maze_cell_width
      
    x = 20
    y += maze_cell_height 
  x = 20
  y = 30 
  
  
  for event in pygame.event.get():
    
    if event.type == pygame.QUIT:
      running = False
      
    elif event.type == pygame.MOUSEBUTTONDOWN:
      
      maze_cell_down = pygame.mouse.get_pos()
      
      # 클릭한 곳이 maze의 start 또는 goal 지점이라면, empty로 변경
      for i in range(N):
        for j in range(M):
          if (x <= maze_cell_down[0] <= (x+maze_cell_width)) and (y <= maze_cell_down[1] <= (y+maze_cell_height)):
            if maze[i][j] == 'start':
              maze[i][j] = 'empty'
              start_pos_drag = True

            elif maze[i][j] == 'goal':
              maze[i][j] = 'empty'
              goal_pos_drag = True
                
          x += maze_cell_width
        x = 20
        y += maze_cell_height
      x = 20
      y = 30 
      
      # 클릭한 곳이 radiobox라면, radiobox 상태 변경 및 선택된 heuristic 함수 저장
      if (650 <= maze_cell_down[0] <= 662) and (80 <= maze_cell_down[1] <= 92):
        radioboxes[0]._update(radioboxes)
        heuristic = 'manhattan'
        print("[clicked Manhattan]")
      elif (650 <= maze_cell_down[0] <= 662) and (100 <= maze_cell_down[1] <= 112):
        radioboxes[1]._update(radioboxes)
        heuristic = 'euclidean'
        print("[clicked Euclidean]")
    
      
    elif event.type == pygame.MOUSEBUTTONUP:
      
      maze_cell_up = pygame.mouse.get_pos()
      
      # start 지점을 이동시킨 후, 마우스 커서를 up 했을 시,
      # 그 지점에 해당하는 미로 칸을 start 지점으로 변경 
      if start_pos_drag:
        for i in range(N):
          for j in range(M):
            if (x <= maze_cell_up[0] <= (x+maze_cell_width)) and (y <= maze_cell_up[1] <= (y+maze_cell_height)):
              maze[i][j] = 'start'
              start_pos_drag = False
              # 마우스 커서를 중심으로 start 지점을 나타내는 박스가 그려지도록 설정
              start_pos_rec.x = maze_cell_up[0] - (start_pos_rec.width // 2)
              start_pos_rec.y = maze_cell_up[1] - (start_pos_rec.height // 2)
              print("[start position drag]")
              break
            x += maze_cell_width
            
          x = 20
          y += maze_cell_height
        x = 20
        y = 30 
        
      # goal 지점을 이동시킨 후, 마우스 커서를 up 했을 시,
      # 그 지점에 해당하는 미로 칸을 goal 지점으로 변경  
      if goal_pos_drag:
        for i in range(N):
          for j in range(M):
            if (x <= maze_cell_up[0] <= (x+maze_cell_width)) and (y <= maze_cell_up[1] <= (y+maze_cell_height)):
              maze[i][j] = 'goal'
              goal_pos_drag = False
              # 마우스 커서를 중심으로 goal 지점을 나타내는 박스가 그려지도록 설정
              goal_pos_rec.x = maze_cell_up[0] - (goal_pos_rec.width // 2)
              goal_pos_rec.y = maze_cell_up[1] - (goal_pos_rec.height // 2)
              print("[goal position drag]")
              break
            x += maze_cell_width
            
          x = 20
          y += maze_cell_height
        x = 20
        y = 30 
      
      # 장애물 랜덤 배치
      # drag 시, 실행 되지 않음
      if (maze_cell_down[0] == maze_cell_up[0]) and (maze_cell_down[1] == maze_cell_up[1]):
        if (20 <= maze_cell_down[0] <= 620) and (30 <= maze_cell_down[1] <= 430):
          maze = clickActions.ChoiceWalls(maze, maze_cell_up, N, M, x, y, maze_cell_width, maze_cell_height)
    
    
    # pygame_gui를 이용해 만든 3개의 버튼 클릭 감지
    # 클릭으로 인해 변경된 미로의 상태를 maze에 저장
    elif event.type == pygame_gui.UI_BUTTON_PRESSED: 
         
      if event.ui_element == random_walls_btn:
        print("[Random walls btn clicked]")
        maze = clickActions.RandomWalls(maze, wall_num, N, M)
      
      elif event.ui_element == reset_btn:
        print("[Reset btn clicked]")
        maze = clickActions.Reset(maze, N, M)
        
        # start 지점과 goal 지점 reset
        start_pos_rec.x = 20
        start_pos_rec.y = 30
        
        goal_pos_rec.x = 620 - maze_cell_width
        goal_pos_rec.y = 430 - maze_cell_height 
        
      elif event.ui_element == search_btn:
        print("[search btn clicked]")
        maze = aStarAlgorithm.AStar(maze, N, M, heuristic)        
    
    # pygame_gui 이용해 생성한 버튼의 event 감지를 위해 필요    
    manager.process_events(event)

  # radiobox를 screen에 그림
  for radiobox in radioboxes:
    radiobox.render_radiobox()
  
  manager.update(time_delta)
  manager.draw_ui(screen)
  pygame.display.update()
            
pygame.quit()