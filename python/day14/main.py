from collections import defaultdict

MAX_STEPS = 40


def get_solution() -> int:
    most_common_element = None
    least_common_element = None
    for element, count in element_count_map.items():
        if not most_common_element or count > element_count_map[most_common_element]:
            most_common_element = element
        if not least_common_element or count < element_count_map[least_common_element]:
            least_common_element = element
    return element_count_map[most_common_element] - element_count_map[least_common_element]


template = None
rules = []
with open('data.txt', 'r') as data_file:
    lines = data_file.read().splitlines()
for line in lines:
    if ' -> ' in line:
        pair, value = line.strip().split(' -> ')
        rules.append((pair, value))
    elif line.strip():
        template = line.strip()

element_count_map = defaultdict(lambda: 0)
pair_count_map = defaultdict(lambda: 0)
added_pair_count_map = defaultdict(lambda: 0)
added_elements_count_map = defaultdict(lambda: 0)
removed_pair_counts = set()

for i in range(len(template)):
    element_count_map[template[i]] += 1

for i in range(len(template) - 1):
    pair_count_map[template[i] + template[i + 1]] += 1

for step in range(MAX_STEPS):
    added_pair_count_map.clear()
    added_elements_count_map.clear()
    removed_pair_counts.clear()
    for rule in rules:
        pre_rule_pair_count = pair_count_map[rule[0]]
        added_elements_count_map[rule[1]] += pre_rule_pair_count
        added_pair_count_map[rule[0][0] + rule[1]] += pre_rule_pair_count
        added_pair_count_map[rule[1] + rule[0][1]] += pre_rule_pair_count
        removed_pair_counts.add(rule[0])
    for pair in removed_pair_counts:
        del pair_count_map[pair]
    for pair, count in added_pair_count_map.items():
        pair_count_map[pair] += count
    for element, count in added_elements_count_map.items():
        element_count_map[element] += count
    if step == 9:
        print('Part 1, most common - least common after {} steps = {}'.format(step + 1, get_solution()))
print('Part 2, most common - least common after {} steps = {}'.format(MAX_STEPS, get_solution()))
