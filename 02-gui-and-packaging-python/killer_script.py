import random
from time import sleep


def get_result(image_path):
    # Simulate opening and processing the image file
    sleep(1)

    return {
        "filename": image_path,
        "q1": random.choice(range(1, 6)),
        "q2": random.choice(range(1, 6)),
        "q3": random.choice(range(1, 6)),
        "q4": random.choice(range(1, 6)),
        "q5": random.choice(range(1, 6)),
    }
