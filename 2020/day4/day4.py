#!/usr/bin/env python
import re

FILENAME = 'input'

with open(FILENAME) as f:
    data = f.read().split('\n\n')

required_fields = [ 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

def validate_passport(pport):
    fields = pport.split()
    if len(fields) < len(required_fields):
        return False
    fields = dict([f.split(':') for f in fields])
    for f in required_fields:
        if f not in fields:
            return False
        elif not validation[f](fields[f]):
            print(f, fields[f])
            return False
    return True

def between(a, value, b):
    return a <= int(value) <= b

def byr(value):
    return between(1920, value, 2002)

def iyr(value):
    return between(2010, value, 2020)

def eyr(value):
    return between(2020, value, 2030)

def hgt(value):
    res = re.search(r'^\d+(cm|in)', value)
    if not res:
        return False
    x = int(value[:-2])
    t = value[-2:]
    if t == 'in':
        return between(59, x, 76)
    elif t == 'cm':
        return between(150, x, 193)
    return False

def hcl(value):
    res = re.search(r'#[a-f0-9]{6}', value)
    if res:
        return True
    return False
            
def ecl(value):
    if value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl','oth']:
        return True
    return False

def pid(value):
    if len(value) != 9:
        return False
    try:
        int(value)
        return True
    except:
        return False

validation = {
    'byr': byr,
    'iyr': iyr,
    'eyr': eyr,
    'hgt': hgt,
    'hcl': hcl,
    'ecl': ecl,
    'pid': pid
}

total = 0
for pport in data:
    if validate_passport(pport):
        total += 1
print(total)
