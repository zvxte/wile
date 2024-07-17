class Player:
    def __init__(self, username: str, rating: int):
        if not username or not rating:
            raise ValueError("Invalid arguments")
        self.username = username
        self.rating = rating

    def __repr__(self) -> str:
        return f"Player({self.username}, {self.rating})"
