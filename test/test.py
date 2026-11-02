# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # 50MHz clock
    clock = Clock(dut.clk, 20, unit="ns")
    clock.start()

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # the first scanline on the first frame will have some uninitialized data
    # (since necessary regs for rendering are computed during the hsync of the
    # previous scanline); skip it
    await ClockCycles(dut.clk, 1526)

    # hsync and vsync should be de-asserted (high)
    assert dut.uo_out.value[7] == 1
    assert dut.uo_out.value[3] == 1

    # hsync should go low after the front porch
    await ClockCycles(dut.clk, 1220+32)
    assert dut.uo_out.value[7] == 0

    # and high again
    await ClockCycles(dut.clk, 185)
    assert dut.uo_out.value[7] == 1
