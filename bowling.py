from typing import List


VALID_DIGITS = set("0123456789")


class BowlingScorer:
    """
    Bowling scorer using Option B: a flat list of rolls.

    Example input:
        ["8", "/", "5", "4", "9", "0", "X", "X", "5", "/", "5", "3", "6", "3", "9", "/", "9", "/", "X"]

    Returns:
        A list of cumulative scores after each of the 10 frames.
    """

    def score_game(self, rolls: List[str]) -> List[int]:
        if not rolls:
            raise ValueError("Roll list cannot be empty.")

        normalized_rolls = [str(roll).upper() for roll in rolls]
        self._validate_symbols(normalized_rolls)

        frames = self._parse_frames(normalized_rolls)
        roll_values = self._build_roll_values(frames)

        scores = []
        total_score = 0
        roll_index = 0

        for frame_number in range(10):
            frame = frames[frame_number]

            if frame_number == 9:
                frame_score = sum(self._frame_values(frame))
            elif self._is_strike(frame):
                frame_score = 10 + roll_values[roll_index + 1] + roll_values[roll_index + 2]
            elif self._is_spare(frame):
                frame_score = 10 + roll_values[roll_index + 2]
            else:
                frame_score = sum(self._frame_values(frame))

            total_score += frame_score
            scores.append(total_score)
            roll_index += len(self._frame_values(frame))

        return scores

    def _validate_symbols(self, rolls: List[str]) -> None:
        for roll in rolls:
            if roll not in VALID_DIGITS and roll not in {"X", "/"}:
                raise ValueError(f"Invalid roll symbol: {roll}")

    def _parse_frames(self, rolls: List[str]) -> List[List[str]]:
        frames = []
        index = 0

        for frame_number in range(1, 10):
            if index >= len(rolls):
                raise ValueError("Incomplete game. Missing rolls before the 10th frame.")

            first = rolls[index]

            if first == "/":
                raise ValueError("Spare cannot be the first roll of a frame.")

            if first == "X":
                frames.append(["X"])
                index += 1
                continue

            if not first.isdigit():
                raise ValueError(f"Invalid first roll in frame {frame_number}: {first}")

            if index + 1 >= len(rolls):
                raise ValueError("Incomplete frame. Missing second roll.")

            second = rolls[index + 1]

            if second == "X":
                raise ValueError("Strike cannot be the second roll in frames 1-9.")

            if second == "/":
                frames.append([first, second])
            elif second.isdigit():
                if int(first) + int(second) > 10:
                    raise ValueError("Frame pin count cannot exceed 10 without a spare.")
                frames.append([first, second])
            else:
                raise ValueError(f"Invalid second roll in frame {frame_number}: {second}")

            index += 2

        tenth_frame = rolls[index:]
        self._validate_tenth_frame(tenth_frame)
        frames.append(tenth_frame)

        return frames

    def _validate_tenth_frame(self, frame: List[str]) -> None:
        if not frame:
            raise ValueError("Missing 10th frame.")

        first = frame[0]

        if first == "/":
            raise ValueError("Spare cannot be the first roll of the 10th frame.")

        if first == "X":
            if len(frame) != 3:
                raise ValueError("Strike in the 10th frame must have exactly two bonus rolls.")

            second = frame[1]
            third = frame[2]

            if second == "/":
                raise ValueError("Spare cannot appear immediately after a 10th-frame strike.")

            if second.isdigit() and third.isdigit():
                if int(second) + int(third) > 10:
                    raise ValueError("10th-frame bonus rolls cannot exceed 10 unless a strike is rolled.")

            if third == "/" and not second.isdigit():
                raise ValueError("Spare bonus roll must follow a numeric roll.")

            return

        if not first.isdigit():
            raise ValueError(f"Invalid first roll in the 10th frame: {first}")

        if len(frame) < 2:
            raise ValueError("10th frame is incomplete.")

        second = frame[1]

        if second == "X":
            raise ValueError("Strike cannot be the second roll unless the first roll was a strike.")

        if second == "/":
            if len(frame) != 3:
                raise ValueError("Spare in the 10th frame must have exactly one bonus roll.")
            if frame[2] == "/":
                raise ValueError("Bonus roll cannot be a spare after a 10th-frame spare.")
            return

        if second.isdigit():
            if int(first) + int(second) > 10:
                raise ValueError("10th-frame pin count cannot exceed 10 without a spare.")
            if len(frame) != 2:
                raise ValueError("Extra rolls are not allowed after an open 10th frame.")
            return

        raise ValueError(f"Invalid second roll in the 10th frame: {second}")

    def _build_roll_values(self, frames: List[List[str]]) -> List[int]:
        values = []

        for frame in frames:
            values.extend(self._frame_values(frame))

        return values

    def _frame_values(self, frame: List[str]) -> List[int]:
        values = []

        for roll in frame:
            if roll == "X":
                values.append(10)
            elif roll == "/":
                if not values:
                    raise ValueError("Spare cannot be calculated without a previous roll.")
                values.append(10 - values[-1])
            else:
                values.append(int(roll))

        return values

    def _is_strike(self, frame: List[str]) -> bool:
        return frame[0] == "X"

    def _is_spare(self, frame: List[str]) -> bool:
        return len(frame) >= 2 and frame[1] == "/"


def score_game(rolls: List[str]) -> List[int]:
    return BowlingScorer().score_game(rolls)
