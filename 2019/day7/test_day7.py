from day7 import (
    parse_opcode, 
    Amplifier
)

import pytest


# @pytest.mark.parametrize("code, output", [
#     (1, (1, [])),
#     (1002, (2, [0, 1]))
# ])
# def test_parse_opcode(code, output):
#     result = parse_opcode(code)
#     assert(result == output)


@pytest.mark.parametrize("code, output", [
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2,3,0,3,99], [2,3,0,6,99]),
    ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
    ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])
])
def test_op1_op2_op99(code, output):
    amp = Amplifier(code)
    amp.run()
    assert(amp.data == output)

@pytest.mark.parametrize("code, inputs, output", [
    ([3,9,7,9,10,9,4,9,99,-1,8], 7, 1),
    ([3,9,7,9,10,9,4,9,99,-1,8], 9, 0),
    ([3,9,8,9,10,9,4,9,99,-1,8], 7, 0),
    ([3,9,8,9,10,9,4,9,99,-1,8], 8, 1),
])
def test_op7_op8(code, inputs, output):
    amp = Amplifier(code, inputs)
    amp.run()
    assert(amp.output == output)


@pytest.mark.parametrize("code, inputs, output", [
    ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0),
    ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1, 1),
    ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0),
    ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1, 1),
])
def test_op5_op6(code, inputs, output):
    amp = Amplifier(code, inputs)
    amp.run()
    assert(amp.output == output)