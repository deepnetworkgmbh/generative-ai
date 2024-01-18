def calculate_metrics(test_name, results, total_elapsed_time):
    # prices are for gpt-35-turbo, west-europe
    price_completion_tokens = 0.002 / 1000
    price_prompt_tokens = 0.0015 / 1000

    total_completion_tokens = sum(element["completion_tokens"] for element in results)
    total_prompt_tokens = sum(element["prompt_tokens"] for element in results)

    results_size = len(results)

    metrics = {
        "test_name": test_name,
        "test_count": results_size,
        "average_tokens": float(total_completion_tokens + total_prompt_tokens) / results_size,
        "average_cost": float(total_completion_tokens * price_completion_tokens + total_prompt_tokens * price_prompt_tokens) / results_size,
        "average_time": float(total_elapsed_time) / results_size
    }
    return metrics
