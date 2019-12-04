#!/usr/bin/env python3

from collections import Counter

def codes(start, end):
    for x in range(start, end):
        yield str(x)

def acceptable(code):
    has_double = False
    for i, v in enumerate(code):
        if i == len(code) - 1:
            continue
        elif int(v) > int(code[i+1]):
            return False
        elif int(v) == int(code[i+1]):
            has_double = True
    if has_double:
        return double_checker(code)
    return False

def double_checker(code):
    cnt = Counter()
    for x in code:
        cnt[x] += 1
    has_double = False
    has_greater = False
    for c in cnt.most_common():
        key, value = c
        if value == 2:
            has_double = True
            break
    return has_double

#555799 pass
#699999 fail

if __name__ == '__main__': 
    total = 0
    # Range 231832-767346
    for code in codes(231832, 767346):
        if acceptable(code):
            total += 1
    print(total)