import sys, time

def run():
    sleepsec=int(sys.argv[1])
    print(f"blocking for {sleepsec} seconds...", end=' ', flush=True)
    time.sleep(sleepsec)
    print("done", flush=True)

if __name__ == "__main__":
    run()

