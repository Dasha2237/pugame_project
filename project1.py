import pygame
import os
import sys
import random
FPS = 50
 
pygame.init()
WIDTH = 650
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.key.set_repeat(200, 70)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()
 
 
def start_screen():
    intro_text = [" ПРОЙДИ ЛАБИРИНТ "," "," ",
                  "Закрасьте белый коридор",
                  "с помощью цветного шарика,",
                  "чтобы выиграть.",]
 
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 80
    for line in intro_text:
        string_rendered = font.render(line, 1,(0,0,240))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 140
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
def win():
    intro_text = ["YOU",
                  "WIN!!!"]
 
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 150
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

def load_level(filename):
    #filename = "C:\Users\Student\AppData\Local\Programs\Python\Python37\Mikhaylova\map_1"
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
 
    # и подсчитываем максимальную длину    
    max_width = max(map(len, level_map))
 
    # дополняем каждую строку пустыми клетками ('.')    
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

tile_images = {
    'wall': load_image("wall.jpg"),
    'empty': load_image('empty.jpg')
}
player_image = load_image('shar.png')
 
tile_width = tile_height = 50

colors = [(249,132,229), (102,0,255), (11,218,81), (255,215,0)]
levels = ["1","2","3","4"]
q_in = 0
dragon = pygame.sprite.Group()
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(dragon)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
 
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
 
    def update(self):
        global q_in
        if q_in == 60:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            q_in = 0
        q_in += 1


dragon1 = AnimatedSprite(load_image("New Piskel.png"), 4, 2, 180, 120)

def menu():
 
    #fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.fill((171, 205, 239))
    surf = pygame.Surface((650, 50))
    surf.fill((171, 205, 239))
    screen.blit(surf, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Меню", 1, (0, 0, 0))
    text_x = 325 - text.get_width() // 2
    text_y = 13
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 0, 0), (220, 0,
                                           215,60), 3)
    text = font.render("Цвет", 1, (0, 0, 0))
    text_x = 107 - text.get_width() // 2
    text_y = 13
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0,
                                           220, 60), 3)
    text = font.render("Уровень", 1, (0, 0, 0))
    text_x = 405 + text.get_width() // 2
    text_y = 13
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 0, 0), (435, 0,
                                           215, 60), 3)
    for i in range(4):
        pygame.draw.rect(screen, (0, 0, 0), (0, 60 + 110 * i,
                                           220, 110), 3)
        pygame.draw.rect(screen, (0, 0, 0), (435, 60 + 110 * i,
                                           215, 110), 3)
        pygame.draw.circle(screen, colors[i],
                           (110,115 + 110 *i), 50)
        text = font.render(levels[i], 1, (0, 0, 0))
        
        screen.blit(text, (540, 95 + 110* i))
    global dragon
    dragon.update()
    dragon.draw(screen)
        
    
        


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
 
radius = 20
#color_boll = 'yellow'
color_boll = (249,132,229)
kol_zakr = 0
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.radius = radius
        self.image = pygame.Surface((50, 50),
                                    pygame.SRCALPHA, 32)
        #pygame.draw.rect(self.image, pygame.Color(color_boll),
                           #(pos_x-10,pos_y-10,51, 51))
        pygame.draw.circle(self.image, color_boll,
                           (radius +  6, radius + 6), radius)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x , tile_height * pos_y )
    def peredvighenie(self,number,x,y):
        global n
        global zakr
        if number == 1 :
            print(y-1,x-2)
            print(n[y-1][x-2])
            if n[y-1][x-2] != '#':
                player.rect.x = player.rect.x - 50
                x = x-1
                print(zakr)
                zakr[y-1][x-1] = 1
                tiles[y-1][x-1].image = load_image('way.jpeg')
                w = 0
            else:
                w = 1
            return x, w
        elif number == 2:
            print(y-1,x)
            print(n[y-1][x])
            if n[y-1][x] != '#':
                player.rect.x = player.rect.x + 50
                x = x+1
                zakr[y-1][x-1] = 1
                tiles[y-1][x-1].image = load_image('way.jpeg')
                w = 0
            else:
                w = 1
            return x, w
        elif number == 3:
            print(y-2,x-1)
            print(n[y-2][x-1])
            if n[y-2][x-1] != '#':
                player.rect.y = player.rect.y - 50
                y = y-1
                zakr[y-1][x-1] = 1
                tiles[y-1][x-1].image = load_image('way.jpeg')
                w = 0
            else:
                w = 1
            return y ,w
        elif number == 4:
            print(y,x-1)
            print(n[y][x-1])
            if n[y][x-1] != '#':
                player.rect.y = player.rect.y + 50
                y = y+1
                zakr[y-1][x-1] = 1
                tiles[y-1][x-1].image = load_image('way.jpeg')
                w = 0
            else:
                w = 1
            return y, w
