from mmu import MMU

class ClockMMU(MMU):
    def __init__(self, frames):
        self.page_table = {}  # Dictionary to map page numbers to frame existence in memory.
        self.page_order = []  # List to track the order of pages in memory (for clock hand).
        self.reference_bits = {}  # Reference bits to track whether a page was recently accessed.
        self.dirty_bits = {}  # Dirty bits to track if a page has been written to (needs to be saved).
        self.debug_mode = False  # Debug mode flag for extra logging.
        self.frames = frames  # Total number of frames (memory slots).
        self.clock_hand = 0  # Position of the clock hand for page replacement.
        self.disk_reads = 0  # Counter for the number of disk reads (loading pages into memory).
        self.disk_writes = 0  # Counter for the number of disk writes (saving modified pages).
        self.page_faults = 0  # Counter for the number of page faults.

    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False

    def read_memory(self, page_number):
        if page_number in self.page_table:
            # Page is in memory; set reference bit to 1 to indicate recent access.
            self.reference_bits[page_number] = 1
        else:
            # Page fault: the page is not in memory.
            self.page_faults += 1
            if len(self.page_table) < self.frames:
                # If there is space in memory, load the page directly.
                self.load_page(page_number, is_write=False)
            else:
                # If memory is full, replace a page using the clock algorithm.
                self.replace_page(page_number, is_write=False)

    def write_memory(self, page_number):
        if page_number in self.page_table:
            # Page is in memory; set reference and dirty bits.
            self.reference_bits[page_number] = 1
            self.dirty_bits[page_number] = True
        else:
            # Page fault: the page is not in memory.
            self.page_faults += 1
            if len(self.page_table) < self.frames:
                # If there is space in memory, load the page and mark it as dirty.
                self.load_page(page_number, is_write=True)
            else:
                # If memory is full, replace a page using the clock algorithm.
                self.replace_page(page_number, is_write=True)

    def load_page(self, page_number, is_write):
        self.page_order.append(page_number)  # Add the page to the order of memory pages.
        self.reference_bits[page_number] = 1  # Set reference bit to 1 (page recently used).
        self.page_table[page_number] = True  # Mark the page as present in memory.
        self.dirty_bits[page_number] = is_write  # Set dirty bit based on whether the page is being written.
        self.disk_reads += 1  # Increment disk reads since the page was loaded into memory.

    def replace_page(self, page_number, is_write):
        while True:
            current_page = self.page_order[self.clock_hand]  # Get the page at the current clock hand position.
            
            if self.reference_bits[current_page] == 0:
                # If the reference bit is 0, the page can be replaced.
                if self.dirty_bits[current_page]:
                    # If the page is dirty, write it to disk before replacing.
                    self.disk_writes += 1

                # Remove the page from memory.
                del self.page_table[current_page]
                del self.reference_bits[current_page]
                del self.dirty_bits[current_page]

                # Replace the current page with the new page.
                self.page_order[self.clock_hand] = page_number
                self.load_page(page_number, is_write)
                
                # Move the clock hand forward.
                self.clock_hand = (self.clock_hand + 1) % self.frames
                break
            else:
                # If the reference bit is 1, give the page a second chance and set the reference bit to 0.
                self.reference_bits[current_page] = 0
                self.clock_hand = (self.clock_hand + 1) % self.frames  # Move the clock hand forward.

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
