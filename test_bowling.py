import pytest
from bowling import score_game


def test_provided_example_game():
    rolls = ["8", "/", "5", "4", "9", "0", "X", "X", "5", "/", "5", "3", "6", "3", "9", "/", "9", "/", "X"]
    assert score_game(rolls) == [15, 24, 33, 58, 78, 93, 101, 110, 129, 149]


def test_perfect_game_returns_300():
    rolls = ["X"] * 12
    assert score_game(rolls)[-1] == 300


def test_all_spares_returns_150():
    rolls = ["5", "/"] * 10 + ["5"]
    assert score_game(rolls)[-1] == 150


def test_all_open_frames_returns_90():
    rolls = ["9", "0"] * 10
    assert score_game(rolls) == [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]


def test_tenth_frame_strike_with_two_bonus_rolls():
    rolls = ["0", "0"] * 9 + ["X", "5", "4"]
    assert score_game(rolls)[-1] == 19


def test_tenth_frame_spare_with_one_bonus_roll():
    rolls = ["0", "0"] * 9 + ["5", "/", "7"]
    assert score_game(rolls)[-1] == 17


def test_tenth_frame_open_frame_ends_game():
    rolls = ["0", "0"] * 9 + ["5", "4"]
    assert score_game(rolls)[-1] == 9


@pytest.mark.parametrize(
    "rolls",
    [
        ["/", "5"] + ["0", "0"] * 9,
        ["5", "A"] + ["0", "0"] * 9,
        ["5", "6"] + ["0", "0"] * 9,
        ["0", "0"] * 9 + ["5", "4", "1"],
        ["0", "0"] * 9 + ["5", "/", "4", "2"],
    ],
)
def test_invalid_games_raise_value_error(rolls):
    with pytest.raises(ValueError):
        score_game(rolls)
