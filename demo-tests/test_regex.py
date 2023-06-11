import random
import pytest
import logging
import faker

fake = faker.Faker()


def generate_random_text_with_pattern(pattern, num_lines, pattern_interval):
    lines = []
    for i in range(num_lines):
        if i % pattern_interval == 0:
            line = f"This line contains the pattern: {pattern}"
            line += "\n"
            line += f"This line contains no pattern"
            line += "\n"
            line += f"This line contains the pattern: {pattern}"
            line += "\n"
            line += f"This line contains the pattern: {pattern}"
            line += "\n"
            line += f"This line contains the pattern: {pattern}"
            line += "\n"
        else:
            line = "Random text line"
        lines.append(line)
    return lines


# @pytest.mark.parametrize(
#     "pattern, num_lines, pattern_interval, expected",
#     [
#         ("  *->", 10, 3),

# def test_random_text_with_pattern(capsys):
#     logger = logging.getLogger()
#     pattern = "  *->"
#     num_lines = random.randint(10,100)
#     pattern_interval = 3

#     lines = generate_random_text_with_pattern(pattern, num_lines, pattern_interval)

#     for line in lines:
#         print(line)
#         logger.info(line)

#     captured = capsys.readouterr()
#     console_output = captured.out

#     assert pattern in console_output
