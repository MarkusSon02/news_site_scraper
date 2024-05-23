from dotenv import load_dotenv
from components.functions import worker
import os
import threading
import queue
import time
import shutil

load_dotenv()

if __name__ == "__main__":
    # Make a set to store URLs so that URLs that has already been processed doesn't get put back in the queue
    start_time = time.time()

    # Check if the folder exists
    if os.path.exists(os.getenv('RESULTS_FOLDER')):
        # If it exists, delete it and its contents
        shutil.rmtree(os.getenv('RESULTS_FOLDER'))

    # Create an empty results folder
    os.makedirs(os.getenv('RESULTS_FOLDER'))

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    ]
    
    URLs = {os.getenv('URL')}
    threads = []
    num_threads = 6

    url_queue = queue.Queue()

    # Enqueue URLs
    for url in URLs:
        url_queue.put((url, 0))

    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(url_queue, URLs, user_agents, 5))
        thread.start()
        threads.append(thread)

    url_queue.join()

    for thread in threads:
        thread.join()

    end_time = time.time()
    running_time = end_time - start_time
    print(running_time)
