from .color import Color


class SanMove:
    """
    Represents chess move in Algebraic Notation.

    Raises:
        TypeError
        ValueError
    """

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Invalid argument types", type(value))
        if not value or len(value) > 7:
            raise ValueError(value)

        self.value = value

    def __repr__(self) -> str:
        return f"SanMove({self.value})"


class UciMove:
    """
    Represents chess move in Universal Chess Interface notation.

    Raises:
        TypeError
        ValueError
    """

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Invalid argument types", type(value))
        if not value or len(value) > 5:
            raise ValueError(value)

        self.value = value

    def __repr__(self) -> str:
        return f"UciMove({self.value})"


class Move:
    """
    Represents chess move

    Raises:
        TypeError
    """

    def __init__(
        self,
        san_move: SanMove,
        uci_move: UciMove,
        side: Color,
    ):
        if (
            not isinstance(san_move, SanMove)
            or not isinstance(uci_move, UciMove)
            or not isinstance(side, Color)
        ):
            raise TypeError("Invalid argument types")

        self.san_move = san_move
        self.uci_move = uci_move
        self.side = side

    def __repr__(self) -> str:
        return f"Move(\n{self.san_move}\n{self.uci_move}\n{self.side}\n)"
