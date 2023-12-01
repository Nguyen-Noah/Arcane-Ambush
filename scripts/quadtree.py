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
    
    def query_closest(self, range, pos):
        target_entity = None
        closest_distance_squared = float('inf')

        if not range.intersects(self.boundary):
            return target_entity
        
        for entity in self.entities:
            if range.contains_entity(entity):
                distance_squared = (entity.pos[0] - pos[0])**2 + (entity.pos[1] - pos[1])**2
                if distance_squared < closest_distance_squared:
                    target_entity = entity
                    closest_distance_squared = distance_squared

        if self.nw:
            for child in [self.nw, self.ne, self.sw, self.se]:
                child_closest_entity = child.query_closest(range, pos)
                if child_closest_entity:
                    distance_squared = (entity.pos[0] - pos[0])**2 + (entity.pos[1] - pos[1])**2
                    if distance_squared < closest_distance_squared:
                        target_entity = entity
                        closest_distance_squared = distance_squared

        return target_entity

    def query_range(self, range):
        entities_in_range = set()

        if not range.intersects(self.boundary):
            return list(entities_in_range)
        
        for entity in self.entities:
            if range.contains_entity(entity):
                entities_in_range.add(entity)

        if self.nw:
            entities_in_range.update(self.nw.query_range(range))
            entities_in_range.update(self.ne.query_range(range))
            entities_in_range.update(self.sw.query_range(range))
            entities_in_range.update(self.se.query_range(range))

        return list(entities_in_range)

    def clear(self):
        self.entities = []

        if self.nw:
            self.nw.clear()
            self.ne.clear()
            self.sw.clear()
            self.se.clear()
        
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

    def show(self, surf, offset=(0, 0)):
        self.boundary.draw(surf, offset)

        if self.nw:
            self.nw.show(surf, offset)
            self.ne.show(surf, offset)
            self.sw.show(surf, offset)
            self.se.show(surf, offset)

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
        
    def draw(self, surf, offset=(0, 0)):
        x, y = self.position
        w, h = self.scale
        pygame.draw.rect(surf, (255, 255, 255), [x - offset[0], y - offset[1], w, h], 1)

class Circle:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius
        self.sqradius = self.radius * self.radius
        self.scale = None

    def contains_entity(self, entity):
        x1, y1 = self.position
        x2, y2 = entity.pos
        dist = pow(x2 - x1, 2) + pow(y2 - y1, 2)
        if dist <= self.sqradius:
            return True
        else:
            return False
        
    def intersects(self, range):
        x1, y1 = self.position
        x2, y2 = range.position
        w, h = range.scale
        r = self.radius
        dist_x, dist_y = abs(x2 - x1), abs(y2 - y1)

        edges = pow(dist_x - w, 2) + pow(dist_y - h, 2)

        if dist_x > (r + w) or dist_y > (r + h):
            return False

        if dist_x <= w or dist_y <= h:
            return True

        return (edges <= self.sqradius)
    
    def draw(self, surf, offset=(0, 0)):
        pygame.draw.circle(surf, (0, 0, 0), (self.position[0] - offset[0], self.position[1] - offset[1]), self.radius)