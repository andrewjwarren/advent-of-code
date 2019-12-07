from day6 import Planet

import pytest


def test_indirect_orbits(planets):
    total = 0
    for k, v in planets.items():
        if v.orbits is None:
            continue
        total += len(list(v.indirect_orbits()))

    assert(total == 314702)


@pytest.mark.parametrize("src, dest, result", [
    ('YOU', 'YQ1', 279), 
    ('SAN', 'YQ1', 160)
])
def test_distance_to(planets, src, dest, result):
    a = planets[src]
    assert(a.distance_to(dest) == result)


@pytest.fixture
def planets():
    with open('input.txt') as f:
        orbits = f.read().split()
    planets = {}
    for orbit in orbits:
        planetA, planetB = orbit.split(')')
        for planet in [planetA, planetB]:
            try:
                planets[planet]
            except KeyError:
                p = Planet(planet)
                planets[planet] = p
        b = planets[planetB]
        a = planets[planetA]
        b.orbits = a
    return planets