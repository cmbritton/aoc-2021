increase_count = 0
prev_value = None

with open('depth_values.data', 'r') as data_file:
    while True:
        line = data_file.readline()
        if not line:
            break
        value = int(line)
        if prev_value is not None:
            if prev_value < value:
                increase_count += 1
        prev_value = value
print("increase_count: {}".format(increase_count))
