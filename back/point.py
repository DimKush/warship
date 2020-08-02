class Movement:
    def __init__(self, curr_value=0.0, delta=0.0, max_value=0.0):
        self.curr = curr_value
        self.max = max_value
        self.delta = delta
        self.moving = 0

    def set_next(self, time: float):
        deltate = self.delta * time
        if self.moving == 0:
            if self.curr > 0:
                if self.curr > deltate:
                    self.curr -= deltate
                else:
                    self.curr = 0
            elif self.curr < 0:
                if abs(self.curr) > deltate:
                    self.curr += deltate
                else:
                    self.curr = 0
        elif self.moving == 1:
            new_curr = self.curr + self.moving * deltate
            self.curr = self.max if new_curr >= self.max else new_curr
        elif self.moving == -1:
            new_curr = self.curr + self.moving * deltate
            self.curr = -self.max if new_curr <= -self.max else new_curr

    @property
    def current(self):
        return self.curr


class AngleMovement(Movement):
    def __init__(self, curr_value=0, delta=0, max_value=0, angle_curr=0):
        super().__init__(curr_value=curr_value,
                         delta=delta,
                         max_value=max_value)
        self.angle_curr = angle_curr

    def set_next(self, time: float):
        deltate = self.delta * time
        if self.moving == 0:
            if abs(self.curr) < deltate:
                self.curr = 0
            else:
                if self.curr > 0:
                    self.curr -= deltate
                elif self.curr < 0:
                    self.curr += deltate
        elif self.moving == 1:
            new_curr = self.curr + self.moving * deltate
            self.curr = self.max if new_curr >= self.max else new_curr
        elif self.moving == -1:
            new_curr = self.curr + self.moving * deltate
            self.curr = -self.max if new_curr <= -self.max else new_curr
        self.angle_curr += self.curr * time

    @property
    def angle_current(self):
        return self.angle_curr
