import socket
import threading


class Socketing:
    def __init__(self, server_address=('127.0.0.1', 68), game_name="Game 1"):
        self.server_address = server_address
        self.game_name = game_name
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_clients = []
        self.game_over = False

    def handle_client(self, client_socket):
        try:
            print(f"Connection from {client_socket.getpeername()} to {self.game_name}")
            # Send a welcome message to the client
            welcome_message = f"Welcome to {self.game_name} Poker! You are now connected to the server."
            client_socket.sendall(welcome_message.encode())

            # Do more processing as needed

        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            # Remove the client from the list when the connection is closed
            self.connected_clients.remove(client_socket)
            client_socket.close()
            print(f"Connection to {self.game_name} closed.")

    def start_server(self):
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(5)

        print("Server is listening for incoming connections...")

        try:
            while not self.game_over:
                client_socket, client_address = self.server_socket.accept()
                self.connected_clients.append(client_socket)

                # Start a new thread to handle the client
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()

        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server_socket.close()

    def connect_to_server(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to the server
            client_socket.connect(self.server_address)
            print("Connected to the server.")

            # Send data to the server
            message = "Hello, server!"
            client_socket.sendall(message.encode())

            # Receive data from the server
            data = client_socket.recv(1024)
            print("Received:", data.decode())

        finally:
            # Close the connection
            client_socket.close()

    def end_game(self):
        self.game_over = True

if __name__ == "__main__":
    socketing = Socketing()
    # Start the server in a separate thread
    server_thread = threading.Thread(target=socketing.start_server)
    server_thread.start()

    # Connect to the server
    socketing.connect_to_server()

    # End the game (for demonstration purposes)
    socketing.end_game()
