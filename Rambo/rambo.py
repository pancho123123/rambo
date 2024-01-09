import pygame, random
from random import randint

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rambo")
clock = pygame.time.Clock()

def draw_text1(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, (255, 255, 255))
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_text2(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, (0, 0, 0))
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, BLACK, border, 2)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("img/player.png").convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 5
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.speed_y = 0
		self.shield = 100

	def update(self):
		self.speed_x = 0
		self.speed_y = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_a]:
			self.speed_x = -5
		if keystate[pygame.K_d]:
			self.speed_x = 5
		if keystate[pygame.K_w]:
			self.speed_y = -2
		if keystate[pygame.K_s]:
			self.speed_y = 2
		self.rect.x += self.speed_x
		self.rect.y += self.speed_y
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
		if self.rect.top < 100:
			self.rect.top = 100

	def shoot(self):
		bullet = Bullet(self.rect.right, self.rect.centery)
		all_sprites.add(bullet)
		bullets.add(bullet)

		#Agregamos sonido
		laser_sound.play()

class Bear(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = bear_images[0]
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH + self.rect.width, WIDTH + 4*self.rect.width)
		self.rect.y = random.randrange(400, 550)
		#self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-3, -1)

	def update(self):
		self.rect.x += self.speedx
		#self.rect.y += self.speedy
		if  self.rect.left < -40:
			self.rect.y = random.randrange(400, 550)
			self.rect.x = random.randrange(WIDTH + self.rect.width, WIDTH + 3*self.rect.width)

			#Change this variable
			self.rect.y = random.randrange(400, 550)
			self.rect.x = random.randrange(WIDTH + self.rect.width, WIDTH + 3*self.rect.width)
			self.speedx = random.randrange(-3, -1)

class Ovni(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = ovni_images[0]
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width,WIDTH + self.rect.width)
		self.rect.y = random.randrange(0, 400)
		self.speedy = random.randrange(-1, 1)
		self.speedx = random.randrange(-5, -1)

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -40:
			self.rect.y = random.randrange(0,400)

			#Change this variable
			self.rect.y = random.randrange(0, 400)
			self.rect.x = random.randrange(WIDTH - self.rect.width,WIDTH + self.rect.width)
			self.speedx = random.randrange(-5, -1)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("img/bullet.png").convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.centery = y
		self.rect.centerx = x
		self.speedx = 10

	def update(self):
		self.rect.x += self.speedx
		if self.rect.left > 850:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # how long to wait for the next frame VELOCITY OF THE EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill() # if we get to the end of the animation we don't keep going.
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

bear_images = []
bear_list = ["img/oso.png"]
for img in bear_list:
	bear_images.append(pygame.transform.scale(pygame.image.load(img).convert(),(100,100)))

ovni_images = []
ovni_list = ["img/ovni.png"]
for img in ovni_list:
	ovni_images.append(pygame.transform.scale(pygame.image.load(img).convert(),(100,100)))

## --------------- CARGAR IMAGENES EXPLOSIÓN -------------------------- ##
explosion_anim = []
for i in range(9):
	file = "img/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70, 70))
	explosion_anim.append(img_scale)


# Cargar fondo.
background = pygame.image.load("img/fond.png").convert()

# Cargar sonidos
laser_sound = pygame.mixer.Sound("sound/laser5.ogg")
explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
#pygame.mixer.music.load("sounds/music.ogg")
pygame.mixer.music.set_volume(0.1)

all_sprites = pygame.sprite.Group()
bear_list = pygame.sprite.Group()
ovni_list = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(4):
	bear = Bear()
	all_sprites.add(bear)
	bear_list.add(bear)
for i in range(3):
	ovni = Ovni()
	all_sprites.add(ovni)
	ovni_list.add(ovni)


#Marcador / Score
score = 0

# Game Loop
running = True
while running:
	# Keep loop running at the right speed
	clock.tick(60)
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_f:
				player.shoot()

	# Update
	all_sprites.update()

	# Colisiones bear - laser
	hits = pygame.sprite.groupcollide(bear_list, bullets, True, True)
	for hit in hits:
		score += randint(5,15)
		explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)

		bear = Bear()
		all_sprites.add(bear)
		bear_list.add(bear)

	# Colisiones ovni - laser
	hits = pygame.sprite.groupcollide(ovni_list, bullets, True, True)
	for hit in hits:
		score += randint(5,15)
		explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)

		ovni = Ovni()
		all_sprites.add(ovni)
		ovni_list.add(ovni)

		
	# Colisiones jugador - bear

	hits = pygame.sprite.spritecollide(player, bear_list, True) # Change here
	for hit in hits:
		player.shield -= 25
		bear = Bear()
		all_sprites.add(bear)
		bear_list.add(bear)
		if player.shield <= 0:
			running = False


	# Colisiones jugador - ovni

	hits = pygame.sprite.spritecollide(player, ovni_list, True) # Change here
	for hit in hits:
		player.shield -= 25
		ovni = Ovni()
		all_sprites.add(ovni)
		ovni_list.add(ovni)
		if player.shield <= 0:
			running = False

	#Draw / Render
	screen.blit(background, [0, 0])
	all_sprites.draw(screen)

	# Marcador
	draw_text2(screen, str(score), 25, WIDTH // 2, 10)

	# ESCUDO.
	draw_shield_bar(screen, 5, 5, player.shield)


	pygame.display.flip()

pygame.quit()