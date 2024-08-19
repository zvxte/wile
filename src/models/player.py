class Player:
    """
    Represents chess player

    Raises:
        TypeError
        ValueError
    """

    def __init__(self, username: str, rating: int):
        if not isinstance(username, str) or not isinstance(rating, int):
            raise TypeError("Invalid argument types")

        if not username:
            raise ValueError("Invalid argument values")

        self.username = username
        self.rating = rating

    def __repr__(self) -> str:
        return f"Player({self.username}, {self.rating})"
