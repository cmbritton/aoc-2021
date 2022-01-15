import numpy as np
import timeit


with open('data.txt', 'r') as data_file:
    input_line = data_file.readline()
    orig_positions = np.array(input_line.strip().split(',')).astype(int)
    min_position = np.amin(orig_positions)
    max_position = np.amax(orig_positions)
    optimum_position = optimum_fuel_used = position_under_test = -1
    fuel_used = 0


def constant_fuel_rate(x):
    global fuel_used
    fuel_used += abs(position_under_test - x)


def decaying_fuel_rate(x):
    global fuel_used
    fuel_used += sum(range(1, abs(position_under_test - x) + 1))


def run(fuel_function):
    global position_under_test, fuel_used, optimum_position, optimum_fuel_used
    optimum_position = -1
    optimum_fuel_used = -1
    for position in range(min_position, max_position + 1):
        position_under_test = position
        fuel_used = 0
        positions = orig_positions.copy()
        np.frompyfunc(fuel_function, 1, 0)(positions)
        if fuel_used < optimum_fuel_used or optimum_fuel_used < 0:
            optimum_fuel_used = fuel_used
            optimum_position = position


def main():
    for fuel_function in [constant_fuel_rate, decaying_fuel_rate]:
        start_time = timeit.default_timer()
        run(fuel_function)
        end_time = timeit.default_timer()
        print('\n{}\n\texecution time: {} seconds\n\tbest position:  {}\n\tfuel used:      {}'.format(
            fuel_function.__name__, end_time - start_time, optimum_position, optimum_fuel_used))


main()
