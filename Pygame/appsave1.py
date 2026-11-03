import os
import sys
import pygame
import random
import json


INITIAL_METEOR_SPAWN_INTERVAL = 2000
DIFFICULTY_LEVELS = [(25, 3), (50, 6), (100, 9), (200, 12)]
DEFAULT_DIFFICULTY_INDEX = 0
DIFFICULTY = DIFFICULTY_LEVELS[DEFAULT_DIFFICULTY_INDEX][0]
STARTING_LIVES = DIFFICULTY_LEVELS[DEFAULT_DIFFICULTY_INDEX][1]

class FloatingText:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = 30

    def update_and_draw(self, WIN, font):
        text_surface = font.render(self.text, True, self.color)
        WIN.blit(text_surface, (self.x, self.y))
        self.y -= 1
        self.lifetime -= 1
        return self.lifetime > 0

class Star:
    def __init__(self, x, y, velocity, size, color, HP=1):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.size = size
        self.color = color
        self.grazed = False
        self.hp = HP

    def move(self):
        self.y += self.velocity

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, self.get_rect())

    @staticmethod
    def stars_draw(a_list):
        for star in a_list:
            star.draw(WIN)

class Player:
    def __init__(self, lifes, x, y, velocity, width, height):
        self.lifes = lifes
        self.rect = pygame.Rect(x, y, width, height)
        self.recthit = pygame.Rect(x, y, width*3, height*3)
        self.velocity = velocity
        self.I_frame = 5
        self.shield = 0
        self.clear = 0
        self.attack = 1

    def shield_damage(self):
        self.shield -= 1
        sounds["damage"].play()

    def slow_down(self):
        self.velocity -= 1

    def take_damage(self):
        self.lifes -= 1
        sounds["damage"].play()

    def heal(self):
        self.lifes += 1
        sounds["healing"].play()

    def speed_up(self):
        self.velocity += 1
        sounds["pickup"].play()

    def move(self, keys, WIDTH, HEIGHT):
        current_speed = self.velocity
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            current_speed = max(2, self.velocity // 2)
        if keys[pygame.K_LEFT] and self.rect.x - self.velocity >= 0:
            self.rect.x -= current_speed
        if keys[pygame.K_RIGHT] and self.rect.x + self.velocity + self.rect.width <= WIDTH:
            self.rect.x += current_speed
        if keys[pygame.K_UP] and self.rect.y - self.velocity >= 0:
            self.rect.y -= current_speed
        if keys[pygame.K_DOWN] and self.rect.y + self.velocity + self.rect.height <= HEIGHT:
            self.rect.y += current_speed
        self.recthit.center = self.rect.center

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def spawns(objects, spawn_timers, player, category, timer_key, Hitpoints=None):
    config = objects[category]
    if spawn_timers[timer_key] > config["counter"]:
        count = config.get("count", 1)
        spawned_any = False
        for _ in range(count):
            size = config["size"]
            if isinstance(size, list):
                size = random.choice(size)
            velocity = config["velocity"]

            if isinstance(velocity, list):
                velocity = random.choice(velocity)

            if "x_override" in config:
                x = config["x_override"](player) if callable(config["x_override"]) else config["x_override"]
            elif config.get("x_center"):
                x = WIDTH / 2 - size / 2
            else:
                x = random.randint(0, WIDTH - size)

            if "y_override" in config:
                y = config["y_override"](player) if callable(config["y_override"]) else config["y_override"]
            else:
                y = -size

            # Use hp from config, or fallback to Hitpoints argument, then default 1
            hp = config.get("hp", Hitpoints if Hitpoints is not None else 1)

            star = Star(x, y, velocity, size, config["color"], hp)
            config["list"].append(star)
            spawned_any = True
        spawn_timers[timer_key] = 0
        return spawned_any
    return False

# CHANGE 7: Simplify sound loading using a dictionary (unchanged)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/background.MP3")
pygame.mixer.music.set_volume(0.2)

sounds = {
    "pickup": pygame.mixer.Sound("sounds/pickup.wav"),
    "damage": pygame.mixer.Sound("sounds/damage.wav"),
    "healing": pygame.mixer.Sound("sounds/healing.wav"),
    "clear": pygame.mixer.Sound("sounds/clear.wav")
}
sounds["pickup"].set_volume(0.5)
sounds["damage"].set_volume(0.5)
sounds["healing"].set_volume(0.2)

WIDTH, HEIGHT = 1400, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")
BG = pygame.transform.scale(pygame.image.load(resource_path("back.jpg")), (WIDTH, HEIGHT))
FONT = pygame.font.SysFont("Segoe UI Emoji", 30)
STAR_SIZES = [12, 16, 20, 25, 30, 35]
STAR_VELOCITY = [3, 3.3, 3.5, 3.7, 3.9, 4.1]

def load_score():
    try:
        with open("score.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_score(best_score):
    with open("score.json", "w") as file:
        json.dump(best_score, file, indent=4)

# CHANGE 6 (unchanged): handle_player_hit
def handle_player_hit(player, objects, multiplier):
    if player.shield > 0:
        player.shield_damage()
    else:
        player.take_damage()
        objects["floating_texts"]["list"].append(
            FloatingText("-1 ❤️", player.rect.x, player.rect.y - 20, "red")
        )
        multiplier = 1
        if player.velocity > 5:
            player.slow_down()
            objects["floating_texts"]["list"].append(
                FloatingText("-1 ⚡", player.rect.x, player.rect.y - 40, "cyan")
            )
    player.I_frame = 0
    return multiplier

# CHANGE 5 (unchanged): draw function
def draw(objects, player, elapsed_time, playing, best_score, difficulty, multiplier):
    WIN.blit(BG, (0, 0))
    for key, config in objects.items():
        if key != "floating_texts" and "list" in config:
            Star.stars_draw(config["list"])

    time_text = FONT.render(f"SCORE  {round(elapsed_time)}  multiplier  {round(multiplier, 2)}", 1, "white")
    WIN.blit(time_text, (10, 10))
    difficulty_text = FONT.render(f"Difficulty:{difficulty}", 1, "green")
    WIN.blit(difficulty_text, (WIDTH - 10 - difficulty_text.get_width(), 10))
    lifes_text = FONT.render(f"❤️:{player.lifes}", 1, "RED")
    WIN.blit(lifes_text, (WIDTH - 10 - lifes_text.get_width(), 40))
    if player.velocity > 5:
        speed_text = FONT.render(f"⚡:{player.velocity}", 1, "cyan")
        WIN.blit(speed_text, (WIDTH - 10 - speed_text.get_width(), 75))
    if player.shield > 0:
        shield_text = FONT.render(f"🛡️:{player.shield}", 1, "GOLD")
        WIN.blit(shield_text, (WIDTH - 10 - shield_text.get_width(), 110))
    if player.clear > 0:
        clear_text = FONT.render(f" 🌀:{player.clear}", 1, "magenta")
        WIN.blit(clear_text, (WIDTH - 10 - clear_text.get_width(), 145))
    if player.attack > 1:
        attack_text = FONT.render(f" 💪 :{player.attack}", 1, "cyan")
        WIN.blit(attack_text, (WIDTH - 10 - attack_text.get_width(), 180))
    if player.I_frame < 3:
        if (player.I_frame % 0.4) > 0.2:
            pygame.draw.rect(WIN, "gold", player.rect, border_radius=10)
        else:
            pygame.draw.rect(WIN, "red", player.rect, border_radius=10)
    else:
        pygame.draw.rect(WIN, "red", player.rect, border_radius=10)

    for ft in objects["floating_texts"]["list"][:]:
        if not ft.update_and_draw(WIN, FONT):
            objects["floating_texts"]["list"].remove(ft)

    if not playing and player.lifes > 0:
        instructions = FONT.render("to pause/unpause press P", 1, "white")
        WIN.blit(instructions, (WIDTH / 2 - instructions.get_width() / 2, HEIGHT / 2 - instructions.get_height()))
    if not playing and player.lifes <= 0:
        background = pygame.Rect(WIDTH / 2 - 150, HEIGHT / 2 - 150, 300, 300)
        pygame.draw.rect(WIN, "blue", background, border_radius=10)
        instructions = FONT.render("to restart press R", 1, "white")
        WIN.blit(instructions, (WIDTH / 2 - instructions.get_width() / 2, HEIGHT / 2 - instructions.get_height() - 30))
        lost_text = FONT.render("You lost 💀💀💀", 1, "white")
        WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height()))
        score_text = FONT.render(f"best score : {best_score} 🏆", 1, "yellow")
        WIN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2 - score_text.get_height() + 30))
    pygame.display.update()

