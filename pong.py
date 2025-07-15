import pygame
import random

# Initialisation de pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Casse-Brique")

# Couleurs
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)

# Fonction pour réinitialiser le jeu
def reset_game():
    global paddle, ball, ball_dx, ball_dy, bricks, game_over
    paddle = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 50, 100, 10)
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 10, 10)
    ball_dx, ball_dy = 4, -4
    bricks = [pygame.Rect(col * (WIDTH // 8), row * 30, (WIDTH // 8) - 2, 30 - 2) for row in range(5) for col in range(8)]
    game_over = False

reset_game()

# Boucle du jeu
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()
    
    # Déplacement de la raquette
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-6, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(6, 0)
    
    if not game_over:
        # Déplacement de la balle
        ball.move_ip(ball_dx, ball_dy)
        
        # Collision avec les murs
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_dx = -ball_dx
        if ball.top <= 0:
            ball_dy = -ball_dy
        
        # Collision avec la raquette
        if ball.colliderect(paddle):
            ball_dy = -ball_dy
        
        # Collision avec les briques
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_dy = -ball_dy
                break
        
        # Vérifier la défaite
        if ball.bottom >= HEIGHT:
            game_over = True
    
    # Dessiner les éléments
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)
    
    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over! Appuyez sur 'R' pour recommencer", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
