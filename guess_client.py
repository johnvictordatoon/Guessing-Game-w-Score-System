# Client

import socket

host = "localhost"
port = 7777

s = socket.socket()
s.connect((host, port))

# Username prompt
username = input("Enter your username: ")
s.sendall(username.encode())
print(f"\nWelcome, {username}!")

# received the banner
data = s.recv(1024)

while True:
    # print banner
    print("\n", data.decode().strip())
    # let the user choose the difficulty level
    difficulty = input("\nEnter your choice (a, b, c, d): ").strip().lower()

    if difficulty == "a" or difficulty == "b" or difficulty == "c":
        s.sendall(difficulty.encode())
    elif difficulty == "d":
        print(f"Thank you for playing, {username}!")
        s.sendall(difficulty.encode())
        break
    else:
        print("Invalid difficulty selection.\n")
        continue

    while True:
        user_input = input("Enter Guess: ").strip()
        s.sendall(user_input.encode())
        
        reply = s.recv(1024).decode().strip()
        if "Correct" in reply:
            print(reply)
            break
        print(reply)

s.close()