def ball_color(y):
    w = (y - 60)//110
    return w

player = None
 
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
kol_pust = 0
tiles = []
zakr = []
def generate_level(level):
    new_player, x, y = None, None, None
    global kol_pust,zakr,tiles
    for y in range(len(level)):
        tiles.append([])
        zakr.append([])
        for x in range(len(level[y])):
            if level[y][x] == '.':
                tiles[y].append(Tile('empty', x, y))
                zakr[y].append(0)
                kol_pust += 1
            elif level[y][x] == '#':
                tiles[y].append(Tile('wall', x, y))
                zakr[y].append(0)
            elif level[y][x] == '@':
                tiles[y].append(Tile('empty', x, y))
                zakr[y].append(0)
                new_player = Player(x, y)
                X = x + 1
                Y = y + 1
                print(X,Y)
                
    # вернем игрока, а также размер поля в клетках            
    return new_player, X, Y
stars = pygame.sprite.Group()
GRAVITY = 10
screen_rect = (0, 0,650,500)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))
 
    def __init__(self, pos, dx, dy):
        super().__init__(stars)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
 
        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos
 
        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY
 
    def update(self):
        # применяем гравитационный эффект: 
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()

            
def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))



a = 0
d = 1
clock = pygame.time.Clock();
levels_doc = ['map1.txt', 'map2.txt', 'map3.txt', 'map4.txt']
pygame.mixer.init(22050,-16,2,4096)
pygame.mixer.music.load("data\Kalimba.ogg")
pygame.mixer.music.play(0,0.0)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN or \
             event.type == pygame.MOUSEBUTTONDOWN:
            if a == 0  or a == 3:
                a = 4
            elif a == 4:
                x1,y1 = event.pos
                if x1 <= 215 :
                    color_boll = colors[ball_color(y1)]
                if x1 >= 435:
                    print(ball_color(y1))
                    level = levels_doc[ball_color(y1)]
                    a = 1
                    tiles = []
                    zakr = []
                    kol_zakr = 0
                    kol_pust = 0
                    m = load_level(level)
                    n = load_level(level)
                    num = 0
                    player, x, y = generate_level(m)
                    print(x,y)
                    d = 1
                    w = 1
                    
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                if w == 1:
                    num = 1
            if key[pygame.K_RIGHT]:
                if w == 1:
                    num = 2
            if key[pygame.K_UP]:
                if w == 1:
                   num = 3
            if key[pygame.K_DOWN]:
                if w == 1:
                   num = 4
    if a == 0:
        start_screen()
    if a == 1:
            tiles[y-1][x-1].image = load_image('way.jpeg')
            kol_zakr = 0
            for i in range(len(zakr)):
                for j in zakr[i]:
                    kol_zakr += int(j)
            if kol_pust != kol_zakr:
                if num == 1 :
                        x, w = player.peredvighenie(1,x,y)
                if num == 2 :
                        x, w = player.peredvighenie(2,x,y)
                if num == 3 :
                        y, w = player.peredvighenie(3,x,y)
                if num == 4 :
                        y, w = player.peredvighenie(4,x,y)
            else:
                a = 3
                h = 1
                tiles[y-1][x-1].image = load_image('empty.jpg')
                player.rect.x = 700
                player.rect.y = 700
                tiles_group.draw(screen)
            player_group.draw(screen)
            tiles_group.draw(screen)
            player_group.draw(screen)
    if a == 3:
        win()
        if h == 1:
            create_particles((150,20))
            h = 0
        else:
            create_particles((450,20))
            h = 1
        stars.update()
        stars.draw(screen)
    if a == 4:
        q_in = 60
        menu()
    pygame.display.flip()
    clock.tick(50)
