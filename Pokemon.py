class Pokemon:
    def __init__(self, name, poke_type, hit_points, attack, defense, moves):
        self.name = name
        self.poke_type = poke_type
        self.hit_points = int(hit_points)
        self.max_hit_points = int(hit_points)
        self.attack = int(attack)
        self.defense = int(defense)
        self.moves = moves

