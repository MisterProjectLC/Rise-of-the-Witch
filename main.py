# -- coding: utf-8 --
#! python3

import heroes
import enemies
import importlib
import random
from entity import Order

def contra_text(entity):
    if entity.stored_order.action.requires_target:
        return " contra " + entity.stored_order.target.name
    else:
        return ""

# Setup game
class Game:
    def __init__(self):
        self.hero_list = heroes.generate_heroes()
        self.enemy_list = [enemies.Haeldra()]
        self.available_enemy_list = [enemies.Ogro(), enemies.Shaman(), enemies.Vibora(), enemies.Vampiro(), enemies.Minibruxo(), enemies.Minibruxo(), enemies.Corvo(),
                                enemies.Corvo(), enemies.Corrupto(), enemies.Corrupto(), enemies.Orc()]
        self.gone_enemy_list = []
        self.all_entities = [self.hero_list, self.enemy_list]


    def add_new_enemy(self):
        if len(self.available_enemy_list) == 0:
            self.available_enemy_list = self.gone_enemy_list
            self.gone_enemy_list = []
        
        new_enemy = self.available_enemy_list[random.randint(0, len(self.enemy_list)-1)]
        self.gone_enemy_list.append(new_enemy)
        self.available_enemy_list.remove(new_enemy)
        
        new_enemy.health = new_enemy.max_health
        same_enemy_count = 0
        if any(x.name == new_enemy.name for x in self.enemy_list):
            same_enemy_count += 1
        
        while any(x.name == new_enemy.name + str(same_enemy_count+1) for x in self.enemy_list):
            same_enemy_count += 1

        if same_enemy_count > 1:
            new_enemy.name = new_enemy.name + str(same_enemy_count+1)
        self.enemy_list.append(new_enemy)


game = Game()
game.add_new_enemy()
game.add_new_enemy()

# Turn
turn_timer = 1
victory = False
while True:
    alive_hero_list = []
    for hero in game.hero_list:
        if hero.health > 0:
            alive_hero_list.append(hero)
    
    # Decide enemy actions
    for enemy in game.enemy_list:
        enemy.stored_order = Order(enemy.active_actions[0],
                              alive_hero_list[random.randint(0, len(alive_hero_list)-1)])
    
    # Print status
    print("----- TURNO " + str(turn_timer) + " -----")
    print("--- HERÓIS ---")
    for hero in game.hero_list:
        print(hero.name.upper())
        print("HP: " + str(hero.health) + "/" + str(hero.max_health))
        print("Ações disponíveis - ações gastas só retornam após todas serem gastas")
        for action in hero.active_actions:
            print(action.name.upper() + ": " + action.description)
        print("")

    print("--- INIMIGOS ---")
    for enemy in game.enemy_list:
        print(enemy.name.upper())
        print("HP: " + str(enemy.health) + "/" + str(enemy.max_health))
        next_action = enemy.stored_order.action
        print("Próxima ação: " + next_action.name.upper() + ": " + next_action.description + contra_text(enemy))
        print("")

    # Decide hero actions
    print("Exemplo de Input: 'Clerigo Clava Esqueleto'")
    print("Digite 'feito' para finalizar turno")
    while True:
        player_input = input()

        # Finalize turn
        if player_input.lower() == 'feito':
            interminado = False
            for hero in game.hero_list:
                if hero.health > 0 and hero.stored_order == None:
                    print("Selecione a ação de " + hero.name + " antes de continuar.")
                    interminado = True
                    break

            if interminado:
                continue
            break

        # Get args
        args = player_input.split(" ")
        if len(args) < 2:
            print("Argumentos insuficientes!")
            continue

        # Get action
        chosen_hero = None
        chosen_action = None
        for hero in game.hero_list:
            if hero.name.lower() == args[0].lower():
                chosen_hero = hero
                for action in hero.active_actions:
                    if action.name.lower() == args[1].lower():
                        chosen_action = action
                        break
                break

        if chosen_action == None:
            print("Ação inválida!")
            continue

        # Get target
        chosen_target = None
        if chosen_action.requires_target:
            if len(args) < 3:
                print("Alvo não foi dado!")
                continue
            
            for entity in game.hero_list:
                if entity.name.lower() == args[2].lower():
                    chosen_target = entity
                    break

            if chosen_target == None:
                for entity in game.enemy_list:
                    if entity.name.lower() == args[2].lower():
                        chosen_target = entity
                        break

            if chosen_target == None:
                print("Alvo inválido!")
                continue

        # Store action
        chosen_hero.stored_order = Order(chosen_action, chosen_target)
        next_action = chosen_hero.stored_order.action
        print("Ação escolhida: " + chosen_hero.name.upper() + ": " + next_action.name.capitalize() + contra_text(chosen_hero))
    
    
    # Resolve turn
    rip_the_witch_lmao = False
    rip_the_team_crying_emoji = True
    
    for entity in game.hero_list:
        if entity.health > 0:
            print(entity.name + " tomando a ação " + entity.stored_order.action.name.capitalize() + contra_text(entity))
            entity.take_action(game.all_entities)

    for entity in game.enemy_list:
        if entity.health > 0:
            print(entity.name + " tomando a ação " + entity.stored_order.action.name.capitalize() + contra_text(entity))
            entity.take_action(game.all_entities)


    # Check deaths
    for hero in game.hero_list:
        if hero.health <= 0:
            print(hero.name + " morreu...")

    i = 0
    while True:
        if i >= len(game.enemy_list):
            break
        
        entity = game.enemy_list[i]
        if entity.health <= 0:
            print(entity.name + " morreu!")
            if entity.name == "Haeldra":
                rip_the_witch_lmao = True
            game.enemy_list.pop(i)
            i -= 1
        i += 1

    # Check victory conditions
    if rip_the_witch_lmao:
        victory = True
        break

    rip_the_team_crying_emoji = True
    for entity in game.hero_list:
        if entity.health > 0:
            rip_the_team_crying_emoji = False
            break

    if rip_the_team_crying_emoji:
        break

    # Advance turn
    game.add_new_enemy()
    if len(game.enemy_list) < 3:
        game.add_new_enemy()
    
    for hero in game.hero_list:
        hero.set_damage_multiplier(1)
    
    for enemy in game.enemy_list:
        enemy.set_damage_multiplier(1)
        
    
    turn_timer += 1
    input()


# Ending
if victory:
    print("VITÓRIA!")
else:
    print("Derrota...")


