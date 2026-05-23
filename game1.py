import pygame
import random
import cv2
import mediapipe as mp
import requests

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Finger Gesture-Controlled Game")

# Clock for FPS
clock = pygame.time.Clock()

# Load Images
sky_img = pygame.image.load("sky.png")
road_img = pygame.image.load("road_texture.png")
left_building_img = pygame.image.load("left_building.png")
right_building_img = pygame.image.load("right_building.png")
car_img = pygame.image.load("car.png")
character_img = pygame.image.load("character.png")
coin_img = pygame.image.load("coin1.png")

# Scale Images
sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
road_img = pygame.transform.scale(road_img, (400, SCREEN_HEIGHT))
left_building_img = pygame.transform.scale(left_building_img, (100, 150))
right_building_img = pygame.transform.scale(right_building_img, (100, 150))
car_img = pygame.transform.scale(car_img, (50, 100))
character_img = pygame.transform.scale(character_img, (50, 50))
coin_img = pygame.transform.scale(coin_img, (30, 30))

# Game Variables
road_x = 200
character_x = SCREEN_WIDTH // 2
character_y = SCREEN_HEIGHT - 100
coin_count = 0

# Vehicle and Coin Dimensions
VEHICLE_WIDTH, VEHICLE_HEIGHT = 50, 100
COIN_WIDTH, COIN_HEIGHT = 30, 30

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Generate random positions without overlaps
def generate_positions(count, width, height, x_min, x_max, y_min, y_max, exclude_rects=[], safe_zone=None):
    positions = []
    while len(positions) < count:
        x = random.randint(x_min, x_max - width)
        y = random.randint(y_min, y_max - height)
        rect = pygame.Rect(x, y, width, height)

        # Avoid overlaps with other objects or the safe zone
        if not any(rect.colliderect(other) for other in exclude_rects + positions):
            if safe_zone is None or not rect.colliderect(safe_zone):
                positions.append(rect)
    return positions

# Define a safe zone around the character to avoid initial collision
character_safe_zone = pygame.Rect(character_x - 50, character_y - 100, 150, 200)

# Initialize vehicles and coins
vehicles = generate_positions(
    3, VEHICLE_WIDTH, VEHICLE_HEIGHT, road_x, road_x + 400, -600, -100, safe_zone=character_safe_zone
)
coins = generate_positions(
    3, COIN_WIDTH, COIN_HEIGHT, road_x + 50, road_x + 350, -600, -100, exclude_rects=vehicles, safe_zone=character_safe_zone
)

# Draw functions
def draw_background():
    screen.blit(sky_img, (0, 0))

def draw_road():
    screen.blit(road_img, (road_x, 0))

def draw_buildings():
    for i in range(0, SCREEN_HEIGHT, 150):
        screen.blit(left_building_img, (road_x - 100, i))
        screen.blit(right_building_img, (road_x + 400, i))

def draw_vehicles():
    for rect in vehicles:
        screen.blit(car_img, (rect.x, rect.y))

def draw_coins():
    for rect in coins:
        screen.blit(coin_img, (rect.x, rect.y))

# Update vehicle positions
def update_vehicles():
    for rect in vehicles:
        rect.y += 5
        if rect.y > SCREEN_HEIGHT:
            vehicles.remove(rect)
            new_vehicle = generate_positions(1, VEHICLE_WIDTH, VEHICLE_HEIGHT, road_x, road_x + 400, -600, -100, vehicles + coins)
            vehicles.append(new_vehicle[0])

# Update coin positions
def update_coins():
    global coin_count
    for rect in coins:
        rect.y += 5
        if rect.y > SCREEN_HEIGHT:
            coins.remove(rect)
            new_coin = generate_positions(1, COIN_WIDTH, COIN_HEIGHT, road_x + 50, road_x + 350, -600, -100, vehicles + coins)
            coins.append(new_coin[0])

        # Check if the character collects the coin
        character_rect = pygame.Rect(character_x, character_y, 50, 50)
        if rect.colliderect(character_rect):
            coins.remove(rect)
            new_coin = generate_positions(1, COIN_WIDTH, COIN_HEIGHT, road_x + 50, road_x + 350, -600, -100, vehicles + coins)
            coins.append(new_coin[0])
            coin_count += 1

# Check collision with vehicles
def check_collision():
    character_rect = pygame.Rect(character_x, character_y, 50, 50)
    for rect in vehicles:
        if rect.colliderect(character_rect):
            return True
    return False

# Get finger position and draw landmarks
def get_finger_position_and_draw(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    finger_x = SCREEN_WIDTH // 2

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
            )
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            finger_x = int(index_tip.x * SCREEN_WIDTH)

    return finger_x, frame

# Initialize webcam
cap = cv2.VideoCapture(0)

def game_over(score):
    """Notify the Flask server that the game is over"""
    response = requests.post('http://127.0.0.1:5000/game-over', json={'score': score})
    if response.status_code == 200:
        print("Game over sent successfully!")
    else:
        print("Failed to send game over!")

# Main game loop
running = True
while running:
    ret, frame = cap.read()
    if not ret:
        break

    character_x, frame = get_finger_position_and_draw(frame)
    draw_background()
    draw_road()
    draw_buildings()
    draw_vehicles()
    draw_coins()
    screen.blit(character_img, (character_x, character_y))

    update_vehicles()
    update_coins()

    if check_collision():
        print("Game Over!")
        game_over(coin_count)  # Send the final score to the Flask server
        running = False

    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Coins: {coin_count}", True, (255, 255, 0))
    screen.blit(text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)
    cv2.imshow("Webcam", frame)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
