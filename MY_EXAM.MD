question 1: added a #Square mixing constant
                            SQUARE_MIX = [
                                (5, 25),
                                (10, 10),
                                (30, 4),
                            ]
question 2: added a function to respawn the squares
                                            self.x = random.randint(0, max(0, self.screen_width - self.size))
                                            self.y = random.randint(0, max(0, self.screen_height - self.size))
                                            self.vx = random.choice([-1, 1]) * random.uniform(MIN_VELOCITY, MAX_VELOCITY)
                                            self.vy = random.choice([-1, 1]) * random.uniform(MIN_VELOCITY, MAX_VELOCITY) 

question 3: 