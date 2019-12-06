from day5 import (
    parse_opcode, 
    read_intcode, 
    opcode_1, 
    opcode_2,
    opcode_3,
    opcode_4,
    opcode_5,
    opcode_6,
    opcode_7,
    opcode_8
)

import pytest


@pytest.mark.parametrize("code, output", [
    (1,(1, [])),
    (1002,(2,[0,1]))
])
def test_parse_opcode(code, output):
    result = parse_opcode(code)
    assert(result == output)

@pytest.mark.parametrize("intcode, output",[
    ([1002,4,3,4,33], [1002,4,3,4,99]), 
    ([1101,100,-1,4,0], [1101,100,-1,4,99]),
    ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])
])
def test_read_intcode(intcode, output):
    result = read_intcode(intcode)
    assert(result == output)


@pytest.mark.parametrize("params, data, output", [
   ([(1,1), (1,20), (1,3)], [1, 1, 1, 1], [1,1,1,21]),
])
def test_opcode_1(params, data, output):
    opcode_1(params, data, 1)
    assert(data == output)

@pytest.mark.parametrize("params, data, output", [
   ([(1,1), (1,20), (1,3)], [1, 1, 1, 1], [1,1,1,20]),
])
def test_opcode_2(params, data, output):
    opcode_2(params, data, 1)
    assert(data == output)

@pytest.mark.parametrize("params, end, output", [
   ([(1,1), (1,20)], 10, 20),
   ([(1,0), (1,20)], 10, 10),
])
def test_opcode_5(params, end, output):
    data = []
    value = opcode_5(params, data, end)
    assert(value == output)

@pytest.mark.parametrize("params, end, output", [
   ([(1,1), (1,20)], 10, 10),
   ([(1,0), (1,20)], 10, 20),
])
def test_opcode_6(params, end, output):
    data = []
    value = opcode_6(params, data, end)
    assert(value == output)

@pytest.mark.parametrize("params, data, output", [
   ([(1,1), (1,20), (1,3)], [7, 10, 20, 9], [7, 10, 20, 1]),
   ([(1,100), (1,20), (1,3)], [7, 10, 20, 9], [7, 10, 20, 0]),
])
def test_opcode_7(params, data, output):
    opcode_7(params, data, None)
    assert(data == output)

@pytest.mark.parametrize("params, data, output", [
   ([(1,1), (1,1), (1,3)], [7, 10, 20, 9], [7, 10, 20, 1]),
   ([(1,1), (1,20), (1,3)], [7, 10, 20, 9], [7, 10, 20, 0]),
])
def test_opcode_8(params, data, output):
    opcode_8(params, data, None)
    assert(data == output)