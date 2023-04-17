import tkinter as tk
import requests


# Make a request to the random-word-api
url = "https://random-word-api.herokuapp.com/word"
response = requests.get(url)
# Extract a random word from the response
if response.status_code == 200:
    word = response.json()[0]
else:
    word = None


# Number of guesses
num_guesses = 6

# Current guesses
guesses = []

# Create the main window
root = tk.Tk()
root.title("Hangman Game word are guessed from web")

# Create the canvas
canvas = tk.Canvas(root, width=420, height=350)
canvas.pack()

# Create the hangman pole
canvas.create_line(50, 350, 200, 350)
canvas.create_line(125, 350, 125, 50)
canvas.create_line(125, 50, 275, 50)
canvas.create_line(275, 50, 275, 100)
# Create the word display
word_display = []
for i in range(len(word)):
    word_display.append("_ ")
text = "".join(word_display)
word_label = tk.Label(root, text=text, font=('Arial', 25))
word_label.pack()

# Create the input label and box
input_label = tk.Label(root, text="Guess a letter:", font=('Arial', 12))
input_label.pack()
input_box = tk.Entry(root, font=('Arial', 15))
input_box.pack()

# Create the message label
message_label = tk.Label(root, text="")
message_label.pack()


# Function to check the guess
def check_guess():
    global num_guesses
    global guesses
    guess = input_box.get()
    input_box.delete(0, tk.END)
    if guess in guesses:
        message_label.config(text="You already guessed that letter!")
    elif guess in word:
        guesses.append(guess)
        for x in range(len(word)):
            if word[x] == guess:
                word_display[x] = guess + " "
        word_text = "".join(word_display)
        word_label.config(text=word_text)
        if "_" not in word_display:
            message_label.config(text="You win!", font=('Arial', 15), fg='Blue')
    else:
        guesses.append(guess)
        num_guesses -= 1
        if num_guesses == 0:
            message_label.config(text="You lose! The word was " + word + ".", font=('Arial', 15), fg='Red')
        else:
            message_label.config(text="Wrong guess! You have " + str(num_guesses) + " guesses left.")
        draw_hangman(num_guesses)


# Function to draw the hangman
def draw_hangman(num):
    if num == 5:
        canvas.create_oval(250, 100, 300, 150)
    elif num == 4:
        canvas.create_line(275, 150, 275, 225)
    elif num == 3:
        canvas.create_line(275, 175, 250, 200)
    elif num == 2:
        canvas.create_line(275, 175, 300, 200)
    elif num == 1:
        canvas.create_line(275, 225, 250, 250)
    elif num == 0:
        canvas.create_line(275, 225, 300, 250)


# Function to reset the game
def reset_game():
    global word
    global num_guesses
    global guesses
    global word_display
    web_url = "https://random-word-api.herokuapp.com/word"
    web_response = requests.get(web_url)

    # Extract a random word from the response
    if web_response.status_code == 200:
        word = web_response.json()[0]
    else:
        word = None
    num_guesses = 6
    guesses = []
    word_display = []
    for x in range(len(word)):
        word_display.append("_ ")
    web_text = "".join(word_display)
    word_label.config(text=web_text)
    message_label.config(text="")
    canvas.delete("all")
    canvas.create_line(50, 350, 200, 350)
    canvas.create_line(125, 350, 125, 50)
    canvas.create_line(125, 50, 275, 50)
    canvas.create_line(275, 50, 275, 100)
    submit_button.config(state=tk.NORMAL)


# Create the submit button
submit_button = tk.Button(root, text="Submit", font=('Arial', 15), bd=10, command=check_guess)
submit_button.pack()
# Play again
submit_button = tk.Button(root, text="Play again", font=('Arial', 15), bd=10, command=reset_game)
submit_button.pack()
# Start the game
root.mainloop()
