# Although my original revision of this worked correctly, I'm still trying to learn
# python features. This revision was after I looked at
# https://github.com/benediktwerner/AdventOfCode/blob/master/2021/day10/sol.py
#
# Things I learned:
#   - "for" loop has an "else" clause that is executed when the loop encounters no break or continue.
#   - // integer division
#   - If a constant is used in just one place, sometimes it's more readable to ditch the constant and use its value in
#     that place.

TOKEN_MATCH = {')': '(', '}': '{', ']': '[', '>': '<', '(': ')', '{': '}', '[': ']', '<': '>'}


with open('data.txt', 'r') as data_file:
    lines = data_file.read().splitlines()

tokens_by_line = []

for line in lines:
    tokens_by_line.append(list(line))

bad_tokens = []
completion_sequences = []
for line_idx in range(len(tokens_by_line)):
    tokens = []
    for col_idx in range(len(tokens_by_line[line_idx])):
        token = tokens_by_line[line_idx][col_idx]
        if token in [')', '}', ']', '>']:
            if token != TOKEN_MATCH[tokens[-1]]:
                bad_tokens.append(token)
                break
            else:
                tokens.pop()
        else:
            tokens.append(token)
    else:
        if len(tokens) != 0:
            completion_sequence = []
            for token in reversed(tokens):
                completion_sequence.append(TOKEN_MATCH[token])
            completion_sequences.append(completion_sequence)
            continue

score = 0
for token in bad_tokens:
    score += {')': 3, ']': 57, '}': 1197, '>': 25137}[token]
print('Part 1, corrupted lines score={}'.format(score))

incomplete_line_scores = []
for completion_sequence in completion_sequences:
    score = 0
    for token in completion_sequence:
        score = (score * 5) + {')': 1, ']': 2, '}': 3, '>': 4}[token]
    incomplete_line_scores.append(score)
incomplete_line_scores.sort()
middle_score = incomplete_line_scores[(len(incomplete_line_scores) - 1) // 2]
print('Part 2, middle incomplete line score={}'.format(middle_score))
