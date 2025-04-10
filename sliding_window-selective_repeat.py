import threading
import time
import random
import sys
import itertools

ACK_LOSS_PROB = 0.2
FRAME_LOSS_PROB = 0.2
TIMEOUT = 3  # seconds

class SelectiveRepeatSimulator:
    def __init__(self, total_packets, window_size):
        self.total_packets = total_packets
        self.window_size = window_size
        self.base = 0
        self.sent_packets = [False] * total_packets
        self.acks_received = [False] * total_packets
        self.timers = [None] * total_packets
        self.receiver_buffer = [None] * total_packets
        self.lock = threading.Lock()

    def start(self):
        log(f"Selective Repeat: Transmitting {self.total_packets} packets with window size {self.window_size}")
        while not all(self.acks_received):
            self.lock.acquire()
            for i in range(self.base, min(self.base + self.window_size, self.total_packets)):
                if not self.sent_packets[i]:
                    self.send_frame(i)
                    self.sent_packets[i] = True
                    self.set_timer(i)
            self.display_progress()
            self.lock.release()
            time.sleep(0.5)

        self.display_progress()
        log("All packets acknowledged!")
        log(f"Receiver final buffer (sorted): {[pkt for pkt in sorted(p for p in self.receiver_buffer if p is not None)]}")

    def send_frame(self, seq_num):
        if maybe_lose(FRAME_LOSS_PROB):
            log(f"Sender: Sent frame {seq_num}")
            threading.Thread(target=self.receiver, args=(seq_num,)).start()
        else:
            log(f"Sender: Frame {seq_num} lost")

    def receiver(self, seq_num):
        time.sleep(random.uniform(0.5, 1.0))
        if maybe_lose(ACK_LOSS_PROB):
            log(f"Receiver: Received frame {seq_num}, sending ACK")
            self.receiver_buffer[seq_num] = seq_num
            threading.Thread(target=self.acknowledge, args=(seq_num,)).start()
        else:
            log(f"Receiver: Received frame {seq_num}, but ACK lost")

    def acknowledge(self, seq_num):
        time.sleep(random.uniform(0.1, 0.3))
        self.lock.acquire()
        self.acks_received[seq_num] = True
        self.sent_packets[seq_num] = True
        self.cancel_timer(seq_num)
        if seq_num == self.base:
            while self.base < self.total_packets and self.acks_received[self.base]:
                self.base += 1
        self.lock.release()
        log(f"Sender: ACK {seq_num} received")

    def set_timer(self, seq_num):
        def timeout_action():
            time.sleep(TIMEOUT)
            self.lock.acquire()
            if not self.acks_received[seq_num]:
                log(f"Sender: Timeout for frame {seq_num}, resending")
                self.send_frame(seq_num)
                self.set_timer(seq_num)
            self.lock.release()
        self.timers[seq_num] = threading.Thread(target=timeout_action)
        self.timers[seq_num].start()

    def cancel_timer(self, seq_num):
        # using threads instead of timers -> nothing to cancel 
        pass

    def display_progress(self):
        bar = ''
        for i in range(self.total_packets):
            if self.acks_received[i]:
                bar += '🟩'
            elif self.sent_packets[i]:
                bar += '🟨'
            else:
                bar += '⬛'
        sys.stdout.write(f"\rProgress: {bar} ")
        sys.stdout.flush()

# Helpers
def maybe_lose(prob=0.2):
    return random.random() > prob

def log(msg):
    print(f"\n[{time.strftime('%H:%M:%S')}] {msg}")

if __name__ == "__main__":
    total_packets = int(input("Number of packages: "))
    window_size = int(input("Window size: "))
    sr = SelectiveRepeatSimulator(total_packets, window_size)
    sr.start()