def main():
    pygame.mixer.music.play(-1)
    best_score = load_score() or 0

    difficulty_index = DEFAULT_DIFFICULTY_INDEX
    difficulty = DIFFICULTY_LEVELS[difficulty_index][0]
    starting_lives = DIFFICULTY_LEVELS[difficulty_index][1]

    player = Player(starting_lives, WIDTH / 2, HEIGHT - 30, 5, 30, 30)

    meteor_star_add_increment = INITIAL_METEOR_SPAWN_INTERVAL

    bullet_size = 7
    trail_size = 5

    # CHANGE 8: Added "hp" and "timer_key" to configs, and grouped spawn conditions
    objects = {
        "tanks": {"list": [], "counter": 5000, "size": 50, "velocity": 3, "color": (150,0,255), "x_center": False, "count": 1, "hp": 10, "timer_key": "tank", "spawn_condition": lambda keys, objects: not objects["bosses"]["list"]},
        "stars": {"list": [], "counter": meteor_star_add_increment, "size": 20, "velocity": STAR_VELOCITY, "color": "white", "x_center": False, "count": 4, "hp": 1, "timer_key": "meteor", "spawn_condition": lambda keys, objects: not objects["bosses"]["list"]},
        "healing": {"list": [], "counter": 5000, "size": 15, "velocity": STAR_VELOCITY, "color": "red", "x_center": False, "count": 1, "hp": 1, "timer_key": "healing", "spawn_condition": lambda keys, objects: not objects["bosses"]["list"]},
        "speed": {"list": [], "counter": 7500, "size": 20, "velocity": STAR_VELOCITY, "color": "cyan", "x_center": False, "count": 1, "hp": 1, "timer_key": "speed", "spawn_condition": lambda keys, objects: not objects["bosses"]["list"]},
        "shield": {"list": [], "counter": 6500, "size": 14, "velocity": STAR_VELOCITY, "color": "gold", "x_center": False, "count": 1, "hp": 1, "timer_key": "shield", "spawn_condition": lambda keys, objects: not objects["bosses"]["list"]},
        "clear": {"list": [], "counter": 5000, "size": 25, "velocity": STAR_VELOCITY, "color": "magenta", "x_center": False, "count": 1, "hp": 1, "timer_key": "clear_star", "spawn_condition": lambda keys, objects: not objects["bosses"]["list"]},
        "trail": {"list": [], "counter": 50, "size": trail_size, "velocity": 0, "color": (200,200,255), "x_center": False, "count": 1, "hp": 1, "timer_key": "trail_star", "spawn_condition": lambda keys, objects: True, "x_override": lambda p, s=trail_size: p.rect.centerx-trail_size/2, "y_override": lambda p, s=trail_size: p.rect.centery-trail_size/2},
        "bosses": {"list": [], "counter": 20000, "size": 200, "velocity": 4, "color": (150,0,255), "x_center": True, "count": 1, "hp": 20, "timer_key": "boss", "spawn_condition": lambda keys, objects: True},
        "background": {"list": [], "counter": 500, "size": 5, "velocity": 1.5, "color": "gray", "x_center": False, "count": 8, "hp": 1, "timer_key": "background", "spawn_condition": lambda keys, objects: True},
        "bullets": {"list": [], "counter": 50, "size": bullet_size, "velocity": -7, "color": "red", "x_center": False, "count": 1, "hp": 1, "timer_key": "bullet", "spawn_condition": lambda keys, objects: keys[pygame.K_SPACE], "x_override": lambda p, s=bullet_size: p.rect.centerx-bullet_size/2, "y_override": lambda p, s=bullet_size: p.rect.centery-bullet_size/2},
        "floating_texts": {"list": []},
        "bullet_upgrades": {"list": [], "counter": 5000, "size": 25, "velocity": STAR_VELOCITY, "color": (255, 165, 0), "x_center": False, "count": 1, "hp": 1, "timer_key": "bullet_upgrade", "spawn_condition": lambda keys, objects: not objects["bosses"]["list"]}
    }

    spawn_timers = {
        "base": 0, "meteor": 0, "healing": 0, "speed": 0,
        "background": 0, "shield": 0, "clear_star": 0, "trail_star": 0,
        "bullet": 0, "boss": 0, "bullet_upgrade": 0, "tank": 0
    }

    run = True
    playing = True
    elapsed_time = 0
    clock = pygame.time.Clock()
    score_count = 0
    multiplier = 1
    player.I_frame = 5

    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and player.clear > 0:
                    player.clear -= 1
                    objects["stars"]["list"].clear()
                    sounds["clear"].play()
                if event.key == pygame.K_p and player.lifes > 0:
                    playing = not playing
                if event.key == pygame.K_r:
                    for key in objects:
                        objects[key]["list"].clear()
                    for spawn_timer in spawn_timers:
                        spawn_timers[spawn_timer] = 0
                    playing = True
                    elapsed_time = 0
                    meteor_star_add_increment = INITIAL_METEOR_SPAWN_INTERVAL
                    player.rect.x = WIDTH / 2
                    player.rect.y = HEIGHT - 30
                    player.clear = 0
                    player.shield = 0
                    player.attack = 1
                    player.velocity = 5
                    player.lifes = starting_lives
                    multiplier = 1
                    player.I_frame = 5
                if not playing and event.key == pygame.K_d:
                    difficulty_index = (difficulty_index + 1) % len(DIFFICULTY_LEVELS)
                    difficulty = DIFFICULTY_LEVELS[difficulty_index][0]
                    starting_lives = DIFFICULTY_LEVELS[difficulty_index][1]  # CHANGE: keep in sync
                    player.lifes = starting_lives

        t = clock.tick(60)
        if playing:
            player.I_frame += t / 1000
            score_count += t / 1000
            if score_count >= 5:
                multiplier += 0.5 + (multiplier * 0.1)
                multiplier = min(multiplier, 25)
                score_count -= 5
            elapsed_time += (t * multiplier) / 1000
            for count in spawn_timers:
                spawn_timers[count] += t
            if player.lifes <= 0:
                if elapsed_time > best_score:
                    best_score = round(elapsed_time)
                    save_score(best_score)
                    objects["floating_texts"]["list"].append(FloatingText("🏆 New Record!", WIDTH//2, HEIGHT//2, "gold"))
                playing = False

            # Update star counter (difficulty scaling)
            objects["stars"]["counter"] = meteor_star_add_increment

            # CHANGE 8: Generic spawning system
            # First, always-spawn types (boss, background, trail)
            for category in ["bosses", "background", "trail"]:
                config = objects[category]
                if spawn_timers[config["timer_key"]] > config["counter"]:
                    spawns(objects, spawn_timers, player, category, config["timer_key"])

            # Then, spawn types that require no boss (if no boss is present)
            if not objects["bosses"]["list"]:
                for category in ["clear", "shield", "healing", "speed", "bullet_upgrades", "stars", "tanks"]:
                    config = objects[category]
                    if spawn_timers[config["timer_key"]] > config["counter"]:
                        # For stars, we need to know if a spawn occurred to adjust difficulty
                        if category == "stars":
                            if spawns(objects, spawn_timers, player, category, config["timer_key"]):
                                meteor_star_add_increment = max(200, meteor_star_add_increment - difficulty)
                                objects["stars"]["counter"] = meteor_star_add_increment
                        else:
                            spawns(objects, spawn_timers, player, category, config["timer_key"])

            # Bullets spawn only when space is held
            if keys[pygame.K_SPACE]:
                config = objects["bullets"]
                if spawn_timers[config["timer_key"]] > config["counter"]:
                    spawns(objects, spawn_timers, player, "bullets", config["timer_key"])

            # Bullet upgrade collision
            for star in objects["bullet_upgrades"]["list"][:]:
                star.move()
                if star.y > HEIGHT:
                    objects["bullet_upgrades"]["list"].remove(star)
                elif star.get_rect().colliderect(player.recthit):
                    objects["bullet_upgrades"]["list"].remove(star)
                    player.attack += 1
                    objects["floating_texts"]["list"].append(FloatingText("+ 1 💪", player.rect.x, player.rect.y - 20, "lime"))
                    sounds["pickup"].play()

            # Boss collision with player
            for boss in objects["bosses"]["list"][:]:
                boss.move()
                if boss.y > HEIGHT:
                    objects["bosses"]["list"].remove(boss)
                elif boss.get_rect().colliderect(player.rect):
                    multiplier = handle_player_hit(player, objects, multiplier)
                    break

            # Bullet collisions
            for bullet in objects["bullets"]["list"][:]:
                bullet.move()
                if bullet.y < 0:
                    objects["bullets"]["list"].remove(bullet)
                    continue
                hit = False
                for meteor in objects["stars"]["list"][:]:
                    if meteor.get_rect().colliderect(bullet.get_rect()):
                        meteor.hp -= player.attack
                        if meteor.hp <= 0:
                            objects["stars"]["list"].remove(meteor)
                        objects["bullets"]["list"].remove(bullet)
                        hit = True
                        break
                if hit:
                    continue
                for boss in objects["bosses"]["list"][:]:
                    if boss.get_rect().colliderect(bullet.get_rect()):
                        boss.hp -= player.attack
                        if boss.hp <= 0:
                            objects["bosses"]["list"].remove(boss)
                        objects["bullets"]["list"].remove(bullet)
                        hit = True
                        break
                for tank in objects["tanks"]["list"][:]:
                    if tank.get_rect().colliderect(bullet.get_rect()):
                        tank.hp -= player.attack
                        if tank.hp <= 0:
                            objects["tanks"]["list"].remove(tank)
                        objects["bullets"]["list"].remove(bullet)
                        hit = True
                        break

            # Trail removal
            for star in objects["trail"]["list"][:]:
                star.move()
                if spawn_timers["base"] > 900:
                    objects["trail"]["list"].remove(star)
                    spawn_timers["base"] = 850

            # Clear pickup
            for star in objects["clear"]["list"][:]:
                star.move()
                if star.y > HEIGHT:
                    objects["clear"]["list"].remove(star)
                elif star.get_rect().colliderect(player.recthit):
                    objects["clear"]["list"].remove(star)
                    player.clear += 1
                    sounds["pickup"].play()
                    objects["floating_texts"]["list"].append(FloatingText("+1 🌀", player.rect.x, player.rect.y - 20, "magenta"))

            # Shield pickup
            for star in objects["shield"]["list"][:]:
                star.move()
                if star.y > HEIGHT:
                    objects["shield"]["list"].remove(star)
                elif star.get_rect().colliderect(player.rect):
                    objects["shield"]["list"].remove(star)
                    player.shield += 1
                    sounds["pickup"].play()
                    objects["floating_texts"]["list"].append(FloatingText("+1 🛡️", player.rect.x, player.rect.y - 20, "gold"))

            # Background stars
            for star in objects["background"]["list"][:]:
                star.move()
                if star.y > HEIGHT:
                    objects["background"]["list"].remove(star)

            # Meteor collisions (stars list)
            for star in objects["stars"]["list"][:]:
                star.move()
                if not star.grazed and star.get_rect().colliderect(player.recthit) and not star.get_rect().colliderect(player.rect):
                    elapsed_time += 3 * multiplier
                    star.grazed = True
                    objects["floating_texts"]["list"].append(FloatingText(f"🎯+{round(3*multiplier)}", player.rect.x, player.rect.y - 20, "green"))
                if star.y > HEIGHT:
                    objects["stars"]["list"].remove(star)
                elif star.get_rect().colliderect(player.rect):
                    objects["stars"]["list"].remove(star)
                    if player.I_frame >= 3:
                        multiplier = handle_player_hit(player, objects, multiplier)
                        break

            # Healing pickup
            for star in objects["healing"]["list"][:]:
                star.move()
                if star.y > HEIGHT:
                    objects["healing"]["list"].remove(star)
                elif star.get_rect().colliderect(player.recthit):
                    objects["healing"]["list"].remove(star)
                    if player.lifes < 10:
                        player.heal()
                        objects["floating_texts"]["list"].append(FloatingText("+1 ❤️", player.rect.x, player.rect.y - 20, "red"))
                    break

            # Speed pickup
            for star in objects["speed"]["list"][:]:
                star.move()
                if star.y > HEIGHT:
                    objects["speed"]["list"].remove(star)
                elif star.get_rect().colliderect(player.recthit):
                    objects["speed"]["list"].remove(star)
                    if player.velocity < 10:
                        player.speed_up()
                        objects["floating_texts"]["list"].append(FloatingText("+1 ⚡", player.rect.x, player.rect.y - 20, "cyan"))
                    break

            # Tank collisions
            for star in objects["tanks"]["list"][:]:
                star.move()
                if not star.grazed and star.get_rect().colliderect(player.recthit) and not star.get_rect().colliderect(player.rect):
                    elapsed_time += 3 * multiplier
                    star.grazed = True
                    objects["floating_texts"]["list"].append(FloatingText(f"🎯+{round(3*multiplier)}", player.rect.x, player.rect.y - 20, "green"))
                if star.y > HEIGHT:
                    objects["tanks"]["list"].remove(star)
                elif star.get_rect().colliderect(player.rect):
                    objects["tanks"]["list"].remove(star)
                    if player.I_frame >= 3:
                        multiplier = handle_player_hit(player, objects, multiplier)
                        break

            player.move(keys, WIDTH, HEIGHT)

        draw(objects, player, elapsed_time, playing, best_score, difficulty, multiplier)

    pygame.quit()

if __name__ == "__main__":
    main()