import random

# 랜덤으로 미로의 장애물을 만들어 주는 함수
def RandomWalls(maze, wall_num, N, M):
  
  # start_btn 연속 클릭 시, 전 클릭으로 인해 생성된 장애물이 maze에 남아있음
  # 따라서, maze의 모든 칸을 다시 0으로 만듦
  # 이 때, start, goal 칸은 현재 상태 그대로 유지
  for i in range(N):
    for j in range(M):
      if (maze[i][j] == 'start') or (maze[i][j] == 'goal'):
        continue
      else:
        maze[i][j] = 'empty'

  # 랜덤으로 maze의 index를 추출하여 장애물 개수만큼 장애물 생성
  while wall_num > 0:
    random_width = random.randint(0, M-1)
    random_height = random.randint(0, N-1)
    
    if maze[random_height][random_width] == 'empty':
      maze[random_height][random_width] = 'wall'
      wall_num -= 1
    
  return maze
   
   
# 미로를 reset 해주는 함수    
def Reset(maze, N, M):

  for i in range(N):
    for j in range(M):
      maze[i][j] = 'empty'
  
  maze[0][0] = 'start'
  maze[N-1][M-1] = 'goal'
  
  return maze
 
 
# 사용자가 장애물을 선택할 수 있도록 해주는 함수
# 비어있는 칸 클릭 시, 장애물로 변경
# 장애물 클릭 시, 비어있는 칸으로 변경    
def ChoiceWalls(maze, mouse, N, M, x, y, maze_cell_width, maze_cell_height):
  
  for i in range(N):
    for j in range(M):
      if (x <= mouse[0] <= (x+maze_cell_width)) and (y <= mouse[1] <= (y+maze_cell_height)):
        
        if maze[i][j] == 'wall':
          maze[i][j] = 'empty'
          print("[clicked cell for random wall] wall -> empty")
          break
        
        elif maze[i][j] == 'empty':
          maze[i][j] = 'wall'
          print("[clicked cell for random wall] empty -> wall")
          break
          
      x += maze_cell_width
    x = 20
    y += maze_cell_height
  
  return maze
  