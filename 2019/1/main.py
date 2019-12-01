import util

def required_fuel(mass, fuel=0):
    res = mass//3 - 2
    if res > 0:
        return required_fuel(res, fuel + res)
    return fuel

def main():
    masses = util.load_data(int)

    res_part1 = sum([m//3 + 2 for m in masses])
    print(f'Part 1 : {res_part1}')
    res_part2 = sum([required_fuel(m) for m in masses])
    print(f'Part 2 : {res_part2}')


if __name__ == '__main__':
    main()
