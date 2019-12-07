package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

// type Planet interface {
// 	distance()
// 	indirectOrbits()
// 	directOrbit()
// }

type planet struct {
	name     string
	orbits   *planet
	children []*planet
}

func (p *planet) distance(name string) int {
	planets := p.indirectOrbits()
	for i, planet := range planets {
		if strings.EqualFold(planet.name, name) {
			return i
		}
		i++
	}
	return -1
}

func (p *planet) indirectOrbits() []*planet {
	iPlanets := make([]*planet, 0, 2)
	planet := p.orbits
	for {
		if planet == nil {
			break
		}
		iPlanets = append(iPlanets, planet)
		planet = planet.orbits
	}
	return iPlanets
}

func (p *planet) directOrbit() *planet {
	return p.orbits
}

func new(name string) *planet {
	return &planet{
		name: name,
	}
}

func setup() (map[string]*planet, error) {
	data, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	planets := make(map[string]*planet)

	for _, orbit := range strings.Split(string(data), "\n") {
		names := strings.Split(orbit, ")")
		for _, name := range names {
			if _, ok := planets[name]; !ok {
				p := new(name)
				planets[name] = p
			}
		}
		p1 := planets[names[0]]
		p2 := planets[names[1]]
		p2.orbits = p1
	}

	return planets, nil
}

func findIntersection(p1, p2 *planet) *planet {
	indirects := p2.indirectOrbits()
	for _, a := range p1.indirectOrbits() {
		for _, b := range indirects {
			if a.name == b.name {
				return a
			}
		}
	}
	return nil
}

func main() {
	p, _ := setup()
	total := 0
	for _, planet := range p {
		total += len(planet.indirectOrbits())
	}
	fmt.Println(total)
	y := p["YOU"]
	s := p["SAN"]
	i := findIntersection(y, s)
	fmt.Println(y.distance(i.name) + s.distance(i.name))
}
