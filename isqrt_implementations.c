#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define squared(x) ((x) * (x))

void test_method(const char *method_name, uint32_t isqrt(uint64_t)) {
	printf("\tTesting %s\n", method_name);
	uint32_t errors = 0;
	int progress = 0;
	clock_t t;
	t = clock();
	for (uint32_t x = 2; x != 0; x++) {
		if (((int64_t)4294967295) * (progress + 1) / 100 == x) {
			progress++;
			printf("\r%3d%%\t", progress);
			fflush(stdout);
		}
		uint64_t x2 = squared((uint64_t)x) - 1;
		uint32_t y = isqrt(x2);
		if (x != y + 1)
			if (errors++ < 3)
				printf("\rERROR: %u -> %lu -> %u\n", x, x2, y);
	}
	t = clock() - t;
	int time_taken = round(((double)t) / CLOCKS_PER_SEC * 1000);
	if (errors) {
		int percents = ((uint64_t)errors) * 100 / 4294967296;
		printf("\rtime=%dms\ttotal number of errors = %u (%d%%)\n", time_taken,
			   errors, percents);
	} else {
		printf("\rtime=%dms\teverything is fine\n", time_taken);
	}
}

uint32_t double_sqrt(uint64_t x) { return sqrt((double)x); }
uint32_t double_sqrt_with_check(uint64_t x) {
	uint64_t root = sqrt((double)x);
	return root * root > x ? root - 1 : root;
}
uint32_t binary_search(uint64_t y) {
	uint64_t x1 = 0;
	uint64_t x2 = 4294967295;
	while (x1 < x2) {
		uint64_t x = (x1 + x2 + 1) / 2;
		uint64_t x_squared = x * x;
		if (x_squared > y)
			x2 = x - 1;
		else
			x1 = x;
	}
	return x1;
}

int main() {
	test_method("float function sqrt()", double_sqrt);
	test_method("float sqrt with check", double_sqrt_with_check);
	test_method("finding square using binary search", binary_search);
}
