import threading
import time
import random

ACK_LOSS_PROB = 0.2
FRAME_LOSS_PROB = 0.2
TIMEOUT = 3  # seconds

class GoBackNSimulator:
    def __init__(self, total_packets, window_size):
        self.total_packets = total_packets
        self.window_size = window_size
        self.base = 0
        self.next_seq_num = 0
        self.acks_received = [False] * total_packets
        self.lock = threading.Lock()
        self.timer = None

    def start(self):
        log(f"Go-Back-N: Starting transmission of {self.total_packets} packets with window size {self.window_size}")
        while self.base < self.total_packets:
            self.lock.acquire()
            while self.next_seq_num < self.base + self.window_size and self.next_seq_num < self.total_packets:
                self.send_frame(self.next_seq_num)
                self.next_seq_num += 1
            self.lock.release()

            time.sleep(TIMEOUT)
            self.check_timeouts()
        log("Go-Back-N: Transmission complete. All packets acknowledged.")

    def send_frame(self, seq_num):
        if maybe_lose(FRAME_LOSS_PROB):
            log(f"Sender: Sent frame {seq_num}")
            threading.Thread(target=self.receiver, args=(seq_num,)).start()
        else:
            log(f"Sender: Frame {seq_num} lost in transmission")

    def receiver(self, seq_num):
        time.sleep(random.uniform(0.5, 1.5))  # Simulate delay
        if maybe_lose(ACK_LOSS_PROB):
            log(f"Receiver: Received frame {seq_num}, sending ACK {seq_num}")
            threading.Thread(target=self.acknowledge, args=(seq_num,)).start()
        else:
            log(f"Receiver: Frame {seq_num} received, but ACK {seq_num} lost")

    def acknowledge(self, seq_num):
        time.sleep(random.uniform(0.1, 0.3))
        self.lock.acquire()
        if seq_num == self.base:
            log(f"Sender: ACK {seq_num} received, sliding window")
            self.acks_received[seq_num] = True
            while self.base < self.total_packets and self.acks_received[self.base]:
                self.base += 1
        else:
            log(f"Sender: ACK {seq_num} received out of order, ignored")
            self.acks_received[seq_num] = True
        self.lock.release()

    def check_timeouts(self):
        self.lock.acquire()
        if self.base < self.total_packets and not self.acks_received[self.base]:
            log(f"Sender: Timeout for frame {self.base}, resending window [{self.base} - {self.next_seq_num - 1}]")
            self.next_seq_num = self.base
        self.lock.release()


def maybe_lose(prob=0.2):
    return random.random() > prob

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")
 
if __name__ == "__main__":
    packets = 10
    window = 4  
    gobackn = GoBackNSimulator(packets, window)
    gobackn.start()
