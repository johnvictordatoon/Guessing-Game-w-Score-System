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

def generate_random_int(difficulty):
    if difficulty == "a":
        return random.randint(1, 50)
    elif difficulty == "b":
        return random.randint(1, 100)
    elif difficulty == "c":
        return random.randint(1, 500)
    else:
        raise ValueError("Invalid difficulty level")

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server Port {port}")

while True:
    conn, addr = s.accept()
    print(f"New User: {addr[0]}")
    conn.sendall(banner.encode())

    while True:
        # receive difficulty choice from the client
        difficulty = conn.recv(1024).decode().strip().lower()

        if difficulty == "d":
            print("(user) left the server.")
            conn.close()
            break

        # generate random number based on difficulty
        guessme = generate_random_int(difficulty)
        print(f"Generated number to guess: {guessme}")

        while True:
            client_input = conn.recv(1024)
            guess = int(client_input.decode().strip())
            print(f"User guess attempt: {guess}")
            if guess == guessme:
                conn.sendall(b"Correct Answer!")
                break
            elif guess > guessme:
                conn.sendall(b"\nGuess Lower!\n")
            else:
                conn.sendall(b"\nGuess Higher!\n")