from entity import Entity, Action
import random

class InimigoQueBate(Entity):
    def ataque(self, target):       
        target.take_damage(self.damage)

    
    def __init__(self, name, health, attack_name, damage):
        self.damage = damage
        Entity.__init__(self, name, health, [Action(attack_name, "Causa " + str(damage) + " dano", True, self.ataque)])
                
class Minibruxo(Entity):
    def habilidade(self, all_entities):
        most_damaged = self
        most_damage = 0
        for entity in all_entities[1]:
            if entity.max_health - entity.health > most_damage:
                most_damage = entity.max_health - entity.health
                most_damaged = entity
        most_damaged.take_damage(-2)

    
    def __init__(self):
        Entity.__init__(self, "Minibruxo", 2,
                      [Action("Cura", "Cura 2HP para o inimigo mais ferido. Alvo inalterável", False, self.habilidade)]
                      )

class Vampiro(Entity):
    def habilidade(self, target):       
        target.take_damage(1)
        self.take_damage(-1)

    
    def __init__(self):
        Entity.__init__(self, "Vampiro", 3,
                      [Action("Mordida", "Causa 1 dano, Vampiro recupera 1HP", True, self.habilidade)]
                      )

class Vibora(Entity):
    def habilidade(self, all_entities):       
        for entity in all_entities[0]:
            entity.take_damage(1)

    
    def __init__(self):
        Entity.__init__(self, "Vibora", 2,
                      [Action("Ácido", "Causa 1 dano contra todos Heróis", False, self.habilidade)]
                      )

class Shaman(Entity):
    def habilidade(self, all_entities):       
        for entity in all_entities[0]:
            entity.set_damage_multiplier(entity.damage_multiplier*2)

    
    def __init__(self):
        Entity.__init__(self, "Shaman", 2,
                      [Action("Ritual", "Heróis levam dano dobrado de inimigos depois do Shaman", False, self.habilidade)]
                      )

class Ogro(Entity):
    def habilidade(self, target):       
        target.take_damage(self.max_health-self.health)

    
    def __init__(self):
        Entity.__init__(self, "Ogro", 4,
                      [Action("Machado", "Causa dano igual ao HP faltante do Ogro", True, self.habilidade)]
                      )

class Haeldra(Entity):
    def ignicao(self, target):       
        target.take_damage(2)

    def agonia(self, all_entities):       
        for entity in all_entities[0]:
            entity.take_damage(1)
        for entity in all_entities[1]:
            entity.take_damage(1)

    
    def __init__(self):
        Entity.__init__(self, "Haeldra", 18,
                      [Action("Ignição", "Causa 2 dano", True, self.ignicao), Action("Agonia", "Causa 1 dano contra todos no campo", False, self.agonia)]
                      )

def Corvo():
    return InimigoQueBate("Corvo", 1, "Mordida", 1)

def Orc():
    return InimigoQueBate("Orc", 3, "Martelo", 2)

def Corrupto():
    return InimigoQueBate("Corrupto", 2, "Bastão", 1)

