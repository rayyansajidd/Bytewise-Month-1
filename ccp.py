import time
from collections import deque

# Constants
PAGE_SIZE = 6000
MAX_VM_COUNT = 5

# Placeholder functions
def retrieve_page_from_disk(virtual_address):
    # Simulate retrieving a page from disk
    return f"Page_for_{virtual_address}"

def remove_page_from_memory(page_to_evict):
    # Simulate removing a page from memory
    pass

# Utility functions for user input
def acquire_positive_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive integer value.")
            else:
                return value
        except ValueError:
            print("Please enter a valid integer.")

# Classes for cloud environment and performance monitoring
class VirtualMachine:
    def __init__(self, id, memory_size):
        self.id = id
        self.memory_size = memory_size

class ResourceMonitor:
    def __init__(self):
        self.page_faults = 0
        self.tlb_hits = 0
        self.total_accesses = 0

    def log_metrics(self, page_fault_occurred, tlb_hit_occurred):
        self.total_accesses += 1
        if page_fault_occurred:
            self.page_faults += 1
        if tlb_hit_occurred:
            self.tlb_hits += 1

    def compute_page_fault_rate(self):
        return self.page_faults / self.total_accesses if self.total_accesses > 0 else 0

    def compute_tlb_hit_rate(self):
        return self.tlb_hits / self.total_accesses if self.total_accesses > 0 else 0

class CloudInfrastructure:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.available_memory = total_memory
        self.virtual_machines = []
        self.monitor = ResourceMonitor()
        self.resource_allocation = {}  # Added for Banker's algorithm

    def allocate_vm_best_fit(self, vm):
        if len(self.virtual_machines) < MAX_VM_COUNT and vm.memory_size <= self.available_memory:
            self.virtual_machines.append(vm)
            self.available_memory -= vm.memory_size
            self.resource_allocation[vm.id] = vm.memory_size  # Added for Banker's algorithm
            return True
        return False

    def compute_memory_usage(self):
        used_memory = sum(vm.memory_size for vm in self.virtual_machines)
        return used_memory / self.total_memory

    def is_safe_state(self):
        # Banker's algorithm implementation
        allocation = self.resource_allocation
        max_demand = {vm.id: vm.memory_size for vm in self.virtual_machines}
        available_resources = self.available_memory
        need = {vm_id: max_demand[vm_id] - allocation[vm_id] for vm_id in allocation}

        while True:
            found_safe_vm = False
            for vm_id in allocation:
                if need[vm_id] <= available_resources:
                    available_resources += allocation[vm_id]
                    del need[vm_id]
                    del allocation[vm_id]
                    found_safe_vm = True
                    break
            if not found_safe_vm:
                break

        return not need  # if need is empty, it's a safe state

# Classes for handling demand paging and TLB management
class TranslationLookasideBuffer:
    def __init__(self, size):
        self.size = size
        self.entries = {}
        self.access_history = deque()

    def resolve_address(self, virtual_address):
        if virtual_address in self.entries:
            self.access_history.remove(virtual_address)
            self.access_history.appendleft(virtual_address)
            return self.entries[virtual_address], True
        return None, False

    def insert_entry(self, virtual_address, page):
        if virtual_address in self.entries:
            self.access_history.remove(virtual_address)
        self.entries[virtual_address] = page
        self.access_history.appendleft(virtual_address)
        if len(self.entries) > self.size:
            self.evict_lru()

    def evict_lru(self):
        lru_address = self.access_history.pop()
        del self.entries[lru_address]

class PageReplacementStrategy:
    def __init__(self, size):
        self.size = size
        self.page_access_history = deque()

    def update_access_history(self, page):
        if page in self.page_access_history:
            self.page_access_history.remove(page)
        self.page_access_history.appendleft(page)
        if len(self.page_access_history) > self.size:
            self.page_access_history.pop()

