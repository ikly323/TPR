import threading
import random
import time


class Warrior:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.lock = threading.Lock()

    def attack(self, enemy):
        damage = 20
        with self.lock:
            if enemy.health > 0:
                enemy.health -= damage
                if enemy.health < 0:
                    enemy.health = 0
                print(f"{self.name} атакует {enemy.name}. {enemy.name} осталось здоровья: {enemy.health}")
                time.sleep(random.uniform(0.1, 0.5))
                if enemy.health == 0:
                    print(f"{self.name} одержал победу!")


def battle(warrior1, warrior2):
    while warrior1.health > 0 and warrior2.health > 0:
        attacker = random.choice([warrior1, warrior2])
        enemy = warrior2 if attacker == warrior1 else warrior1
        attacker.attack(enemy)


if __name__ == "__main__":
    warrior1 = Warrior("Воин 1")
    warrior2 = Warrior("Воин 2")

    battle_thread = threading.Thread(target=battle, args=(warrior1, warrior2))
    battle_thread.start()
    battle_thread.join()
