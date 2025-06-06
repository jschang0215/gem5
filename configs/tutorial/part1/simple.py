import m5
from m5.objects import *

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

# membus
system.membus = SystemXBar()

# port
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
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
binary = "tests/test-progs/hello/bin/x86/linux/hello"
system.workload = SEWorkload.init_compatible(binary)
process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

# instantiate
root = Root(full_system=False, system=system)
m5.instantiate()

print("Simulation begin")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
