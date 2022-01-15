MAX_STEPS = 500


def get_adjacent_indexes(index):
    row, col = index
    candidate_indexes = [(row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1),
                         (row + 1, col), (row + 1, col - 1), (row, col - 1), (row - 1, col - 1)]
    adj_indexes = []
    for candidate_index in candidate_indexes:
        adj_row, adj_col = candidate_index
        if 0 <= adj_row < rows and 0 <= adj_col < cols:
            adj_indexes.append(candidate_index)
    return adj_indexes


def process_adjacent_cells(index):
    adjacent_indexes = get_adjacent_indexes(index)
    for adj_index in adjacent_indexes:
        if energy_levels[adj_index[0]][adj_index[1]] != 0:
            energy_levels[adj_index[0]][adj_index[1]] += 1
    check_for_flashes(adjacent_indexes)


def maybe_flash(index):
    flashed_indexes = []
    if index_flashed(index):
        flashed_indexes.append(index)
    return flashed_indexes


def process_flashes(indexes):
    for index in indexes:
        process_adjacent_cells(index)


def index_flashed(index):
    if energy_levels[index[0]][index[1]] > 9:
        energy_levels[index[0]][index[1]] = 0
        return True
    return False


def check_for_flashes(indexes):
    flashed_indexes = []
    for index in indexes:
        if index_flashed(index):
            flashed_indexes.append(index)
    process_flashes(flashed_indexes)


def count_flashes():
    count = 0
    for row in range(rows):
        for col in range(cols):
            if energy_levels[row][col] == 0:
                count += 1
    return count


def add_energy():
    for row in range(rows):
        for col in range(cols):
            energy_levels[row][col] += 1


with open('data.txt', 'r') as data_file:
    lines = data_file.read().splitlines()
rows = len(lines)
cols = len(lines[0])

energy_levels = [[int(lines[row][col]) for col in range(cols)] for row in range(rows)]
index_map = [[(row, col) for col in range(cols)] for row in range(rows)]

flash_count = 0

flat_indexes = [item for sublist in index_map for item in sublist]

for step in range(1, MAX_STEPS):
    add_energy()
    check_for_flashes(flat_indexes)
    step_flash_count = count_flashes()
    flash_count += step_flash_count
    if step == 100:
        print('Part 1, flash_count = {}'.format(flash_count))
    if step_flash_count == rows * cols:
        print('Part 2, all_flash_step = {}'.format(step))
        break
