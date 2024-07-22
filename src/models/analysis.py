class Analysis:
    """
    Represents engine analysis

    Raises:
        AssertionError: If arguments with invalid types are provided.
    """

    def __init__(self, uci_name: str, multipv: int, score_name: str, score_value: int):
        assert isinstance(uci_name, str), ["Invalid uci_name type", uci_name]
        assert isinstance(multipv, int), ["Invalid multipv type", multipv]
        assert isinstance(score_name, str), ["Invalid score_name type", score_name]
        assert isinstance(score_value, int), ["Invalid score_value type", score_value]

        self.uci_name = uci_name
        self.multipv = multipv
        self.score_name = score_name
        self.score_value = score_value
