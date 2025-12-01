import random
import statistics
import timeit

from sorting_algorithms import insertion_sort, merge_sort


def generate_random_list(n, *, seed: int):
	random.seed(seed)
	return [random.randint(-10_000_000, 10_000_000) for _ in range(n)]


def generate_sorted_list(n):
	return list(range(n))


def generate_reversed_list(n):
	return list(range(n, 0, -1))


def generate_nearly_sorted_list(n, *, fraction_out_of_place: float, seed: int):
	arr = list(range(n))
	num_swaps = max(1, int(n * fraction_out_of_place / 2))
	random.seed(seed)
	for _ in range(num_swaps):
		i = random.randrange(n)
		j = random.randrange(n)
		arr[i], arr[j] = arr[j], arr[i]
	return arr


def benchmark_once(algo, data):
	name, func = algo
	timer = timeit.Timer(lambda: func(data))
	# A single timing run to use inside repeats
	return timer.timeit(number=1)


def benchmark_algo_on_dataset(algo, data, repeats: int):
	times = [benchmark_once(algo, data) for _ in range(repeats)]
	return statistics.median(times)


def allowed_for_insertion(dataset, n):
	# if dataset == "reversed":
	# 	return n <= 5000
	# if dataset == "random":
	# 	return n <= 5000

	return n <= 50000


def main():
	repeats = 5
	datasets = {}

	random_sizes = [1_000, 5_000, 10_000, 50_000, 100_000]
	sorted_sizes = [1_000, 5_000, 10_000, 50_000, 100_000]
	reversed_sizes = [1_000, 5_000, 10_000, 50_000]
	nearly_sorted_sizes = [1_000, 5_000, 10_000, 50_000, 100_000]

	datasets["random"] = [(n, generate_random_list(n, seed=42)) for n in random_sizes]
	datasets["sorted"] = [(n, generate_sorted_list(n)) for n in sorted_sizes]
	datasets["reversed"] = [(n, generate_reversed_list(n)) for n in reversed_sizes]
	datasets["nearly_sorted"] = [
		(n, generate_nearly_sorted_list(n, fraction_out_of_place=0.05, seed=99)) for n in nearly_sorted_sizes
	]

	algorithms = [
		("insertion", insertion_sort),
		("merge", merge_sort),
		("timsort", sorted),  
	]
	results = []

	for dataset_name, items in datasets.items():
		print(f"\nDataset: {dataset_name}")
		print(f"{'n':^10}|{'algo':^10}|{'median_time_s':^15}")
		print("-" * 40)

		for n, data in items:
			for algo in algorithms:
				algo_name, _ = algo
				if algo_name == "insertion" and not allowed_for_insertion(dataset_name, n):
					continue
				median_time = benchmark_algo_on_dataset(algo, data, repeats=repeats)
				results.append(
					{
						"dataset": dataset_name,
						"n": n,
						"algo": algo_name,
						"median_s": median_time,
					}
				)
				print(f"{n:^10}|{algo_name:^10}|{median_time:>15.6f}")
		print("-" * 40) 
	print("\nRelative speed vs Timsort (algo_time / timsort_time):")
	print(f"{'dataset':^20}|{'n':^10}|{'algo':^10}|{'ratio':^15}")
	index = {}
	for r in results:
		index[(r["dataset"], r["n"], r["algo"])] = r["median_s"]
	for r in results:
		if r["algo"] == "timsort":
			continue
		key_t = (r["dataset"], r["n"], "timsort")
		if key_t in index:
			ratio = index[(r["dataset"], r["n"], r["algo"])] / index[key_t]
			print(f"{r['dataset']:^20}|{r['n']:^10}|{r['algo']:^10}|{ratio:>15.2f}")


if __name__ == "__main__":
	main()


