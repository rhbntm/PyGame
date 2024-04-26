import random
import pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Matching Game")

# Load images
tile_images = {
    '1.png': pygame.image.load('./images/1 (1).png'),
    '2.png': pygame.image.load('./images/2 (1).png'),
    '3.png': pygame.image.load('./images/3 (1).png'),
    '4.png': pygame.image.load('./images/4 (1).png'),
    '5.png': pygame.image.load('./images/5 (1).png'),
    '6.png': pygame.image.load('./images/6 (1).png'),
    '7.png': pygame.image.load('./images/7 (1).png'),
    '8.png': pygame.image.load('./images/8 (1).png'),
    # Add more images as needed
}

# Initialize game board
game_board = [['' for _ in range(4)] for _ in range(4)]

def render_board(game_board):
    tile_width = 30
    tile_height = 30
    padding_x = 70 # Horizontal padding between tiles
    padding_y = 70  # Vertical padding between tiles
    
    for i in range(len(game_board)):
        for j in range(len(game_board[0])):
            tile = game_board[i][j]
            tile_image = tile_images[tile]  # Get the corresponding image
            x = j * (tile_width + padding_x)
            y = i * (tile_height + padding_y)
            screen.blit(tile_image, (x, y))




# Get list of image filenames
images = list(tile_images.keys())

# Shuffle and duplicate images to create pairs
random.shuffle(images)
pairs = images + images
print("Length of pairs:", len(pairs))  # Debug print
for i in range(4):
    for j in range(4):
        if pairs:
            game_board[i][j] = pairs.pop()
        else:
            break  # Exit the loop if there are no more elements in pairs


matched_tiles = set()
selected_tiles = []
last_selected_position = None

def handle_click(row, col):
    global selected_tiles
    global last_selected_position
    
    # Check if the clicked tile is already matched
    if (row, col) in matched_tiles:
        print("This tile is already matched!")
        return
    
    # Check if the clicked position is the same as the last selected position
    if (row, col) == last_selected_position:
        print("You cannot select the same position again!")
        return
    
    # Handle logic for when a tile is clicked
    clicked_tile = game_board[row][col]
    
    # Add the clicked tile to the selected tiles list
    selected_tiles.append((row, col))
    
    # Check if two tiles are selected
    if len(selected_tiles) == 2:
        # Get the row and column of the two selected tiles
        row1, col1 = selected_tiles[0]
        row2, col2 = selected_tiles[1]
        
        # Get the tiles at the selected positions
        tile1 = game_board[row1][col1]
        tile2 = game_board[row2][col2]
        
        # Check if the tiles have different positions and match
        if (row1, col1) != (row2, col2) and tile1 == tile2:
            print("Matched!")
            # Keep the tiles selected
            matched_tiles.add((row1, col1))
            matched_tiles.add((row2, col2))
            selected_tiles = []  # Reset the selected tiles list
        else:
            print("Not matched!")
            # Deselect the tiles
            selected_tiles = []
    elif len(selected_tiles) > 2:
        print("You can only select two tiles at a time!")
        # Reset the selected tiles list
        selected_tiles = []
    else:
        print("Selected tile:", clicked_tile)
    
    # Update the last selected position
    last_selected_position = (row, col)


# Main game loop
running = True
tile_width = 100
tile_height = 100
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            clicked_row = mouse_y // tile_height
            clicked_col = mouse_x // tile_width
            handle_click(clicked_row, clicked_col)

    # Update display
    render_board(game_board)
    pygame.display.flip()

pygame.quit()
