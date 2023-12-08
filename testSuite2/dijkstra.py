
import heapq


def dijkstra_with_predecessors(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    predecessors = {node: None for node in graph}
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return distances, predecessors


def backtrack_path(predecessors, start, end):
    path = []
    current_node = end
    while current_node != start:
        path.append(current_node)
        current_node = predecessors[current_node]
        if current_node is None:
            # No path exists between start and end
            return None
    path.append(start)
    path.reverse()
    return path


def draw_path_on_image(image, path, color_value):
    # Assuming a 3-channel color image and the path color value is a tuple (R, G, B)
    for position in path:
        image[position[0], position[1]] = color_value
    return image
