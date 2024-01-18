def calculate_and_print_metrics(test_heading, results, total_elapsed_time):
    # prices are for gpt-35-turbo, west-europe
    price_completion_tokens = 0.002 / 1000
    price_prompt_tokens = 0.0015 / 1000

    total_completion_tokens = sum(element["completion_tokens"] for element in results)
    total_prompt_tokens = sum(element["prompt_tokens"] for element in results)

    print(test_heading)
    print(f"\tAverage Time (seconds): { float(total_elapsed_time) / len(results)}")
    print(f"\tTotal token: { total_completion_tokens + total_prompt_tokens }")
    print(f"\tAverage token: { float(total_completion_tokens + total_prompt_tokens) / len(results) }")
    print(f"\tEstimated cost: { total_completion_tokens * price_completion_tokens + total_prompt_tokens * price_prompt_tokens }")