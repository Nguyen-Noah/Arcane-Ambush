import pygame

class QuadTree:
    def __init__(self, capacity, boundary):
        self.capacity = capacity
        self.boundary = boundary
        self.entities = []

        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
    
    def subdivide(self):
        parent = self.boundary

        boundary_nw = Rectangle(
            pygame.math.Vector2(
                parent.position.x,
                parent.position.y
                ),
            parent.scale / 2
            )
        boundary_ne = Rectangle(
            pygame.math.Vector2(
                parent.position.x + parent.scale.x / 2,
                parent.position.y
                ),
            parent.scale / 2
            )
        boundary_sw = Rectangle(
            pygame.math.Vector2(
                parent.position.x,
                parent.position.y + parent.scale.y / 2
                ),
            parent.scale / 2
            )
        boundary_se = Rectangle(
            pygame.math.Vector2(
                parent.position.x + parent.scale.x / 2,
                parent.position.y + parent.scale.y / 2
                ),
            parent.scale / 2
            )
        
        self.nw = QuadTree(self.capacity, boundary_nw)
        self.ne = QuadTree(self.capacity, boundary_ne)
        self.sw = QuadTree(self.capacity, boundary_sw)
        self.se = QuadTree(self.capacity, boundary_se)

        for entity in range(len(self.entities)):
            self.nw.insert(self.entities[entity])
            self.ne.insert(self.entities[entity])
            self.sw.insert(self.entities[entity])
            self.se.insert(self.entities[entity])

    def insert(self, entity):
        if not self.boundary.contains_entity(entity):
            return False
        
        if len(self.entities) < self.capacity and not self.nw:
            self.entities.append(entity)
            return True
        else:
            if not self.nw:
                self.subdivide()
        
            if self.nw.insert(entity):
                return True
            if self.ne.insert(entity):
                return True
            if self.sw.insert(entity):
                return True
            if self.se.insert(entity):
                return True
            
        return False
    
    def query_range(self, range):
        entities_in_range = []

        if not range.intersects(self.boundary):
            return entities_in_range
        
        for entity in self.entities:
            if range.contains_entity(entity):
                entities_in_range.append(entity)
            
        if self.nw:
            entities_in_range += self.nw.query_range(range)
            entities_in_range += self.ne.query_range(range)
            entities_in_range += self.sw.query_range(range)
            entities_in_range += self.se.query_range(range)
            
class Rectangle:
    def __init__(self, position, scale):
        self.position = position
        self.scale = scale

    def contains_entity(self, entity):
        x, y = entity.pos
        bx, by = self.position
        w, h = self.scale
        if x >= bx and x <= bx + w and y >= by and y <= by + h:
            return True
        else:
            return False
        
class Circle:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius
        self.sqradius = self.radius * self.radius
        self.scale = None

    def contains_entity(self, particle):
        x1, y1 = self.position
        x2, y2 = particle.position
        dist = pow(x2 - x1, 2) + pow(y2 - y1, 2)
        if dist <= self.sqradius:
            return True
        else:
            return False
        
    def intersects(self, _range):
        x1, y1 = self.position
        x2, y2 = _range.position
        w, h = _range.scale
        r = self.radius
        dist_x, dist_y = abs(x2 - x1), abs(y2 - y1)

        edges = pow(dist_x - w, 2) + pow(dist_y - h, 2)

        if dist_x > (r + w) or dist_y > (r + h):
            return False

        if dist_x <= w or dist_y <= h:
            return True

        return (edges <= self.sqradius)

""" class QuadTreeNode:
    def __init__(self, x, y, width, height, depth=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.depth = depth
        self.entities = []  # List of entities in this node
        self.children = []  # List of four child nodes

def insert_entity(node, entity):
    # Insert an entity into the quadtree
    print(node)
    print('node children', len(node.children))
    print('node entities', len(node.entities))
    if len(node.children) == 0 and len(node.entities) < 4:
        # If the node is a leaf and has room for the entity, add it to the node
        node.entities.append(entity)
    else:
        # If the node is not a leaf, insert the entity into the appropriate child node
        index = get_quadrant_index(node, entity.center[0], entity.center[1])
        if len(node.children) == 0:
            sub_width = node.width / 2
            sub_height = node.height / 2
            node.children = [None] * 4
            node.children[index] = QuadTreeNode(
                node.x + (index % 2) * sub_width,
                node.y + (index // 2) * sub_height,
                sub_width, sub_height, node.depth + 1
            )
        insert_entity(node.children[index], entity)

def get_quadrant_index(node, x, y):
    # Determine the index of the quadrant in which the point (x, y) belongs
    mid_x = node.x + node.width / 2
    mid_y = node.y + node.height / 2
    index = 0
    if x > mid_x:
        index += 1
    if y > mid_y:
        index += 2
    print('index', index)
    return index

def find_nearest_entity(node, x, y, radius, nearest_entity=None, nearest_distance=float('inf')):
    # Recursively find the nearest entity within the specified radius from the point (x, y)
    for entity in node.entities:
        distance = ((entity.center[0] - x) ** 2 + (entity.center[1] - y) ** 2) ** 0.5
        if distance < nearest_distance and distance <= radius:
            nearest_entity = entity
            nearest_distance = distance

    for child in node.children:
        if child is not None and intersects_circle(child, x, y, radius):
            nearest_entity, nearest_distance = find_nearest_entity(
                child, x, y, radius, nearest_entity, nearest_distance
            )

    return nearest_entity, nearest_distance

def intersects_circle(node, x, y, radius):
    # Check if the circle centered at (x, y) with the given radius intersects with the node's bounds
    dx = abs(x - max(node.x, min(x, node.x + node.width)))
    dy = abs(y - max(node.y, min(y, node.y + node.height)))
    return dx ** 2 + dy ** 2 < radius ** 2
 """
