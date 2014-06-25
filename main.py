import pygame
import random
SCRNXB = 800
SCRNYB = 600

colors = map(lambda x: [int(t) * 255 for t in x],
             ['{0:0>3b}'.format(t) for t in range(0, 8)])

shadowcolor = map(lambda x: [int(t) * 180 for t in x],
             ['{0:0>3b}'.format(t) for t in range(0, 8)])

shadowcolor[0] = (20, 20, 20)

class Particle():

    def __init__(self, x=SCRNXB / 2, y=SCRNYB + 300):
        self.x = x
        self.y = y
        self.color = random.choice(colors)
        self.secondcolor = shadowcolor[colors.index(self.color)]
        self.scalarisx = random.uniform(-1, 1)
        self.scalarisy = random.uniform(-1, 1)
        self.randoms = [random.randint(-5, 5) for x in range(0, 7)]
        self.randoms.append(random.randint(10, 30))

    def move(self, x, y):
        self.scalarisx += x
        self.scalarisy += y
        self.x += self.scalarisx
        self.y += self.scalarisy

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 2, 2), 0)

    def polyrender(self, screen):
        pygame.draw.polygon(screen, (20, 20, 20),
        ((self.x - 10 + self.randoms[0] + 3, (self.y + self.randoms[1] - 3)),
        (self.x + self.randoms[2] + 3, (self.y - 5 + self.randoms[5] - 3)),
        (self.x + 10 + self.randoms[3] + 3, (self.y + self.randoms[6] - 3)),
        (self.x + self.randoms[4] + 3, (self.y - 20 - self.randoms[7] - 3))), 0)
       
        pygame.draw.polygon(screen, self.color,
        ((self.x - 10 + self.randoms[0], (self.y + self.randoms[1])),
        (self.x + self.randoms[2], (self.y - 5 + self.randoms[5])),
        (self.x + 10 + self.randoms[3], (self.y + self.randoms[6])),
        (self.x + self.randoms[4], (self.y - 20 - self.randoms[7]))),
        0)

        pygame.draw.polygon(screen, self.secondcolor,
        ((self.x - 10 + self.randoms[0], (self.y + self.randoms[1])),
        (self.x + self.randoms[2], (self.y - 5 + self.randoms[5])),
        (self.x + self.randoms[4], (self.y - 20 - self.randoms[7]))),
        0)    

    def is_out_of_bounds(self):
        if (self.x > SCRNXB or self.x < -100 or
            self.y > SCRNYB + 100 or self.y < -100):
            return 1
        else:
            return 0


def init():
    pygame.init()
    return pygame.display.set_mode((SCRNXB, SCRNYB),
           (pygame.HWSURFACE + pygame.HWACCEL +
           pygame.DOUBLEBUF + pygame.ASYNCBLIT),
           32)


def UI(screen, font, fade):
    pygame.draw.line(screen, fade, (40 + SCRNXB / 2, SCRNYB / 2), 
                    (-40 + SCRNXB / 2, SCRNYB / 2), 1)
    pygame.draw.line(screen, fade, (SCRNXB / 2, 40 + SCRNYB / 2),
                    (SCRNXB / 2, -40 + SCRNYB / 2), 1)
    screen.blit(font.render("Direction", 0, fade),
                           (-45 + SCRNXB / 2, SCRNYB / 2))
    screen.blit(font.render("Speed", 0, fade),
                           (4 + SCRNXB / 2, -45 + SCRNYB / 2))


def main():
    fade = 255
    mouse = (0, 0)
    PLANES = 50
    screen = init()
    font = pygame.font.Font(None, 15)
    clock = pygame.time.Clock()
    particles = [Particle() for i in range(0, PLANES)]
    caption = "FPS: {0:.1f} X, Y: {1}, {2}"
    while True:
        if fade > 1:
            color = (fade, fade, fade)
            fade -= 1
            UI(screen, font, color)
        for particle in particles:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    mouse = (event.pos[0] - SCRNXB / 2,
                             event.pos[1] - SCRNYB / 2)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            particle.move(mouse[0] * 0.001, mouse[1] * 0.001)
            if particle.is_out_of_bounds():
                particle.__init__(random.randint(0, SCRNXB),
                                  SCRNYB + 50)
            particle.render(screen)
            particle.polyrender(screen)
        pygame.display.flip()
        pygame.display.set_caption(caption.format(clock.get_fps(),
                                   mouse[0], mouse[1]))
        screen.fill((30, 30, 30))
        clock.tick(60)

if __name__ == "__main__":
    main()
