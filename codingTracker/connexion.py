class Connexion:
    def __init__(self, host="127.0.0.1", port=10000):
        self.host = host
        self.port = port
        self.reader, self.writer = asyncio.open_connection(host, port)

    def update(self):
        pass


