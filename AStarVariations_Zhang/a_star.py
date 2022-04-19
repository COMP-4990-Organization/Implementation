# a_star.py

import sys
import time

import numpy as np

from matplotlib.patches import Rectangle

import point
import random_map


class AStar:
    def __init__(self, map, startX, startY, endX, endY):
        self.map = map
        self.open_set = []
        self.close_set = []

        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY

        self.const1 = np.sqrt(2)

    '''def BaseCost(self, p):
        x_dis = abs(p.x - self.startX)
        y_dis = abs(p.y - self.startY)
        # Distance to start point
        #return x_dis + y_dis + (self.const1 - 2) * min(x_dis, y_dis)
        #return x_dis+y_dis'''


    def HeuristicCost(self, p):
        x_dis = abs(self.endX - p.x)
        y_dis = abs(self.endY - p.y)
        # Distance to end point
        #return x_dis + y_dis + (self.const1 - 2) * min(x_dis, y_dis)
        #return x_dis+y_dis
        return max(x_dis, y_dis)

    def TotalCost(self, p):
        return p.cost + self.HeuristicCost(p)

    def IsValidPoint(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= self.map.size or y >= self.map.size:
            return False
        return not self.map.IsObstacle(x, y)

    def IsInPointList(self, p, point_list):
        for point in point_list:
            if point.x == p.x and point.y == p.y:
                return True
        return False

    def IsInOpenList(self, p):
        return self.IsInPointList(p, self.open_set)

    def IsInCloseList(self, p):
        return self.IsInPointList(p, self.close_set)

    def IsStartPoint(self, p):
        #return p.x == 0 and p.y ==0
        return p.x == self.startX and p.y == self.startY

    def IsEndPoint(self, p):
        #return p.x == self.map.size-1 and p.y == self.map.size-1
        return p.x == self.endX and p.y == self.endY

    def SaveImage(self, plt):
        millis = int(round(time.time() * 1000))
        filename = './test/' + str(millis) + '.png'
        plt.savefig(filename)

    def ProcessPoint(self, x, y, parent):
        if not self.IsValidPoint(x, y):
            return  # Do nothing for invalid point
        p = point.Point(x, y)
        if self.IsInCloseList(p):
            return  # Do nothing for visited point
        #print('Process Point [', p.x, ',', p.y, ']', ', cost: ', p.cost)
        if not self.IsInOpenList(p):
            p.parent = parent
            dist = abs(parent.x - p.x) + abs(parent.y - p.y)
            if dist == 2:
                p.cost = parent.cost + self.const1
            else:
                p.cost = parent.cost + 1
            self.open_set.append(p)
            print('Process Point [', p.x, ',', p.y, ']', ', cost: ', p.cost)

    def SelectPointInOpenList(self):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for p in self.open_set:
            cost = self.TotalCost(p)
            if cost < min_cost:
                min_cost = cost
                selected_index = index
            index += 1
        return selected_index

    def BuildPath(self, p, ax, plt, start_time):
        path = []
        while True:
            path.insert(0, p)  # Insert first
            if self.IsStartPoint(p):
                break
            else:
                p = p.parent
        for p in path:
            rec = Rectangle((p.x, p.y), 1, 1, color='orange')
            ax.add_patch(rec)
        plt.draw()
        self.SaveImage(plt)
        end_time = time.time()
        usedtime = end_time - start_time
        print("===== Algorithm finish in %.3f" % usedtime, ' seconds. Length of path: ', p.cost)

    # a_star.py
    def RunAndSaveImage(self, ax, plt):
        start_time = time.time()

        #start_point = point.Point(0, 0)
        start_point = point.Point(self.startX, self.startY)
        start_point.cost = 0
        self.open_set.append(start_point)

        number = 0
        while True:
            index = self.SelectPointInOpenList()
            if index < 0:
                end_time = time.time()
                usedtime = end_time - start_time
                print('No path found! Running time: %.3f' %usedtime)
                return
            p = self.open_set[index]
            rec = Rectangle((p.x, p.y), 1, 1, color='g')
            ax.add_patch(rec)

            if number % 1 == 0:
                self.SaveImage(plt)
            number += 1

            if self.IsEndPoint(p):
                return self.BuildPath(p, ax, plt, start_time)

            del self.open_set[index]
            self.close_set.append(p)

            # Process all neighbors
            x = p.x
            y = p.y
            #self.ProcessPoint(x - 1, y + 1, p)
            self.ProcessPoint(x - 1, y, p)
            #self.ProcessPoint(x - 1, y - 1, p)
            self.ProcessPoint(x, y - 1, p)
            #self.ProcessPoint(x + 1, y - 1, p)
            self.ProcessPoint(x + 1, y, p)
            #self.ProcessPoint(x + 1, y + 1, p)
            self.ProcessPoint(x, y + 1, p)