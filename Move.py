class Move:
    def __init__(self, name, poke_type, power, power_points=1):
        self.name = name
        self.poke_type = poke_type
        self.power = int(power)
        self.power_points = power_points
