# argument parser
import argparse

from caches import *

import m5
from m5.objects import *

parser = argparse.ArgumentParser(
    description="A simple system with 2-level cache."
)
parser.add_argument(
    "binary",
    default="",
    nargs="?",
    type=str,
    help="Path to the binary to execute.",
)

options = parser.parse_args()

system = System()

# clock
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# memory
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

# cpu
system.cpu = X86TimingSimpleCPU()
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# L2 bus
system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# L2
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)

# membus
system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

# port
system.cpu.createInterruptController()
# x86-specific port setup
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

# memcon
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR4_2400_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# test process
process = Process()
process.cmd = [options.binary]
system.workload = SEWorkload.init_compatible(options.binary)
system.cpu.workload = process
system.cpu.createThreads()

# instantiate
root = Root(full_system=False, system=system)
m5.instantiate()

print("Simulation begin")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
