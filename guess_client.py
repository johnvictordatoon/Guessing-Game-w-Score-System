
# Client

import socket

host = "localhost"
port = 7777

s = socket.socket()
s.connect((host, port))

# received the banner
data = s.recv(1024)

while True:
    # print banner
    print(data.decode().strip())

    # let the user choose the difficulty level
    difficulty = input("\nEnter your choice (a, b, c, d): ").strip().lower()

    # send the difficulty choice to the server
    s.sendall(difficulty.encode())

    if difficulty == "d":
        print("Thank you for playing!")
        break

    while True:
        print("Enter Guess: ")
        user_input = input("").strip()
        s.sendall(user_input.encode())
        
        reply = s.recv(1024).decode().strip()
        if "Correct" in reply:
            print(reply)
            break
        print(reply)

s.close()