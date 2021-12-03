from copy import copy, deepcopy

def do_nothing(all_entities):
      pass

class Action:
   def __init__(self, name, description, requires_target, function):
        self.name = name
        self.description = description
        self.requires_target = requires_target
        self.function = function


class Order:
   def __init__(self, action, target):
      self.action = action
      self.target = target


class Entity:
   def __init__(self, name, max_health, actions):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.damage_multiplier = 1
        self.actions = actions
        self.active_actions = copy(actions)
        self.stored_order = None


   def take_action(self, all_entities):
      if self.stored_order.action.requires_target:
         self.stored_order.action.function(self.stored_order.target)
      else:
         self.stored_order.action.function(all_entities)

      if self.stored_order.action.function != do_nothing:
            self.active_actions.remove(self.stored_order.action)
      if len(self.active_actions) <= 0:
         self.active_actions = copy(self.actions)

      self.stored_order = None


   def take_damage(self, damage):
      if damage > 0:
         damage *= self.damage_multiplier

      self.health -= damage
      if (self.health < 0):
         self.health = 0
      elif (self.health > self.max_health):
         self.health = self.max_health


   def set_damage_multiplier(self, multiplier):
      self.damage_multiplier = multiplier


   def interrupt_order(self):
      self.stored_order.action = Action("Nada", "Nada", False, do_nothing)


   def change_target(self, target):
      self.stored_order.target = target
