#!/usr/bin/env python3


class Planet:

    def __init__(self, name):
        self._orbits = None
        self.children = []
        self.name = name

    @property
    def orbits(self):
        return self._orbits

    @orbits.setter
    def orbits(self, x):
        if self._orbits is not None:
            print('Overwriting {} orbit with {}'.format(self, x))
        self._orbits = x
        x.add_child(self)

    def add_child(self, x):
        self.children.append(x)

    def __len__(self):
        if self._orbits:
            return 1
        return 0

    def indirect_orbits(self):
        planet = self.orbits
        while True:
            if planet is None:
                break
            yield planet
            planet = planet.orbits

    def distance_to(self, planet_name):
        total = 0
        if self.name == planet_name:
            return total
        for planet in self.indirect_orbits():
            if planet.name == planet_name:
                return total
            total += 1
        return -1

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Planet({})'.format(self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name and len(self) == len(other)


def find_intersection(planetA, planetB):
    b = list(planetB.indirect_orbits())
    for a in planetA.indirect_orbits():
        if a in b:
            return a


if __name__ == '__main__':
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
    you = planets['YOU']
    san = planets['SAN']
    intersection = find_intersection(you, san)

    print(you.distance_to(intersection.name) +
          san.distance_to(intersection.name))
