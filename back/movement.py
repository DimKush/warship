class Movement:
    def __init__(self, curr_value=0.0, delta=0.0, max_value=0.0):
        self.current = curr_value
        self.max = max_value
        self.delta = delta
        self.moving = 0

    def update(self, time: float):
        deltate = self.delta * time
        if self.moving == 0:
            if abs(self.current) < deltate:
                self.current = 0
            else:
                if self.current > 0:
                    self.current -= deltate
                elif self.current < 0:
                    self.current += deltate
                else:
                    pass
        elif self.moving == 1:
            new_curr = self.current + self.moving * deltate
            self.current = self.max if new_curr >= self.max else new_curr
        elif self.moving == -1:
            new_curr = self.current + self.moving * deltate
            self.current = -self.max if new_curr <= -self.max else new_curr
        else:
            pass
