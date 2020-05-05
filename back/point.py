from math import pi


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Movement:
    def __init__(self, curr_value=0, delta=0, max_value=0):
        self.curr = curr_value
        self.max = max_value
        self.delta = delta
        self.moving = 0

    def set_next(self, time: float):
        if self.moving == 0:
            self.curr = 0
        else:
            new_curr = self.delta * self.moving
            self.curr = self.max if new_curr >= self.max else new_curr

    @property
    def current(self):
        return self.curr


class AngleMovement(Movement):
    def __init__(self, curr_value=0, delta=0, max_value=0):
        super().__init__(curr_value, delta, max_value)
        self.angle_curr = 0

    def set_next(self, time: float):
        if self.moving == 0:
            self.curr = 0
        else:
            new_curr = self.delta * self.moving * pi / 180
            self.curr = self.max if new_curr >= self.max else new_curr
            self.angle_curr += self.curr

    @property
    def current(self):
        return self.curr

    @property
    def angle_current(self):
        return self.angle_curr
