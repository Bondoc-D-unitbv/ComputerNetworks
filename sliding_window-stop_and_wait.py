import threading
import time
import random

class Frame:
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data

def maybe_lose(prob=0.2):
    return random.random() > prob

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


def stop_and_wait_sender(packets, timeout=3):
    for i in range(packets):
        ack_received = False
        while not ack_received:
            log(f"Sender: Sending frame {i}")
            receiver_thread = threading.Thread(target=stop_and_wait_receiver, args=(i,))
            receiver_thread.start()
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                time.sleep(0.1)
                if ack_flags.get(i):
                    ack_received = True
                    log(f"Sender: ACK {i} received.")
                    break
            if not ack_received:
                log(f"Sender: Timeout! Resending frame {i}.")

ack_flags = {}

def stop_and_wait_receiver(frame_num):
    time.sleep(random.uniform(0.5, 1.5))  # Simulate processing delay
    if maybe_lose():
        log(f"Receiver: Received frame {frame_num}, sending ACK {frame_num}")
        ack_flags[frame_num] = True
    else:
        log(f"Receiver: Frame {frame_num} lost or ACK lost")

if __name__ == "__main__":
    stop_and_wait_sender(packets=6)

