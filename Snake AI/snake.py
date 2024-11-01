import pygame
import random
from GeneticAI import Controller
from GeneticAI import AIController
from GeneticAI import AITrainedControler


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
        # self.body = [(4, 8), (3, 8), (2, 8), (1, 8), (0, 8), (0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (16, 1), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 7), (16, 8), (16, 9), (16, 10), (16, 11), (16, 12), (16, 13), (16, 14)]
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
    


mode_input = input("Choose the mode (1: Human, 2: AI Training, 3: AI Trained): ").strip()
population = 100
display = True


if mode_input == '1':
    controller = HumanController()
    training = False
    human = True
elif mode_input == '2':
    controller = AIController(population)
    display_input = input("Display the training ? (y/n)").strip()
    if display_input == 'n':
        display = False
    training = True
    human = False
elif mode_input == '3':
    controller = AITrainedControler()
    training = False
    human = False
else:
    print("Invalid input. Defaulting to Human mode.")
    controller = HumanController()
    training = False

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
    
mySnake = Snake()

fruit = (random.randint(0, 16), random.randint(0, 14))
while mySnake.check_object_collision(fruit):
    fruit = (random.randint(0, 16), random.randint(0, 14))
screen.fill(GREEN)



score = 0
numGenome = 0
limit = 1000
if training:
    limit = 100
nbStep = 0
nbStepTotal = 0
nbGeneration = 0
if training:
    print("New Generation" + str(nbGeneration))

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if training:
                controller.saveBestGenome()
                #controller.saveTrainingState()
            running = False

    # Get the direction from the controller
    if training:
        direction = controller.get_direction(mySnake.get_status(fruit),numGenome)
    else:    
        if human:
            direction = controller.get_direction()
        else:
            direction = controller.get_direction(mySnake.get_status(fruit))

    if direction:
        if (direction == "up" and mySnake.direction != "down") or (direction == "down" and mySnake.direction != "up") or (direction == "left" and mySnake.direction != "right") or (direction == "right" and mySnake.direction != "left"):
            mySnake.direction = direction

    # Update the game state
    mySnake.move()
    if mySnake.check_wall() or mySnake.check_collision() or nbStep > limit:
        nbStep = 0
        if(display):
            font = pygame.font.Font(None, 74)  # 74 est la taille de la police
            message = f"Game Over. Score: {score}"
            overlay = pygame.Surface((850, 750))  # Créer une surface de la taille de l'écran
            overlay.set_alpha(150)  # Définir la transparence (0 = transparent, 255 = opaque)
            overlay.fill(GRAY)  # Colorier la surface avec du gris

        # Afficher le rectangle grisé
            screen.blit(overlay, (0, 0))
            # Rendre le message texte
            text = font.render(message, True, WHITE)

            # Obtenir la position du texte (centré)
            text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

            # Afficher le texte sur l'écran
            screen.blit(text, text_rect)

        if(training):
            controller.setFitness(numGenome,score)
            nbStepTotal = 0
            numGenome += 1
            numGenome = numGenome % population
            limit = 100
            if numGenome == 0:
                nbGeneration += 1
                print("New Generation" + str(nbGeneration))
                controller.newGeneration(nbGeneration)

        score = 0
        mySnake.reset()
        fruit = (random.randint(0, 16), random.randint(0, 14))
        while mySnake.check_object_collision(fruit):
            fruit = (random.randint(0, 16), random.randint(0, 14))

        if(display):
            pygame.display.flip()
        if not training:
            wait = pygame.time.wait(1000)
    
    if mySnake.check_fruit(fruit):
        mySnake.grow()
        score += 1
        if training:
            limit += 3
        nbStep = 0
        while mySnake.check_object_collision(fruit):
            fruit = (random.randint(0, 16), random.randint(0, 14))

    # Draw everything

    # Draw the grid
    if(display):
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
    nbStepTotal += 1
    if not training:
        if(human):
            wait = pygame.time.wait(100)
        else:
            wait = pygame.time.wait(10)
    # Display the screen
    if(display):
        pygame.display.flip()