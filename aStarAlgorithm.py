from math import sqrt

# 블로그 [PROGRAMMING PER SE] 참조
# https://choiseokwon.tistory.com/210
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def Manhattan(child, goalNode): 
    dx = abs(child.position[0] - goalNode.position[0])
    dy = abs(child.position[1] - goalNode.position[1])
    return dx + dy


def Euclidean(child, goalNode):
    dxy = ((child.position[0] - goalNode.position[0]) ** 2) + ((child.position[1] - goalNode.position[1]) ** 2)
    dxy =   round(sqrt(dxy), 2) # dxy 루트 계산 후, 소수점 둘째 자리까지 반올림
    return dxy
    
    
def AStar(maze, N, M, heuristic):
    for i in range(N):
        for j in range(M):
            if maze[i][j] == 'start':
                start = (i, j)
                
            elif maze[i][j] == 'goal':
                goal = (i, j)
    
    # start_node와 goal_node 초기화
    start_node = Node(None, start)
    goal_node = Node(None, goal)

    # openList와 closedList 초기화
    open_list = []
    closed_list = []

    # openList에 시작 노드 추가
    open_list.append(start_node)
    
    # 경로를 찾기 위해 탐색 된 노드 개수를 위한 변수
    explored_node = 0
    
    # goal을 찾을 때까지 실행
    while open_list:

        # 현재 노드 지정
        current_node = open_list[0]
        current_index = 0

        # open_list에 있는 노드들 중, 현재 노드와 비교 시
        # 가장 작은 f값을 가지는 노드를 current_node로 지정
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # 비교 전 current_node를 open_list에서 제거하고, 
        # closed_list에 추가
        open_list.pop(current_index)
        closed_list.append(current_node)

        # 현재 노드가 목적지면, current_node의 부모로 이동하며
        # 노드의 위치를 path에 append
        if current_node == goal_node:
            print("find goal!")
            print(heuristic, '이용')
            print('탐색된 노드는 총', explored_node, '개')
            path = []
            current = current_node
            while current is not None:

                x, y = current.position
                maze[x][y] = 'path'

                path.append(current.position)
                current = current.parent
            
            path = path[::-1] # reverse
            return maze

        children = []
        # 현재 노드와 인접한 노드 탐색
        for adjacent_pos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            
            # 노드 위치 업데이트
            node_pos = (
                current_node.position[0] + adjacent_pos[0],  # X
                current_node.position[1] + adjacent_pos[1])  # Y
                
            # 미로의 index 범위 안의 노드들만 탐색하도록 함
            within_range = [
                node_pos[0] > (len(maze) - 1),
                node_pos[0] < 0,
                node_pos[1] > (len(maze[len(maze) - 1]) - 1),
                node_pos[1] < 0,
            ]
            
            if any(within_range): 
                continue

            # 장애물은 탐색하지 않음
            if maze[node_pos[0]][node_pos[1]] == 'wall':
                continue

            new_node = Node(current_node, node_pos)
            children.append(new_node)
        
        # 인접한 노드의 F 계산     
        for child in children:

            # child가 closed_list에 있으면 계산X
            if child in closed_list:
                continue

            # F, G, H값 계산
            child.g = current_node.g + 1

            # 선택 된 Heuristic 함수로 거리 계산
            if heuristic == 'manhattan':
                child.h = Manhattan(child, goal_node)

            elif heuristic == 'euclidean':
                child.h = Euclidean(child, goal_node)
            
            child.f = child.g + child.h
            explored_node += 1
            
            # child가 open_list에 있고, 
            # g값이 open_list의 노드들 보다 크면 continue
            if len([openNode for openNode in open_list
                    if child == openNode and child.g > openNode.g]) > 0:
                continue
                    
            open_list.append(child)
            
        
    # 길을 찾으면 return으로 인해 바로 종료됨
    # 따라서, 아래의 코드를 실행한다는 것은 길을 찾지 못했다는 뜻
    print("can not find goal")
    print(heuristic, '이용')
    print('탐색된 노드는 총 ', explored_node,'개') 
    path = []
    current = current_node
    while current is not None:
        x, y = current.position
        maze[x][y] = 'path'
        path.append(current.position)
        current = current.parent
            
    path = path[::-1]
    return maze
         