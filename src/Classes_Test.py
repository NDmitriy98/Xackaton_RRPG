from src.Classes import *
import src.Map as Map

my_map = Map.Map()
my_map.generate_map()
my_map.print_map()

#
# main = Character.Character()
# main.set_pos(1, 2)
# print("Pos (" + main.info + "): = " + str(main.x) + ", " + str(main.y))
# main.move(3, 2)
# print("Pos: = " + str(main.x) + ", " + str(main.y))
# print("Level = " + str(main.level) + " exp = " + str(main.experience))
# main.add_experience(25)
# print("Level = " + str(main.level) + " exp = " + str(main.experience))
# print("Attack = " + str(main.get_damage()))
# main.add_experience(250)
# print("Level = " + str(main.level) + " exp = " + str(main.experience))
# print("Attack = " + str(main.get_damage()))
#
# skelet = Skeleton.Skeleton()
# skelet.x = 2
# skelet.y = 7
# print("Pos (" + skelet.info + "): = " + str(skelet.x) + ", " + str(skelet.y))
# print("(skelet) Alive: " + str(skelet.alive) + " hp " + str(skelet.hp) + " protect " + str(skelet.protection))
# skelet.in_damage(main.get_damage())
# print("(skelet) Alive: " + str(skelet.alive) + " hp " + str(skelet.hp))
# skelet.in_damage(main.get_damage())
# print("(skelet) Alive: " + str(skelet.alive) + " hp " + str(skelet.hp))
#
# weapon = Weapon.Weapon()
# weapon.attack = 100
# main.set_weapon(weapon)
# print("Attack new = " + str(main.get_damage()))
#
# superskelet = Skeleton.Skeleton()
# superskelet.hp = 150
# superskelet.protection = 5
# print("(superskelet) Alive: " + str(superskelet.alive) + " hp " + str(superskelet.hp) + " protect " + str(superskelet.protection))
# superskelet.in_damage(main.get_damage())
# print("(superskelet) Alive: " + str(superskelet.alive) + " hp " + str(superskelet.hp))
# superskelet.in_damage(main.get_damage())
# print("(superskelet) Alive: " + str(superskelet.alive) + " hp " + str(superskelet.hp))
# superskelet.in_damage(main.get_damage())
# print("(superskelet) Alive: " + str(superskelet.alive) + " hp " + str(superskelet.hp))
#
# BOSS = Skeleton.Skeleton()
# BOSS.hp = 9999
# BOSS.attack = 9999
# print("(BOSS) Alive: " + str(BOSS.alive) + " hp " + str(BOSS.hp) + " attack " + str(BOSS.attack))
# print("(player) Alive: " + str(main.alive) + " hp " + str(main.hp) + " protect " + str(main.full_protection))
# main.in_damage(BOSS.get_damage())
# print("(player) Alive: " + str(main.alive) + " hp " + str(main.hp) + " protect " + str(main.full_protection))
#
# print("FUCK GG")