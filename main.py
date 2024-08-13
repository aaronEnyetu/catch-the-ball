import tkinter as tk
import random

# Create the main window
root = tk.Tk()
root.title("Catch the Ball Game")
root.geometry("600x400")

# Define game variables
paddle_width = 100
paddle_height = 20
ball_radius = 10
ball_speed = 5
game_over = False

# Create a canvas to draw on
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

# Create the paddle
paddle = canvas.create_rectangle(250, 380, 250 + paddle_width, 380 + paddle_height, fill="blue")

# Function to create a new ball
def create_ball():
    """Create a new ball at the top of the canvas."""
    return canvas.create_oval(
        random.randint(10, 590 - ball_radius * 2), 
        50, 
        random.randint(10, 590 - ball_radius * 2) + ball_radius * 2, 
        50 + ball_radius * 2, 
        fill="red"
    )

# Initialize ball
ball = create_ball()

def move_paddle(event):
    """Move the paddle left or right."""
    x = event.x
    if x < paddle_width / 2:
        x = paddle_width / 2
    elif x > 600 - paddle_width / 2:
        x = 600 - paddle_width / 2
    
    canvas.coords(paddle, x - paddle_width / 2, 380, x + paddle_width / 2, 380 + paddle_height)

def move_ball():
    """Move the ball and check for collisions."""
    global game_over
    
    if game_over:
        return

    coords = canvas.coords(ball)
    canvas.move(ball, 0, ball_speed)
    
    # Check if ball hits the bottom
    if coords[3] >= 400:
        end_game()
        return
    
    # Check for collision with the paddle
    if coords[2] > canvas.coords(paddle)[0] and coords[0] < canvas.coords(paddle)[2]:
        if coords[3] >= canvas.coords(paddle)[1]:
            canvas.coords(ball, random.randint(10, 590 - ball_radius * 2), 50, random.randint(10, 590 - ball_radius * 2) + ball_radius * 2, 50 + ball_radius * 2)
    
    root.after(20, move_ball)

def end_game():
    """End the game and display a game over message."""
    global game_over
    game_over = True
    canvas.create_text(300, 200, text="Game Over", fill="black", font=("Arial", 24))
    canvas.create_text(300, 250, text="Click to Restart", fill="black", font=("Arial", 16))
    canvas.bind("<Button-1>", restart_game)

def restart_game(event):
    """Restart the game."""
    global game_over
    game_over = False
    
    # Delete all items on the canvas
    canvas.delete("all")
    
    # Recreate paddle and ball
    canvas.create_rectangle(250, 380, 250 + paddle_width, 380 + paddle_height, fill="blue")
    global ball
    ball = create_ball()
    
    # Start moving the ball
    move_ball()

# Bind mouse movement to the paddle
canvas.bind("<Motion>", move_paddle)

# Start moving the ball
move_ball()

# Start the Tkinter event loop
root.mainloop()
