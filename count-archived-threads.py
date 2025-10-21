from pychan import FourChan, LogLevel, PychanLogger

# Initialize pychan
logger = PychanLogger(LogLevel.INFO)
fourchan = FourChan(logger=logger, raise_http_exceptions=False)

board = "pol"

print(f"Counting total archived threads on /{board}/...")

try:
    thread_count = 0
    for thread in fourchan.get_archived_threads(board):
        thread_count += 1
        if thread_count % 100 == 0:  # Progress indicator
            print(f"Counted {thread_count} threads so far...")
    
    print(f"\n✅ Total archived threads available on /{board}/: {thread_count}")
    
except Exception as e:
    print(f"Error: {e}")
    print("Note: Some boards (like /b/) don't have archives.")