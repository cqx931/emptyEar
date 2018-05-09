#!/usr/bin/env python3
from threading import Thread
import time

def drive_bus():
    time.sleep(1)
    print("Igor: I'm Igor and I'm driving to... Moskow!")
    time.sleep(9)
    print("Igor: Yei, Moskow!")

def build_house():
    print("Peter: Let's start building a large house...")
    time.sleep(10.1)
    print("Peter: Urks, we have no tools :-(")

threads = [Thread(target=drive_bus), Thread(target=build_house)]

for t in threads:
    t.start()

for t in threads:
    t.join()
