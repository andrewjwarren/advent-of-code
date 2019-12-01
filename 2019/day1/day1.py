#!/usr/bin/env python3

def calculate_fuel(mass):
    fuel = (mass // 3) - 2
    if fuel <= 0:
        fuel = 0
    return fuel

def total_fuel(mass):
    fuel_needed = 0
    while mass > 0:
        mass = calculate_fuel(mass)
        fuel_needed += mass
    return fuel_needed


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.readlines()
        total = 0
        print(sum([total_fuel(int(mass)) for mass in data]))