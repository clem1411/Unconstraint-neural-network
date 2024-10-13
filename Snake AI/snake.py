import pygame
import random
from GeneticAI import Controller
from GeneticAI import AIController

# Initialize the game
pygame.init()

# Set up the display
screen = pygame.display.set_mode((850, 750))

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (0, 255, 0)
GREEN = (0, 200, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Set up the game loop
running = True

class Snake:
    direction = "right"
    body = [(4, 8), (3, 8), (2, 8)]
    head = (4, 8)

    def move(self):
        if self.direction == "right":
            self.head = (self.head[0] + 1, self.head[1])
        elif self.direction == "left":
            self.head = (self.head[0] - 1, self.head[1])
        elif self.direction == "up":
            self.head = (self.head[0], self.head[1] - 1)
        elif self.direction == "down":
            self.head = (self.head[0], self.head[1] + 1)
        
        self.body.insert(0, self.head)
        self.body.pop()
    
    def grow(self):
        self.body.append(self.body[-1])
    
    def check_collision(self):
        if self.head in self.body[1:]:
            return True
        return False
    
    def check_fruit(self, fruit):
        if self.head == fruit:
            return True
        return False

    def check_wall(self):
        if self.head[0] < 0 or self.head[0] > 16 or self.head[1] < 0 or self.head[1] > 14:
            return True
        return False
    
    def check_object_collision(self,object):
        if object in self.body:
            return True
        return False
    
    def get_status(self,fruit):
        status = [0] * 16  # Initialiser status avec un élément, ici 0
    
    # Check if the snake is going to hit itself
        status[0]= self.head +(0,1) in self.body
        status[1]= self.head +(1,0) in self.body
        status[2]= self.head +(0,-1) in self.body
        status[3]= self.head +(-1,0) in self.body
    # Check if the snake is going to hit a wall
        status[4]= self.head[0] == 0
        status[5]= self.head[1] == 0
        status[6]= self.head[0] == 16
        status[7]= self.head[1] == 14
    # Check if the fruit is on one direction
        status[8]= self.head[0] < fruit[0]
        status[9]= self.head[0] > fruit[0]
        status[10]= self.head[1] < fruit[1]
        status[11]= self.head[1] > fruit[1]

    # check if the fruit is close to the snake
        status[12]= (self.head +(0,1) == fruit)
        status[13]= (self.head +(1,0) == fruit)
        status[14]= (self.head +(0,-1) == fruit)
        status[15]= (self.head +(-1,0) == fruit)
        return status
    
    def reset(self):
        self.direction = "right"
        self.body = [(4, 8), (3, 8), (2, 8)]
        self.head = (4, 8)




class HumanController(Controller):
    def get_direction(self):
        """Contrôleur humain utilisant les événements clavier."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            return 'left'
        if keys[pygame.K_RIGHT]:
            return 'right'
        if keys[pygame.K_UP]:
            return 'up'
        if keys[pygame.K_DOWN]:
            return 'down'
        return None
    

    
mySnake = Snake()
fruit = (random.randint(0, 16), random.randint(0, 14))

screen.fill(GREEN)

population = 100
controller = AIController(population)
score = 0
numGenome = 0
limit = 300
nbStep = 0
nbGeneration = 0
print("New Generation" + str(nbGeneration))
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the direction from the controller
    direction = controller.get_direction(mySnake.get_status(fruit),numGenome)
    if direction:
        if (direction == "up" and mySnake.direction != "down") or (direction == "down" and mySnake.direction != "up") or (direction == "left" and mySnake.direction != "right") or (direction == "right" and mySnake.direction != "left"):
            mySnake.direction = direction

    # Update the game state
    mySnake.move()
    if mySnake.check_wall() or mySnake.check_collision() or nbStep > limit:
        controller.setFitness(numGenome,score)
        nbStep = 0
        font = pygame.font.Font(None, 74)  # 74 est la taille de la police
        message = f"Game Over. Score: {score}"
        overlay = pygame.Surface((850, 750))  # Créer une surface de la taille de l'écran
        overlay.set_alpha(150)  # Définir la transparence (0 = transparent, 255 = opaque)
        overlay.fill(GRAY)  # Colorier la surface avec du gris

        # Afficher le rectangle grisé
        screen.blit(overlay, (0, 0))
        numGenome += 1
        numGenome = numGenome % population
        if numGenome == 0:
            nbGeneration += 1
            print("New Generation" + str(nbGeneration))
            controller.newGeneration(nbGeneration)

        # Rendre le message texte
        text = font.render(message, True, WHITE)

        # Obtenir la position du texte (centré)
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        # Afficher le texte sur l'écran
        screen.blit(text, text_rect)
        score = 0
        mySnake.reset()

        pygame.display.flip()
        wait = pygame.time.wait(0)
    
    if mySnake.check_fruit(fruit):
        mySnake.grow()
        score += 1
        nbStep = 0
        while mySnake.check_object_collision(fruit):
            fruit = (random.randint(0, 16), random.randint(0, 14))

    # Draw everything

    # Draw the grid
    x=0
    y=0
    for x in range(0, 850, 50):
        for y in range(0, 750, 50):
            if x%100 != y%100:
                pygame.draw.rect(screen, GREEN, (x, y, 50, 50))
            else:
                pygame.draw.rect(screen, LIGHT_GREEN, (x, y, 50, 50))

    # Draw the snake
    for segment in mySnake.body:
        pygame.draw.rect(screen, WHITE, (segment[0]*50, segment[1]*50, 50, 50))

    pygame.draw.rect(screen, RED, (fruit[0]*50, fruit[1]*50, 50, 50))

    nbStep += 1
    wait = pygame.time.wait(0)
    # Display the screen
    pygame.display.flip()