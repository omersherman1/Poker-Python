import socket
import threading

def func1():
    pass

# Global variable to store connected clients
connected_clients = []

def handle_client(client_socket, game_name):
    try:
        print(f"Connection from {client_socket.getpeername()} to {game_name}")
        # Send a welcome message to the client
        welcome_message = f"Welcome to {game_name} Poker! You are now connected to the server."
        client_socket.sendall(welcome_message.encode())

        # Do more processing as needed

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        # Remove the client from the list when the connection is closed
        connected_clients.remove(client_socket)
        client_socket.close()
        print(f"Connection to {game_name} closed.")

def start_server():
    server_address = ('127.0.0.1', 5556)  # Listen on all available interfaces
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print("Server is listening for incoming connections...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            connected_clients.append(client_socket)

            # Start a new thread to handle the client
            game_name = "Game 1"  # You may want to pass the actual game name
            client_handler = threading.Thread(target=handle_client, args=(client_socket, game_name))
            client_handler.start()

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()