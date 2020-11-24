import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import math


def loadMap(file):
    # Load map txt as matrix.
    # 0: path, 1: obstacle, 2: start point, 3: end point, 4: path
    f = open(file)
    lines = f.readlines()
    numOfLines = len(lines)
    returnMap = np.zeros((numOfLines, 40))

    for i ,line in enumerate(lines):
        for j,val in enumerate(line[0:40]):
            returnMap[i,j] = val
    return returnMap

class Node:
    def __init__(self, parent, x, y, dist):
        self.parent = parent
        self.x = x
        self.y = y
        self.dist = dist


class A_Star:
    def __init__(self, map):
        self.map = map
        self.start_x, self.start_y = 0, 0
        self.end_x, self.end_y = 39, 26
        self.open, self.close = [], []  
        self.path = []

    def a_star(self):
        self.find_path()
        self.mark_path(self.path)
        print(self.path[::-1])
        self.drawMap()

    # 找路徑
    def find_path(self):
        # 起點
        p = Node(None, self.start_x, self.start_y, 0.0)
        while True:
            # extend
            self.extend_round(p)
            # 如果open[]沒東西，代表不存在路徑
            if not self.open:
                return
            # 取F值最小的節點
            idx, p = self.get_best()
            # 到達終點，生成路徑
            if self.is_target(p):
                self.make_path(p)
                return
            # 把節點加入close[]，並從open[]刪掉
            self.close.append(p)
            del self.open[idx]

    # 生成路徑
    def make_path(self, p):
        while p:
            # 從結束的點回到起点，起點的parent == None
            self.path.append((p.x, p.y))
            p = p.parent

    # 標記路徑
    def mark_path(self, path):
        for x, y in path:
            self.map[y, x] = 4

    # 判斷是否為終點
    def is_target(self, i):
        return i.x == self.end_x and i.y == self.end_y

    # 取F值最小的節點
    def get_best(self):
        best = None
        bv = 9999999  # MAX值
        bi = -1
        for idx, i in enumerate(self.open):
            value = self.get_dist(i)
            if value < bv:
                best = i
                bv = value
                bi = idx
            return bi, best

    # 求距離
    def get_dist(self, i):
        # F = G + H
        # G 為當前路徑長度，H為估計的長度
        return i.dist + math.sqrt((self.end_x - i.x) ** 2 + (self.end_y - i.y) ** 2)

    # extend
    def extend_round(self, p):
        # 八個方向
        xs = (-1, 0, 1, -1, 1, -1, 0, 1)
        ys = (-1, -1, -1, 0, 0, 1, 1, 1)
        # 上下左右四個方向
        xs = (0, -1, 1, 0)
        ys = (-1, 0, 0, 1)
        for x, y in zip(xs, ys):
            new_x, new_y = x + p.x, y + p.y
            # 檢查位置是否合理
            if not self.is_valid_coord(new_x, new_y):
                continue
            # 增加新的節點，計算距離
            node = Node(p, new_x, new_y, p.dist + self.get_cost(p.x, p.y, new_x, new_y))
            # 若新的節點在close[]，忽略
            if self.node_in_close(node):
                continue
            i = self.node_in_open(node)
            # 新節點在open[]
            if i != -1:
                # 目前路徑更短
                if self.open[i].dist > node.dist:
                    # 更新距離
                    self.open[i].parrent = p
                    self.open[i].dist = node.dist
                continue
            # 否則加入open[]
            self.open.append(node)

    # 移動距離，直走1.0，斜走1.4
    def get_cost(self, x1, y1, x2, y2):
        if x1 == x2 or y1 == y2:
            return 1.0
        return 1.4

    # 检查节点是否在close表
    def node_in_close(self, node):
        for i in self.close:
            if node.x == i.x and node.y == i.y:
                return True
        return False

    # 检查节点是否在open表，返回序号
    def node_in_open(self, node):
        for i, n in enumerate(self.open):
            if node.x == n.x and node.y == n.y:
                return i
        return -1

    # 判斷位置是否合理，超出邊界或為障礙物
    def is_valid_coord(self, x, y):
        if x < 0 or x > 39 or y < 0 or y > 26:
            return False
        return self.map[y, x] != 1

    def drawMap(self):
        # Visulize the maze map.
        # Draw obstacles(1) as red rectangles. Draw path(0) as white rectangles. Draw starting point(2) and ending point(3) as circles.
        rowNum = len(self.map)
        colNum = len(self.map[0])
        ax = plt.subplot()
        param = 1
        for col in range(colNum):
            for row in range(rowNum):
                if self.map[row, col] == 2:
                    circle = mpathes.Circle([param * col + param / 2.0, param * row + param / 2.0], param / 2.0,
                                            color='g')
                    ax.add_patch(circle)
                elif self.map[row, col] == 3:
                    circle = mpathes.Circle([param * col + param / 2.0, param * row + param / 2.0], param / 2.0,
                                            color='y')
                    ax.add_patch(circle)
                elif self.map[row, col] == 1:
                    rect = mpathes.Rectangle([param * col, param * row], param, param, color='r')
                    ax.add_patch(rect)
                elif self.map[row, col] == 4:
                    rect = mpathes.Rectangle([param * col, param * row], param, param, color='b')
                    ax.add_patch(rect)
                else:
                    rect = mpathes.Rectangle([param * col, param * row], param, param, color='w')
                    ax.add_patch(rect)
        # Improve visualization
        plt.xlim((0, colNum))
        plt.ylim((0, rowNum))
        my_x_ticks = np.arange(0, colNum + 1, 1)
        my_y_ticks = np.arange(0, rowNum + 1, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        axx = plt.gca()
        axx.xaxis.set_ticks_position('top')
        axx.invert_yaxis()
        plt.grid()
        # Save maze image.
        plt.savefig('./A_Star_maze.jpg')


if __name__ == "__main__":
    A_Star(loadMap('maze.txt')).a_star()
