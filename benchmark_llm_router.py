import time
import os
import sys

# Ensure the root directory is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.llm_router import LLMRouter

def run_benchmark(iterations=100000):
    router = LLMRouter("config/models.yaml")

    # Pre-warm
    router._get_model_config("gpt-4o")

    start_time = time.perf_counter()
    for _ in range(iterations):
        router._get_model_config("gpt-4o")
    end_time = time.perf_counter()

    config_time = end_time - start_time
    print(f"_get_model_config({iterations} iterations): {config_time:.6f} seconds")

    start_time = time.perf_counter()
    for _ in range(iterations):
        router._get_models_for_task("topic_generation", "free")
    end_time = time.perf_counter()

    task_time = end_time - start_time
    print(f"_get_models_for_task({iterations} iterations): {task_time:.6f} seconds")

if __name__ == "__main__":
    run_benchmark()
