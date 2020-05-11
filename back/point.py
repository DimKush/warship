from math import pi

from json import JSONEncoder


class PointEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Point):
            return obj.x, obj.y
        else:
            return JSONEncoder.default(self, obj)


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Movement:
    def __init__(self, curr_value=0.0, delta=0.0, max_value=0.0):
        self.curr = curr_value
        self.max = max_value
        self.delta = delta
        self.moving = 0

    def set_next(self, time: float):
        if self.moving == 0:
            if self.curr > 0:
                self.curr -= self.delta* time
            elif self.curr < 0:
                self.curr += self.delta* time
        elif self.moving == 1:
            new_curr = self.curr + self.delta * self.moving * time
            self.curr = self.max if new_curr >= self.max else new_curr
        elif self.moving == -1:
            new_curr = self.curr + self.delta * self.moving * time
            self.curr = -self.max if new_curr <= -self.max else new_curr

    @property
    def current(self):
        return self.curr


class AngleMovement(Movement):
    def __init__(self, curr_value=0, delta=0, max_value=0):
        super().__init__(curr_value=curr_value,
                         delta=delta * pi / 180,
                         max_value=max_value * pi / 180)
        self.angle_curr = 0

    def set_next(self, time: float):
        delta_time = self.delta * time
        if self.moving == 0:
            if abs(self.curr) < delta_time:
                self.curr = 0
            else:
                if self.curr > 0:
                    self.curr -= delta_time
                elif self.curr < 0:
                    self.curr += delta_time
        elif self.moving == 1:
            new_curr = self.curr + self.moving * delta_time
            self.curr = self.max if new_curr >= self.max else new_curr
        elif self.moving == -1:
            new_curr = self.curr + self.moving * delta_time
            self.curr = -self.max if new_curr <= -self.max else new_curr
        self.angle_curr += self.curr

    @property
    def angle_current(self):
        return self.angle_curr
