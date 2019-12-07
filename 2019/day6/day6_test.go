package main

import "testing"

func TestIndirectOrbits(t *testing.T) {
	p, _ := setup()
	total := 0
	for _, planet := range p {
		total += len(planet.indirectOrbits())
	}
	if total != 314702 {
		t.Errorf("%d != 314702", total)
	}
}

func TestDistance(t *testing.T) {
	p, _ := setup()
	y := p["YOU"]
	s := p["SAN"]
	i := findIntersection(y, s)
	dist := y.distance(i.name) + s.distance(i.name)
	if dist != 439 {
		t.Errorf("%d != 439", dist)
	}
}
