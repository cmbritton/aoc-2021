class Power(object):
    LENGTH = 12

    def __init__(self):
        self.zeroCount = [0] * Power.LENGTH
        self.oneCount = [0] * Power.LENGTH

    def gamma(self):
        str_value = ""
        for char_value in self.gamma_str():
            str_value += char_value
        return int(str_value, 2)

    def gamma_str(self):
        value = [0] * Power.LENGTH
        for i in range(Power.LENGTH):
            if self.zeroCount[i] > self.oneCount[i]:
                value[i] = '0'
            else:
                value[i] = '1'
        return value

    def epsilon(self):
        str_value = ""
        for char_value in self.gamma_str():
            if char_value == '1':
                str_value += '0'
            else:
                str_value += '1'
        return int(str_value, 2)

    def value(self):
        return self.gamma() * self.epsilon()


class PowerDiagnostics(object):

    def __init__(self):
        self.power = Power()

    def accumulate(self, value):
        for i in range(Power.LENGTH):
            if value[i] == '1':
                self.power.oneCount[i] += 1
            else:
                self.power.zeroCount[i] += 1


def main():
    power_diagnostics = PowerDiagnostics()
    with open('../../data/day03.data', 'r') as data_file:
        line = data_file.readline()
        while line:
            value = line.strip()
            power_diagnostics.accumulate(value=value)
            line = data_file.readline()
    print("gamma: {}".format(power_diagnostics.power.value()))


main()
