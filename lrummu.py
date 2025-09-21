from mmu import MMU
from collections import OrderedDict

class LruMMU(MMU):
    def __init__(self, frames):
        super().__init__()
        self.frames = OrderedDict()  # Holds the pages in memory
        self.max_frames = frames
        self.total_disk_reads = 0
        self.total_disk_writes = 0
        self.total_page_faults = 0
        self.debug_mode = False

    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False

    def read_memory(self, page_number):
        if page_number in self.frames:
            self.frames.move_to_end(page_number)  # Page is already in memory, mark as recently used
            if self.debug_mode:
                print(f"Read hit: page {page_number}")
        else:
            self.total_page_faults += 1
            self.total_disk_reads += 1
            if len(self.frames) >= self.max_frames:
                evicted_page, dirty = self.frames.popitem(last=False)  # Evict LRU page
                if dirty:  # Write back to disk if the page was dirty
                    self.total_disk_writes += 1
                if self.debug_mode:
                    print(f"Evicting page {evicted_page}")
            self.frames[page_number] = False  # Load new page, not dirty
            if self.debug_mode:
                print(f"Read miss: page {page_number}")

    def write_memory(self, page_number):
        if page_number in self.frames:
            self.frames.move_to_end(page_number)  # Page is already in memory, mark as recently used
            self.frames[page_number] = True  # Mark the page as dirty
            if self.debug_mode:
                print(f"Write hit: page {page_number}")
        else:
            self.total_page_faults += 1
            self.total_disk_reads += 1
            if len(self.frames) >= self.max_frames:
                evicted_page, dirty = self.frames.popitem(last=False)  # Evict LRU page
                if dirty:  # Write back to disk if the page was dirty
                    self.total_disk_writes += 1
                if self.debug_mode:
                    print(f"Evicting page {evicted_page}")
            self.frames[page_number] = True  # Load new page, mark as dirty
            if self.debug_mode:
                print(f"Write miss: page {page_number}")

    def get_total_disk_reads(self):
        return self.total_disk_reads

    def get_total_disk_writes(self):
        return self.total_disk_writes

    def get_total_page_faults(self):
        return self.total_page_faults