class PagingHandler:
    def __init__(self, page_table, tlb, page_replacement, monitor):
        self.page_table = page_table
        self.tlb = tlb
        self.page_replacement = page_replacement
        self.monitor = monitor

    def manage_page_fault(self, vm_id, virtual_address):
        page_fault_occurred = False
        page, tlb_hit = self.tlb.resolve_address(virtual_address)
        if not tlb_hit:
            page_fault_occurred = True
            if virtual_address in self.page_table[vm_id]:
                page = self.page_table[vm_id][virtual_address]
            else:
                # Page clustering: Load multiple related pages
                for offset in range(0, PAGE_SIZE, 1000):
                    va = virtual_address + offset
                    page = retrieve_page_from_disk(va)
                    self.page_table[vm_id][va] = page
                    self.tlb.insert_entry(va, page)
                    self.page_replacement.update_access_history(page)
            self.tlb.insert_entry(virtual_address, page)
            self.page_replacement.update_access_history(page)
        self.monitor.log_metrics(page_fault_occurred, tlb_hit)
        return tlb_hit

class PageFaultManager:
    def __init__(self, paging_handler):
        self.paging_handler = paging_handler

    def process_page_fault(self, vm_id, virtual_address):
        self.paging_handler.manage_page_fault(vm_id, virtual_address)

# Main function
def main():
    # Input total memory capacity of the cloud environment
    total_memory = acquire_positive_integer_input("Enter total memory capacity: ")
    while total_memory >= 4000:
        if total_memory > 4000:
            print('The total memory exceeds 4000 MB')
            total_memory = acquire_positive_integer_input("Enter total memory capacity: ")

    # Initialize CloudInfrastructure instance
    cloud_env = CloudInfrastructure(total_memory)

  # Input the number of virtual machines to be created
    num_vms = min(acquire_positive_integer_input("Enter the number of VMs to create (max 10): "), MAX_VM_COUNT)

    # Loop through each VM and allocate resources
    for i in range(1, num_vms + 1):
        print(f"\nSpecify VM {i} parameters:")
        vm_memory = acquire_positive_integer_input("Memory size (in MB): ")
        vm = VirtualMachine(i, vm_memory)
        if cloud_env.allocate_vm_best_fit(vm):
            print(f"VM {i} created and allocated {vm_memory} MB memory.")
        else:
            print(f"Failed to allocate memory for VM {i}. Insufficient memory or max VM count reached.")

    # Initialize other components
    page_table = {i: {} for i in range(1, num_vms + 1)}
    tlb = TranslationLookasideBuffer(size=16)
    page_replacement = PageReplacementStrategy(size=16)
    paging_handler = PagingHandler(page_table, tlb, page_replacement, cloud_env.monitor)
    page_fault_manager = PageFaultManager(paging_handler)

    # Simulate some memory accesses for all VMs
    for vm_id in range(1, num_vms + 1):
        virtual_addresses = [1000, 2000, 3000, 1000, 4000, 5000, 2000, 6000]
        print(f"\nSimulating memory accesses for VM {vm_id}:")
        for va in virtual_addresses:
            page_fault_manager.process_page_fault(vm_id, va)
            time.sleep(0.1)  # Add a delay to simulate the time taken for memory access

    # Check if the system is in a safe state
    safe_state = cloud_env.is_safe_state()
    if safe_state:
        print("\nThe system is in a safe state.")
    else:
        print("\nWarning: The system is in an unsafe state.")

    # Calculate performance metrics
    used_memory = sum(vm.memory_size for vm in cloud_env.virtual_machines)
    memory_utilization = used_memory / total_memory if total_memory > 0 else 0
    page_fault_rate = cloud_env.monitor.compute_page_fault_rate()
    tlb_hit_rate = cloud_env.monitor.compute_tlb_hit_rate()

    # Display performance metrics with visual enhancements
    print("\nPerformance Analysis:")
    print(f"{'Memory Utilization:':<20} {min(memory_utilization * 100, 100):.2f}%")

    # Check if memory utilization exceeds 100%
    if memory_utilization > 1:
        print("Warning: Memory utilization exceeds total available memory.")

    print(f"{'Page Fault Rate:':<20} {page_fault_rate:.4f}")
    print(f"{'TLB Hit Rate:':<20} {tlb_hit_rate:.4f}")

if __name__ == "__main__":
    main()

