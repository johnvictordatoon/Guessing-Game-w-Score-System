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

    while True:
        # receive difficulty choice from the client
        difficulty = conn.recv(1024).decode().strip().lower()

        if difficulty == "d":
            print(f"{username} left the server.")
            conn.close()
            break

        guessme = generate_random_int(difficulty)
        if guessme is None:
            break
        print(f"Generated number to guess: {guessme}")

        # Guessing loop
        while True:
            client_input = conn.recv(1024)
            guess = int(client_input.decode().strip())
            print(f"{username} guess attempt: {guess}")
            if guess == guessme:
                conn.sendall(b"Correct Answer!")
                break
            elif guess > guessme:
                conn.sendall(b"\nGuess Lower!")
            else:
                conn.sendall(b"\nGuess Higher!")