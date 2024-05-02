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

def get_username(conn):
    username = conn.recv(1024).decode().strip()
    return username

def generate_random_int(difficulty):
    if difficulty == "a":
        return random.randint(1, 50)
    elif difficulty == "b":
        return random.randint(1, 100)
    elif difficulty == "c":
        return random.randint(1, 500)
    else:
        return None

def update_score(username, difficulty, tries):
    if username not in player_scores:
        player_scores[username] = {}
    player_scores[username][difficulty] = tries

def display_leaderboard():
    print("\n==Leaderboard==")
    for username, scores in sorted(player_scores.items()):
        for difficulty, tries in sorted(scores.items(), key=lambda x: x[1]):
            print(f"Player Name: {username}, Difficulty: {difficulty}, Number of Tries: {tries}")

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server Port: {port}")
print("Waiting for connection...")

while True:
    conn, addr = s.accept()

    # Get username from the client
    username = get_username(conn)
    print(f"{username} is in the server.")

    print(f"User address: {addr[0]}")
    conn.sendall(banner.encode())

    left_server = False

    while True:
        # receive difficulty choice from the client
        difficulty = conn.recv(1024).decode().strip().lower()

        if difficulty == "d":
            print(f"{username} left the server.")
            display_leaderboard()  # Show leaderboard
            left_server = True
            break

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
                update_score(username, difficulty, tries)  # Update player score
                break
            elif guess > guessme:
                conn.sendall(b"\nGuess Lower!")
            else:
                conn.sendall(b"\nGuess Higher!")

    if left_server:
        break
conn.close()