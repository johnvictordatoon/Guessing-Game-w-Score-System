# Server

import socket
import random

host = "localhost"
port = 7777
banner = """
== Guessing Game v1.0 ==

Difficulty Options:
a. Easy (1-50)
b. Medium (1-100)
c. Hard (1-500)
d. Exit
"""

# Dictionary to store player scores
player_scores = {}

# Getting username to the server
def get_username(conn):
    username = conn.recv(1024).decode().strip()
    return username

# Generating random number based on difficulty
def generate_random_int(difficulty):
    if difficulty == "a":
        return random.randint(1, 50)
    elif difficulty == "b":
        return random.randint(1, 100)
    elif difficulty == "c":
        return random.randint(1, 500)
    else:
        return None

# Update Score
def update_score(username, difficulty, tries):
    if username not in player_scores:
        player_scores[username] = {}
    player_scores[username][difficulty] = tries

# Sorting and displaying leaderboard from highest difficulty and less guesses to lowest difficulty and more guesses 
def display_leaderboard():
    difficulty_mapping = {"a": "Easy", "b": "Medium", "c": "Hard"}
    print("\n==Leaderboard==")
    for username, scores in sorted(player_scores.items()):
        for difficulty, tries in sorted(scores.items(), key=lambda x: x[1]):
            difficulty_name = difficulty_mapping.get(difficulty, "Unknown")
            print(f"Player Name: {username}, === Difficulty: {difficulty_name}, === Number of Tries: {tries}\n")

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print(f"Server Port: {port}")
print("Waiting for connection...")

while True:
    # Accepting connection
    conn, addr = s.accept()

    # Get username from the client
    username = get_username(conn)
    print(f"{username} is in the server.")
    print(f"User address: {addr[0]}")

    # Send the banner to the client
    conn.sendall(banner.encode())

    while True:
        # receive difficulty choice from the client
        difficulty = conn.recv(1024).decode().strip().lower()
        if difficulty == "d":
            print(f"{username} left the server.")
            display_leaderboard()
            break
        
        # Generates a random number based on difficulty and "showing" the generated number to the server (in comment)
        guessme = generate_random_int(difficulty)
        if guessme is None:
            break
        print(f"Generated number to guess: {guessme}")

        # Guessing loop
        tries = 0
        while True:
            client_input = conn.recv(1024)
            guess = int(client_input.decode().strip())
            print(f"{username} guess attempt: {guess}")
            tries += 1
            if guess == guessme:
                conn.sendall(b"Correct Answer!")
                update_score(username, difficulty, tries)
                break
            elif guess > guessme:
                conn.sendall(b"\nGuess Lower!")
            else:
                conn.sendall(b"\nGuess Higher!")
    conn.close()