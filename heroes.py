from entity import Entity, Action

class Samurai(Entity):
    def corte(self, target):
        if self.health == 1:
            target.interrupt_order()
        
        target.take_damage(2)

    def defesa(self, all_entities):
        self.set_damage_multiplier(0)

    def reflexo(self, target):
        target.change_target(target)

    
    def __init__(self):
        Entity.__init__(self, "Samurai", 3,
                      [Action("corte", "Causa 2 dano. Interrompe ação se tiver 1HP", True, self.corte),
                       Action("defesa", "Samurai fica imune a dano neste turno", False, self.defesa),
                       Action("reflexo", "Troca o alvo do alvo para si mesmo", True, self.reflexo)]
                      )
                
class Clerigo(Entity):
    def clava(self, target):
        self.set_damage_multiplier(0)
        target.take_damage(1)

    def cura(self, target):
        target.take_damage(-2)

    def grito(self, target):
        target.change_target(self)

    
    def __init__(self):
        Entity.__init__(self, "Paladino", 6,
                      [Action("clava", "Causa 1 dano, Paladino fica imune a dano neste turno", True, self.clava),
                       Action("cura", "Cura 2HP", True, self.cura),
                       Action("grito", "Troca o alvo do alvo para o Paladino", True, self.grito)]
                      )

class Feiticeiro(Entity):
    def fogo(self, target):       
        target.take_damage(3)

    def tempestade(self, all_entities):
        for entity in all_entities[1]:
            entity.take_damage(1)

    def escudo(self, target):
        target.set_damage_multiplier(0)

    
    def __init__(self):
        Entity.__init__(self, "Feiticeiro", 2,
                      [Action("fogo", "Causa 3 dano", True, self.fogo),
                       Action("tempestade", "Causa 1 dano contra todos inimigos", False, self.tempestade),
                       Action("escudo", "Alvo fica imune a dano neste turno", True, self.escudo)]
                      )

class Bruxo(Entity):
    def medo(self, target):
        target.set_damage_multiplier(2)

    def choque(self, target):
        target.interrupt_order()

    def vampiro(self, target):
        target.take_damage(1)
        self.take_damage(-1)

    
    def __init__(self):
        Entity.__init__(self, "Bruxo", 3,
                      [Action("medo", "Alvo leva dano dobrado neste turno", True, self.medo),
                       Action("choque", "Interrompe a ação do alvo", True, self.choque),
                       Action("vampiro", "Causa 1 dano, Bruxo recupera 1HP", True, self.vampiro)]
                      )



def generate_heroes():
    return [Bruxo(), Feiticeiro(), Clerigo(), Samurai()]
