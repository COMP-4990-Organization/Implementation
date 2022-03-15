
import pygame
from queue import PriorityQueue
from math import sqrt

class ASTAR:

    # Euclidean distance heuristic
    def h(self,p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        #return abs(x1 - x2) + abs(y1 - y2)
        return int(sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2)))

        
    # Used for searching without the use of pygame
    def searchT(self, grid, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid.grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in grid.grid for spot in row}
        f_score[start] = self.h(start.get_pos(), end.get_pos())
        visited_set = {None}

        open_set_hash = {start}
        
        while not open_set.empty():
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if(visited_set.__contains__(current)):
                continue

            if current == end:
                start.make_start()
                end.make_end()
                # print("AStar: Nodes opened = " + str(count))
                return came_from, count
            
            for neighbour in current.neighbours:
                temp_g_score = g_score[current] + neighbour.weight

                if temp_g_score < g_score[neighbour]and not(visited_set.__contains__(neighbour)):
                    came_from[neighbour] = current
                    g_score[neighbour] = temp_g_score
                    f_score[neighbour] = temp_g_score + self.h(neighbour.get_pos(), end.get_pos())
                    if neighbour not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbour], count, neighbour))
                        open_set_hash.add(neighbour)
                        neighbour.make_open()

            if current != start:
                current.make_closed()

            visited_set.add(current)
        return {}, count


    def astar(self, draw, heuristic, grid, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid.grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in grid.grid for spot in row}
        f_score[start] = heuristic(start.get_pos(), end.get_pos())

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                break
            
            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()
            
            draw()

            if current != start:
                current.make_closed()

        return False