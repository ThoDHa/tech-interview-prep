# Tech Interview Prep

This repository is a structured study guide for algorithmic problem solving built on three curated problem banks: the [Grind 75](https://www.techinterviewhandbook.org/grind75) list of LeetCode questions from the [Tech Interview Handbook](https://www.techinterviewhandbook.org/) team, the [NeetCode 150](https://neetcode.io/practice/practice/neetcode150) track from the [NeetCode](https://neetcode.io/) team, and an [Amazon OA](docs/problems/amazon_oa/index.md) bank collected from the [Tech-OA-Interview-Questions](https://github.com/perixtar/Tech-OA-Interview-Questions) repository. All credit for the curated problem lists goes to them for their excellent work in creating these focused interview preparation resources.

**Read it as a website:** the full guide, including complete solution write-ups for every Grind 75 problem (write-ups for the newer banks are in progress), is published at [thodha.github.io/tech-interview-prep](https://thodha.github.io/tech-interview-prep/).

## The three problem banks

- **Grind 75** is the core track: the canonical 75 problems in study order (plus two bonus problems), listed in the table below and mirrored on the site's home page.
- **NeetCode 150** extends the bank to 150 problems in NeetCode's section order; 59 of them overlap with Grind 75 and share their write-ups. Its table is generated into a marker-bounded section of the home page.
- **Amazon OA** is a growing bank of Amazon-tagged online-assessment questions with its own [index page](docs/problems/amazon_oa/index.md), most recently updated first, and practice stubs under `practice/amazon_oa/`.

Every problem, regardless of track, has the same core page structure (statement and examples, with constraints where available) and a matching practice folder under `practice/` with stubs and tests; Grind 75 pages also link the **Pattern** guide behind the technique.

## How this repository is organized

- The `main` branch is the study environment: problem statements, pattern guides, foundations, interview prep planning, system design material, and the `practice/` workspace with unsolved stubs. Solution write-ups are deliberately absent here so you can attempt problems without spoilers.
- The `solutions` branch adds the full multi-approach solution write-ups to every Grind 75 problem page; the NeetCode 150 and Amazon OA write-ups land there later. The published site is built from it, so read solutions on the website (or that branch) when you are ready to compare answers.
- The `scripts/` directory holds the generators that maintain the generated tracks: `generate_neetcode150_scaffolds.py` rebuilds the NeetCode 150 statement pages, practice stubs, and the home-page table from `scripts/neetcode150_manifest.json`, and `generate_amazon_oa_scaffolds.py` does the same for the Amazon OA bank from `scripts/amazon_oa_manifest.json`. Both are manifest-driven: the generated files are not edited by hand, and changes are validated with `cd practice && uv run pytest ../scripts/`.

## First time here?

New to algorithms or interview prep? Start with the [Foundations](docs/foundations/index.md) section before the problems. It teaches the prerequisites the problem pages assume, all from zero:

1. [Big-O Notation](docs/foundations/big_o.md): what `O(n)` and `O(log n)` mean and when each is too slow.
2. [Recursion and the Call Stack](docs/foundations/recursion.md): how a function that calls itself actually works.
3. [Data Structures in Pictures](docs/foundations/data_structures.md): arrays, hash maps, stacks, queues, trees, graphs, and heaps.
4. [How to Approach a Problem](docs/foundations/how_to_approach.md): a repeatable method from problem statement to working solution.
5. [Glossary](docs/foundations/glossary.md): the jargon the guides lean on, defined in plain language.

Then work the problems in order, reading each one's linked **Pattern** guide for the *why* behind the technique. For the plan around the problems, how to budget your time, and what the non-coding rounds require, see the [Interview Prep](docs/interview_prep/index.md) section.

## Grind 75 Problem List

The canonical 75 problems in study order (for real progress tracking, use the [practice progress tracker](#practice-workspace) instead of editing this table):

| Status | # | Problem | Difficulty | Category | Time |
|--------|---|---------|------------|----------|------|
| 󰄰 | [1](https://leetcode.com/problems/two-sum/) | [Two Sum](docs/problems/two_sum.md) | Easy | Array, Hash Table | 15 minutes |
| 󰄰 | [2](https://leetcode.com/problems/valid-parentheses/) | [Valid Parentheses](docs/problems/valid_parentheses.md) | Easy | Stack, String | 20 minutes |
| 󰄰 | [3](https://leetcode.com/problems/merge-two-sorted-lists/) | [Merge Two Sorted Lists](docs/problems/merge_two_sorted_lists.md) | Easy | Linked List | 20 minutes |
| 󰄰 | [4](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | [Best Time to Buy and Sell Stock](docs/problems/best_time_to_buy_and_sell_stock.md) | Easy | Array | 20 minutes |
| 󰄰 | [5](https://leetcode.com/problems/valid-palindrome/) | [Valid Palindrome](docs/problems/valid_palindrome.md) | Easy | String | 15 minutes |
| 󰄰 | [6](https://leetcode.com/problems/invert-binary-tree/) | [Invert Binary Tree](docs/problems/invert_binary_tree.md) | Easy | Tree | 15 minutes |
| 󰄰 | [7](https://leetcode.com/problems/valid-anagram/) | [Valid Anagram](docs/problems/valid_anagram.md) | Easy | String | 15 minutes |
| 󰄰 | [8](https://leetcode.com/problems/binary-search/) | [Binary Search](docs/problems/binary_search.md) | Easy | Binary Search | 15 minutes |
| 󰄰 | [9](https://leetcode.com/problems/flood-fill/) | [Flood Fill](docs/problems/flood_fill.md) | Easy | Graph, DFS | 20 minutes |
| 󰄰 | [10](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | [Lowest Common Ancestor of a BST](docs/problems/lowest_common_ancestor_of_a_binary_search_tree.md) | Medium | Tree | 20 minutes |
| 󰄰 | [11](https://leetcode.com/problems/balanced-binary-tree/) | [Balanced Binary Tree](docs/problems/balanced_binary_tree.md) | Easy | Tree | 15 minutes |
| 󰄰 | [12](https://leetcode.com/problems/linked-list-cycle/) | [Linked List Cycle](docs/problems/linked_list_cycle.md) | Easy | Linked List | 20 minutes |
| 󰄰 | [13](https://leetcode.com/problems/implement-queue-using-stacks/) | [Implement Queue using Stacks](docs/problems/implement_queue_using_stacks.md) | Easy | Stack | 20 minutes |
| 󰄰 | [14](https://leetcode.com/problems/first-bad-version/) | [First Bad Version](docs/problems/first_bad_version.md) | Easy | Binary Search | 20 minutes |
| 󰄰 | [15](https://leetcode.com/problems/ransom-note/) | [Ransom Note](docs/problems/ransom_note.md) | Easy | Hash Table | 15 minutes |
| 󰄰 | [16](https://leetcode.com/problems/climbing-stairs/) | [Climbing Stairs](docs/problems/climbing_stairs.md) | Easy | Dynamic Programming | 20 minutes |
| 󰄰 | [17](https://leetcode.com/problems/longest-palindrome/) | [Longest Palindrome](docs/problems/longest_palindrome.md) | Easy | String | 20 minutes |
| 󰄰 | [18](https://leetcode.com/problems/reverse-linked-list/) | [Reverse Linked List](docs/problems/reverse_linked_list.md) | Easy | Linked List | 20 minutes |
| 󰄰 | [19](https://leetcode.com/problems/majority-element/) | [Majority Element](docs/problems/majority_element.md) | Easy | Array | 20 minutes |
| 󰄰 | [20](https://leetcode.com/problems/add-binary/) | [Add Binary](docs/problems/add_binary.md) | Easy | String | 15 minutes |
| 󰄰 | [21](https://leetcode.com/problems/diameter-of-binary-tree/) | [Diameter of Binary Tree](docs/problems/diameter_of_binary_tree.md) | Easy | Tree | 30 minutes |
| 󰄰 | [22](https://leetcode.com/problems/middle-of-the-linked-list/) | [Middle of the Linked List](docs/problems/middle_of_the_linked_list.md) | Easy | Linked List | 20 minutes |
| 󰄰 | [23](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | [Maximum Depth of Binary Tree](docs/problems/maximum_depth_of_binary_tree.md) | Easy | Tree | 15 minutes |
| 󰄰 | [24](https://leetcode.com/problems/contains-duplicate/) | [Contains Duplicate](docs/problems/contains_duplicate.md) | Easy | Array | 15 minutes |
| 󰄰 | [25](https://leetcode.com/problems/maximum-subarray/) | [Maximum Subarray](docs/problems/maximum_subarray.md) | Medium| Array, Dynamic Programming | 20 minutes |
| 󰄰 | [26](https://leetcode.com/problems/insert-interval/) | [Insert Interval](docs/problems/insert_interval.md) | Medium | Array | 25 minutes |
| 󰄰 | [27](https://leetcode.com/problems/01-matrix/) | [01 Matrix](docs/problems/01_matrix.md) | Medium | BFS | 30 minutes |
| 󰄰 | [28](https://leetcode.com/problems/k-closest-points-to-origin/) | [K Closest Points to Origin](docs/problems/k_closest_points_to_origin.md) | Medium | Heap | 30 minutes |
| 󰄰 | [29](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | [Longest Substring Without Repeating Characters](docs/problems/longest_substring_without_repeating_characters.md) | Medium | String | 30 minutes |
| 󰄰 | [30](https://leetcode.com/problems/3sum/) | [3Sum](docs/problems/3sum.md) | Medium | Array | 30 minutes |
| 󰄰 | [31](https://leetcode.com/problems/binary-tree-level-order-traversal/) | [Binary Tree Level Order Traversal](docs/problems/binary_tree_level_order_traversal.md) | Medium | Tree | 20 minutes |
| 󰄰 | [32](https://leetcode.com/problems/clone-graph/) | [Clone Graph](docs/problems/clone_graph.md) | Medium | Graph | 25 minutes |
| 󰄰 | [33](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | [Evaluate Reverse Polish Notation](docs/problems/evaluate_reverse_polish_notation.md) | Medium | Stack | 30 minutes |
| 󰄰 | [34](https://leetcode.com/problems/course-schedule/) | [Course Schedule](docs/problems/course_schedule.md) | Medium | Graph | 30 minutes |
| 󰄰 | [35](https://leetcode.com/problems/implement-trie-prefix-tree/) | [Implement Trie (Prefix Tree)](docs/problems/implement_trie_prefix_tree.md) | Medium | Trie | 35 minutes |
| 󰄰 | [36](https://leetcode.com/problems/coin-change/) | [Coin Change](docs/problems/coin_change.md) | Medium | Dynamic Programming | 25 minutes |
| 󰄰 | [37](https://leetcode.com/problems/product-of-array-except-self/) | [Product of Array Except Self](docs/problems/product_of_array_except_self.md) | Medium | Array | 30 minutes |
| 󰄰 | [38](https://leetcode.com/problems/min-stack/) | [Minimum Stack](docs/problems/min_stack.md) | Medium | Stack | 20 minutes |
| 󰄰 | [39](https://leetcode.com/problems/validate-binary-search-tree/) | [Validate Binary Search Tree](docs/problems/validate_binary_search_tree.md) | Medium | Tree | 20 minutes |
| 󰄰 | [40](https://leetcode.com/problems/number-of-islands/) | [Number of Islands](docs/problems/number_of_islands.md) | Medium | Graph | 25 minutes |
| 󰄰 | [41](https://leetcode.com/problems/rotting-oranges/) | [Rotting Oranges](docs/problems/rotting_oranges.md) | Medium | BFS | 30 minutes |
| 󰄰 | [42](https://leetcode.com/problems/search-in-rotated-sorted-array/) | [Search in Rotated Sorted Array](docs/problems/search_in_rotated_sorted_array.md) | Medium | Binary Search | 30 minutes |
| 󰄰 | [43](https://leetcode.com/problems/combination-sum/) | [Combination Sum](docs/problems/combination_sum.md) | Medium | Backtracking | 30 minutes |
| 󰄰 | [44](https://leetcode.com/problems/permutations/) | [Permutations](docs/problems/permutations.md) | Medium | Backtracking | 30 minutes |
| 󰄰 | [45](https://leetcode.com/problems/merge-intervals/) | [Merge Intervals](docs/problems/merge_intervals.md) | Medium | Sorting | 30 minutes |
| 󰄰 | [46](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | [Lowest Common Ancestor of a Binary Tree](docs/problems/lowest_common_ancestor_of_a_binary_tree.md) | Medium | Tree | 25 minutes |
| 󰄰 | [47](https://leetcode.com/problems/time-based-key-value-store/) | [Time Based Key-Value Store](docs/problems/time_based_key_value_store.md) | Medium | Binary Search | 35 minutes |
| 󰄰 | [48](https://leetcode.com/problems/accounts-merge/) | [Accounts Merge](docs/problems/accounts_merge.md) | Medium | Graph | 30 minutes |
| 󰄰 | [49](https://leetcode.com/problems/sort-colors/) | [Sort Colors](docs/problems/sort_colors.md) | Medium | Array | 25 minutes |
| 󰄰 | [50](https://leetcode.com/problems/word-break/) | [Word Break](docs/problems/word_break.md) | Medium | Dynamic Programming | 30 minutes |
| 󰄰 | [51](https://leetcode.com/problems/partition-equal-subset-sum/) | [Partition Equal Subset Sum](docs/problems/partition_equal_subset_sum.md) | Medium | Dynamic Programming | 30 minutes |
| 󰄰 | [52](https://leetcode.com/problems/string-to-integer-atoi/) | [String to Integer (atoi)](docs/problems/string_to_integer_atoi.md) | Medium | String | 25 minutes |
| 󰄰 | [53](https://leetcode.com/problems/spiral-matrix/) | [Spiral Matrix](docs/problems/spiral_matrix.md) | Medium | Array | 25 minutes |
| 󰄰 | [54](https://leetcode.com/problems/subsets/) | [Subsets](docs/problems/subsets.md) | Medium | Backtracking | 30 minutes |
| 󰄰 | [55](https://leetcode.com/problems/binary-tree-right-side-view/) | [Binary Tree Right Side View](docs/problems/binary_tree_right_side_view.md) | Medium | Tree | 20 minutes |
| 󰄰 | [56](https://leetcode.com/problems/longest-palindromic-substring/) | [Longest Palindromic Substring](docs/problems/longest_palindromic_substring.md) | Medium | String | 25 minutes |
| 󰄰 | [57](https://leetcode.com/problems/unique-paths/) | [Unique Paths](docs/problems/unique_paths.md) | Medium | Dynamic Programming | 20 minutes |
| 󰄰 | [58](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | [Construct Binary Tree from Preorder and Inorder Traversal](docs/problems/construct_binary_tree_from_preorder_and_inorder_traversal.md) | Medium | Tree | 25 minutes |
| 󰄰 | [59](https://leetcode.com/problems/container-with-most-water/) | [Container With Most Water](docs/problems/container_with_most_water.md) | Medium | Array | 35 minutes |
| 󰄰 | [60](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | [Letter Combinations of a Phone Number](docs/problems/letter_combinations_of_a_phone_number.md) | Medium | Backtracking | 30 minutes |
| 󰄰 | [61](https://leetcode.com/problems/word-search/) | [Word Search](docs/problems/word_search.md) | Medium | Backtracking | 30 minutes |
| 󰄰 | [62](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | [Find All Anagrams in a String](docs/problems/find_all_anagrams_in_a_string.md) | Medium | String | 30 minutes |
| 󰄰 | [63](https://leetcode.com/problems/minimum-height-trees/) | [Minimum Height Trees](docs/problems/minimum_height_trees.md) | Medium | Graph | 30 minutes |
| 󰄰 | [64](https://leetcode.com/problems/task-scheduler/) | [Task Scheduler](docs/problems/task_scheduler.md) | Medium | Heap | 35 minutes |
| 󰄰 | [65](https://leetcode.com/problems/lru-cache/) | [LRU Cache](docs/problems/lru_cache.md) | Medium | Linked List | 30 minutes |
| 󰄰 | [66](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | [Kth Smallest Element in a BST](docs/problems/kth_smallest_element_in_a_bst.md) | Medium | Tree | 25 minutes |
| 󰄰 | [67](https://leetcode.com/problems/minimum-window-substring/) | [Minimum Window Substring](docs/problems/minimum_window_substring.md) | Hard | String | 30 minutes |
| 󰄰 | [68](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | [Serialize and Deserialize Binary Tree](docs/problems/serialize_and_deserialize_binary_tree.md) | Hard | Tree | 40 minutes |
| 󰄰 | [69](https://leetcode.com/problems/trapping-rain-water/) | [Trapping Rain Water](docs/problems/trapping_rain_water.md) | Hard | Stack | 35 minutes |
| 󰄰 | [70](https://leetcode.com/problems/find-median-from-data-stream/) | [Find Median from Data Stream](docs/problems/find_median_from_data_stream.md) | Hard | Heap | 30 minutes |
| 󰄰 | [71](https://leetcode.com/problems/word-ladder/) | [Word Ladder](docs/problems/word_ladder.md) | Hard | BFS | 45 minutes |
| 󰄰 | [72](https://leetcode.com/problems/basic-calculator/) | [Basic Calculator](docs/problems/basic_calculator.md) | Hard | Stack | 40 minutes |
| 󰄰 | [73](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | [Maximum Profit in Job Scheduling](docs/problems/maximum_profit_in_job_scheduling.md) | Hard | Binary Search | 45 minutes |
| 󰄰 | [74](https://leetcode.com/problems/merge-k-sorted-lists/) | [Merge k Sorted Lists](docs/problems/merge_k_sorted_lists.md) | Hard | Linked List | 30 minutes |
| 󰄰 | [75](https://leetcode.com/problems/largest-rectangle-in-histogram/) | [Largest Rectangle in Histogram](docs/problems/largest_rectangle_in_histogram.md) | Hard | Stack | 35 minutes |

Two bonus problems beyond the canonical 75 are also covered: [Binary Tree Maximum Path Sum](docs/problems/binary_tree_maximum_path_sum.md) (Hard) and [Maximum Frequency Stack](docs/problems/maximum_frequency_stack.md) (Hard).

The [8-week schedule](docs/interview_prep/study_plan.md#the-8-week-schedule) organizes the problems in increasing order of difficulty, with related problem types grouped together: each week places a manageable batch of problems, and earlier weeks focus on foundational concepts while later weeks tackle more advanced topics.

## Pattern Intuition

Beyond the individual problems, the guide includes [algorithm pattern intuition guides](docs/patterns/index.md) covering the recurring patterns these problems share (sliding window, two pointers, binary search, backtracking, dynamic programming, graph traversal, and more). Each guide explains *why* the pattern works, when it applies, and the invariant that makes it correct, then maps the pattern to the Grind 75 problems that use it. The guides are adapted from the [NeetCode practice framework](https://lufftw.github.io/neetcode/).

## System Design

Coding rounds are only half the interview loop. The [System Design section](docs/system_design/index.md) is a growing scaffold for the other half: a repeatable [interview method](docs/system_design/method.md) with a 45-minute time budget, [back-of-envelope estimation](docs/system_design/estimation.md) skills, a [building-blocks vocabulary](docs/system_design/building_blocks.md) from load balancers to consistency models, and [guided case studies](docs/system_design/case_studies/index.md) (URL shortener, rate limiter, news feed, chat) that walk the method with collapsible answers and extension checklists.

## Practice Workspace

The [`practice/`](practice/) directory is a `pytest` workspace for solving the problems yourself rather than just reading them. Each problem has its own folder with a `solution.py` to implement, two test sets that mirror LeetCode's Run (the examples) and Submit (a full corner-case gauntlet), and a `__main__` block for stepping through a single case in a debugger. An unsolved `solution.py` raises `NotSolved` so its tests skip until you fill it in. A progress tracker (`practice/progress.py`) derives solved status from the test suite, records your confidence per problem, and maintains a spaced-repetition review queue. See [`practice/README.md`](practice/README.md) for setup and the full workflow.

## Creating a PDF of the Grind 75 Track with Pandoc

You can generate a compiled PDF of the Grind 75 track problems using the included configuration:

### Prerequisites

1. Install [Pandoc](https://pandoc.org/installing.html) - universal document converter
   - On Debian/Ubuntu: `sudo apt-get install pandoc`
   - On macOS: `brew install pandoc`
2. Install [LaTeX](https://www.latex-project.org/get/) distribution (like TeX Live, MiKTeX, or MacTeX)
   - On Debian/Ubuntu: `sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-plain-generic`
   - On macOS: `brew install --cask mactex`
3. Make sure all markdown files referenced in `grind75.yaml` exist in your directory

### Generating the PDF

Run the following command from the terminal in your project directory:

```bash
pandoc --defaults grind75.yaml
```

This will:

- Read configuration from `grind75.yaml`
- Combine the Grind 75 track markdown files (`two_sum.md`, `valid_parentheses.md`, etc.)
- Create a table of contents
- Generate a PDF file named `grind75.pdf` using the XeLaTeX engine

To customize the output, edit the `grind75.yaml` file. You can add more input files, change metadata, adjust the table of contents, or modify the PDF engine settings.

As you work through each problem, document your solutions, optimizations, and insights. This creates a personalized study resource that helps reinforce your understanding of algorithms and data structures while preparing you for technical interviews.
