"""Top K Frequent Elements — https://leetcode.com/problems/top-k-frequent-elements/

Write-up & approaches: ../../docs/problems/top_k_frequent_elements.md

Canonical reference implementation: the write-up's optimal approach (bucket
sort by frequency), kept next to the harness so authored cases stay
falsifiable. Your own attempt lives in solution.py.

  uv run python top_k_frequent_elements/reference.py   # debug one case (see below)
  uv run pytest top_k_frequent_elements/               # run the test sets
"""


class Solution:
    def topKFrequent(self, nums, k):
        """Return the k most frequent values, bucketed by frequency.

        Every frequency is between 1 and n, so the distinct values drop into
        n frequency buckets and reading the buckets from high to low yields
        the top k without any comparison sorting.

        Time:  O(n): one pass to count, one pass over n+1 buckets.
        Space: O(n): the count map and the bucket list.
        """
        counts = {}
        for num in nums:
            counts[num] = counts.get(num, 0) + 1
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, freq in counts.items():
            buckets[freq].append(num)
        top = []
        for freq in range(len(buckets) - 1, 0, -1):
            for num in buckets[freq]:
                top.append(num)
                if len(top) == k:
                    return top
        return top


if __name__ == "__main__":
    # Debug playground: set a breakpoint in topKFrequent above, then run this
    # file. cases.json is empty (any-order output), so a literal example
    # stands in.
    nums, k = [1, 2, 2, 3, 3, 3], 2
    result = Solution().topKFrequent(nums, k)
    print(f"args = nums={nums}, k={k}")
    print(f"got: {sorted(result)}")
