class BingoCardEntry(object):

    def __init__(self, value):
        self.value = value
        self.is_called = False

    def mark_value(self, value):
        if self.value == value:
            self.is_called = True

    def to_string(self):
        return '[ value={}, called={} ]'.format(self.value, self.is_called)


class BingoCard(object):

    def __init__(self):
        self.rows = []
        self.last_number_called = None

    def add_row(self, row_str):
        values_str = row_str.split()
        row = []
        for value in values_str:
            entry = BingoCardEntry(value)
            row.append(entry)
        self.rows.append(row)

    def mark_value(self, value):
        self.last_number_called = value
        for row in self.rows:
            for entry in row:
                entry.mark_value(value)

    def is_winner(self):
        return self.is_row_winner() or self.is_column_winner()

    def is_row_winner(self):
        for row in self.rows:
            if self.is_line_winner(row):
                return True
        return False

    def is_column_winner(self):
        for column_index in range(len(self.rows[0])):
            column = []
            for row in self.rows:
                column.append(row[column_index])
            if self.is_line_winner(column):
                return True
        return False

    def is_line_winner(self, row_or_column):
        for entry in row_or_column:
            if not entry.is_called:
                return False
        return True

    def score(self):
        score = 0
        for row in self.rows:
            for entry in row:
                if not entry.is_called:
                    score += int(entry.value)
        score *= int(self.last_number_called)
        return score

    def to_string(self):
        result = 'is_winner={}, score={}\n'.format(self.is_winner(), self.score())
        for row in self.rows:
            for entry in row:
                result += '{}, '.format(entry.to_string())
            result += '\n'
        return result


class BingoGame(object):

    def __init__(self, called_numbers):
        self.called_numbers = called_numbers.split(',')
        self.cards = []

    def play(self):
        first_winning_card = None
        last_winning_card = None
        for value in self.called_numbers:
            for card in self.cards:
                if not card.is_winner():
                    card.mark_value(value)
                    if card.is_winner():
                        if not first_winning_card:
                            first_winning_card = card
                        last_winning_card = card

        print('First winning card')
        print(first_winning_card.to_string())
        print('Last winning card')
        print(last_winning_card.to_string())

    def add_card(self, card):
        self.cards.append(card)

    def print(self):
        print('called_numbers: {}'.format(self.called_numbers))
        for card in self.cards:
            print('{}'.format(card.to_string()))


def main():
    with open('bingo.data', 'r') as data_file:
        line = data_file.readline()
        bingo_game = BingoGame(line)
        line = data_file.readline()
        bingo_card = None
        while line:
            if not line.strip():
                if bingo_card:
                    bingo_game.add_card(bingo_card)
                bingo_card = BingoCard()
                line = data_file.readline()
                continue
            bingo_card.add_row(line.strip())
            line = data_file.readline()
        if bingo_card:
            bingo_game.add_card(bingo_card)

        bingo_game.play()


main()
