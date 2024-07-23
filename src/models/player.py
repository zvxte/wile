class Player:
    """
    Represents chess player
    
    Raises:
        AssertionError: If arguments with invalid types are provided.
        ValueError: If argument values are falsy.
    """
    def __init__(self, username: str, rating: int):
        assert isinstance(username, str), ["Invalid username type", username]
        assert isinstance(rating, int), ["Invalid rating type", rating]

        if not username:
            raise ValueError("Invalid arguments")

        self.username = username
        self.rating = rating

    def __repr__(self) -> str:
        return f"Player({self.username}, {self.rating})"
