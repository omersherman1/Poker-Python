import http.server
import json

board_status_data = \
    {
        "Round": 1,
        "CurrentBet": 100,
        "MinimumBet": 50,
        "CurrentPlayer": "Player1",
        "CommunityCards": [
            {
                "Suit": "Hearts",
                "Rank": "A",
                "isHidden": True
            },
            {
                "Suit": "Spades",
                "Rank": "Q",
                "isHidden": True
            },
            {
                "Suit": "Clubs",
                "Rank": "10",
                "isHidden": True
            },
            {
                "Suit": "Spades",
                "Rank": "2",
                "isHidden": True
            },
            {
                "Suit": "Diamonds",
                "Rank": "6",
                "isHidden": True
            }
        ],
        "Players": [
            {
                "Name": "Player1",
                "Money": 10000,
                "Bet": 100,
                "Hand": [
                    {
                        "Suit": "Diamonds",
                        "Rank": "7",
                        "isHidden": True
                    },
                    {
                        "Suit": "Diamonds",
                        "Rank": "4",
                        "isHidden": True
                    }
                ]
            },
            {
                "Name": "Player2",
                "Money": 10000,
                "Bet": 100,
                "Hand": [
                    {
                        "Suit": "Diamonds",
                        "Rank": "7",
                        "isHidden": True
                    },
                    {
                        "Suit": "Diamonds",
                        "Rank": "4",
                        "isHidden": True
                    }
                ]
            },
            {
                "Name": "Player3",
                "Money": 10000,
                "Bet": 100,
                "Hand": [
                    {
                        "Suit": "Diamonds",
                        "Rank": "7",
                        "isHidden": True
                    },
                    {
                        "Suit": "Diamonds",
                        "Rank": "4",
                        "isHidden": True
                    }
                ]
            },
            {
                "Name": "Player4",
                "Money": 10000,
                "Bet": 100,
                "Hand": [
                    {
                        "Suit": "Diamonds",
                        "Rank": "7",
                        "isHidden": True
                    },
                    {
                        "Suit": "Diamonds",
                        "Rank": "4",
                        "isHidden": True
                    }
                ]
            }
        ]
    }

class JsonRequestHandler(http.server.BaseHTTPRequestHandler):
    def set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length).decode()
        print(post_body)

        try:
            # data = json.loads(post_body)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"message": "Received JSON data"}
            self.wfile.write(json.dumps(board_status_data).encode())
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Invalid JSON format")

def run(server_class=http.server.HTTPServer, handler_class=JsonRequestHandler, port=8000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
