
import pygame
from queue import PriorityQueue

class DIJKSTRA:

    # Used for searching without the use of pygame
    def searchT(self, grid, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid.grid for spot in row}
        g_score[start] = 0
        visited_set = {None}

        open_set_hash = {start}
        
        while not open_set.empty():
            current = open_set.get()[1]
            open_set_hash.remove(current)

            if(visited_set.__contains__(current)):
                continue

            if current == end:
                start.make_start()
                end.make_end()
                return came_from, count
            
            for neighbour in current.neighbours:
                temp_g_score = g_score[current] + neighbour.weight

                if temp_g_score < g_score[neighbour] and not(visited_set.__contains__(neighbour)):
                    came_from[neighbour] = current
                    g_score[neighbour] = temp_g_score
                    if neighbour not in open_set_hash:
                        count += 1
                        open_set.put((g_score[neighbour], neighbour))
                        open_set_hash.add(neighbour)
                        neighbour.make_open()

            if current != start:
                current.make_closed()
            visited_set.add(current)
        return {}, count

    def dijkstra(self, draw, grid, start, end):
        open_set = PriorityQueue()
        open_set.put((0,start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid.grid for spot in row}
        g_score[start] = 0
        visited_set = {None}

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            current = open_set.get()[1]
            open_set_hash.remove(current)

            if(visited_set.__contains__(current)):
                continue

            if current == end:
                print("Total cost of the trip is " + str(g_score[current]))
                break
            
            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + neighbor.weight
                if(neighbor.is_closed()):
                    continue
                if temp_g_score < g_score[neighbor] and not(visited_set.__contains__(neighbor)):
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    if neighbor not in open_set_hash:
                        open_set.put((g_score[neighbor],neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()
            
            draw()

            if current != start:
                current.make_closed()
            visited_set.add(current)
        return False

    def __str__(self) -> str:
        return "DIJKSTRA"