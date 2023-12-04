import pygame

class World():
    def __init__(self,data, map_image):
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.image = map_image

#Здесь обрабатывается JSON-файл, чтобы получить x y для waypoint`a(точки, по которым ходит враг)
    def process_data(self):
        for layer in self.level_data['layers']:
            if layer['name'] == 'tilemap':
                self.tile_map = layer['data']
            if layer['name'] == 'waypoints':
                for objects in layer['objects']:
                    waypoint_data = objects['polyline']
                    self.process_waypoints(waypoint_data)

    def process_waypoints(self,data):
        for point in data:
            temporary_x = point.get('x')
            temporary_y = point.get('y')
            print((temporary_x,temporary_x))
            self.waypoints.append((temporary_x,temporary_y))


    def draw(self,surface):
        surface.blit(self.image,(0,0))