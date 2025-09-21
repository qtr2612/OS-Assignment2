from mmu import MMU
import random  # Import the random module

class RandMMU(MMU):
    def __init__(self, frames):
        # TODO: 
        self.frames = []  
        self.frame_capacity = frames  
        self.page_table = {}  
        self.page_faults = 0  
        self.disk_reads = 0  
        self.disk_writes = 0  
        self.debug_mode = False  
        

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        self.debug_mode = True
        

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        self.debug_mode = False

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        if page_number not in self.page_table:
            # Page fault: page not in memory
            self.page_faults += 1
            if self.debug_mode:
                print(f"Page fault: page {page_number} not in memory")
            # Allocate a frame randomly
            frame_index = random.randint(0, self.frame_capacity - 1)
            self.frames.append(frame_index)
            self.page_table[page_number] = frame_index
            self.disk_reads += 1  # Increment disk read count
        else:
            # Page is already in memory
            if self.debug_mode:
                print(f"Page {page_number} is already in memory")
    
    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        if page_number not in self.page_table:
            # Page fault: page not in memory
            self.page_faults += 1
            if self.debug_mode:
                print(f"Page fault: page {page_number} not in memory")
            # Allocate a frame randomly
            frame_index = random.randint(0, self.frame_capacity - 1)
            self.frames.append(frame_index)
            self.page_table[page_number] = frame_index
            self.disk_reads += 1  # Increment disk read count
        else:
            # Page is already in memory
            if self.debug_mode:
                print(f"Page {page_number} is already in memory")
            # Mark the page as dirty
            self.disk_writes += 1  # Increment disk write count
        

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.disk_reads
        

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.page_faults