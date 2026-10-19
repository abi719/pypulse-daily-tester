"""
Comprehensive Python Question Bank for Daily Coding Tests
Each question includes:
- id, title, topic, difficulty
- description, starter_code
- sample_test_cases (visible)
- hidden_test_cases (for final grading)
- solution (optimal Pythonic code)
- explanation (clear concept walkthrough)
- pythonic_tip (best practices, built-ins, idioms)
"""

QUESTIONS = [
    # --- Topic: Variables, Types & Math Basics ---
    {
        "id": "py-001",
        "title": "Temperature Converter",
        "topic": "Variables & Math",
        "difficulty": "Easy",
        "description": "Write a function `celsius_to_fahrenheit(c: float) -> float` that converts a temperature from Celsius to Fahrenheit.\n\nFormula: `F = (C * 9/5) + 32`.\nReturn the result rounded to 2 decimal places using `round(val, 2)`.",
        "starter_code": "def celsius_to_fahrenheit(c: float) -> float:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [0], "expected": 32.0, "explanation": "0 Celsius is 32 Fahrenheit"},
            {"input": [100], "expected": 212.0, "explanation": "100 Celsius is 212 Fahrenheit"},
            {"input": [37], "expected": 98.6, "explanation": "Human body temp 37C is 98.6F"}
        ],
        "hidden_test_cases": [
            {"input": [-40], "expected": -40.0},
            {"input": [25.5], "expected": 77.9},
            {"input": [-10], "expected": 14.0}
        ],
        "solution": "def celsius_to_fahrenheit(c: float) -> float:\n    return round((c * 9/5) + 32, 2)",
        "explanation": "Multiply Celsius by 9/5 and add 32. Use `round(..., 2)` to constrain float precision.",
        "pythonic_tip": "Python handles floating point arithmetic cleanly, but beware of precision quirks (e.g. 0.1 + 0.2 != 0.3). `round()` helps sanitize display values."
    },
    {
        "id": "py-002",
        "title": "Sum of Natural Numbers",
        "topic": "Variables & Math",
        "difficulty": "Easy",
        "description": "Write a function `sum_of_n(n: int) -> int` that calculates the sum of all positive integers from 1 up to `n` (inclusive).\nIf `n <= 0`, return 0.",
        "starter_code": "def sum_of_n(n: int) -> int:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [5], "expected": 15, "explanation": "1 + 2 + 3 + 4 + 5 = 15"},
            {"input": [1], "expected": 1, "explanation": "Sum up to 1 is 1"},
            {"input": [0], "expected": 0, "explanation": "0 or negative returns 0"}
        ],
        "hidden_test_cases": [
            {"input": [10], "expected": 55},
            {"input": [100], "expected": 5050},
            {"input": [-5], "expected": 0}
        ],
        "solution": "def sum_of_n(n: int) -> int:\n    if n <= 0:\n        return 0\n    return (n * (n + 1)) // 2",
        "explanation": "While a loop or `sum(range(1, n + 1))` works in O(n), Gauss' formula `n * (n + 1) // 2` computes it in constant O(1) time.",
        "pythonic_tip": "Use integer division `//` instead of `/` when the result is guaranteed to be an integer, avoiding floating point conversion."
    },
    {
        "id": "py-003",
        "title": "Swap Without Temp Variable",
        "topic": "Variables & Math",
        "difficulty": "Easy",
        "description": "Write a function `swap_values(a, b)` that returns a tuple `(b, a)` with the values swapped.",
        "starter_code": "def swap_values(a, b):\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [1, 2], "expected": [2, 1], "explanation": "1, 2 becomes 2, 1"},
            {"input": ["hello", "world"], "expected": ["world", "hello"], "explanation": "Strings are swapped"}
        ],
        "hidden_test_cases": [
            {"input": [True, False], "expected": [False, True]},
            {"input": [[1], [2]], "expected": [[2], [1]]},
            {"input": [None, 42], "expected": [42, None]}
        ],
        "solution": "def swap_values(a, b):\n    return b, a",
        "explanation": "Python supports tuple packing and unpacking natively. `a, b = b, a` evaluates the right-hand tuple first, then assigns it.",
        "pythonic_tip": "Never use a temporary variable in Python for swapping. Python's `b, a` tuple unpacking is faster and cleaner."
    },

    # --- Topic: String Manipulation & Slicing ---
    {
        "id": "py-004",
        "title": "Reverse a String",
        "topic": "Strings",
        "difficulty": "Easy",
        "description": "Write a function `reverse_string(s: str) -> str` that takes a string `s` and returns the reversed string.",
        "starter_code": "def reverse_string(s: str) -> str:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": ["python"], "expected": "nohtyp", "explanation": "'python' reversed is 'nohtyp'"},
            {"input": ["racecar"], "expected": "racecar", "explanation": "Palindrome stays the same"},
            {"input": [""], "expected": "", "explanation": "Empty string returns empty"}
        ],
        "hidden_test_cases": [
            {"input": ["12345"], "expected": "54321"},
            {"input": ["A"], "expected": "A"},
            {"input": ["Hello World!"], "expected": "!dlroW olleH"}
        ],
        "solution": "def reverse_string(s: str) -> str:\n    return s[::-1]",
        "explanation": "Python's slice notation `s[start:stop:step]` with step `-1` reverses any sequence efficiently in C-level speed.",
        "pythonic_tip": "`s[::-1]` is the idiomatic Python way to reverse strings. Alternatively, `''.join(reversed(s))` also works."
    },
    {
        "id": "py-005",
        "title": "Count Vowels",
        "topic": "Strings",
        "difficulty": "Easy",
        "description": "Write a function `count_vowels(s: str) -> int` that returns the count of vowels (`a, e, i, o, u`, case-insensitive) in the given string `s`.",
        "starter_code": "def count_vowels(s: str) -> int:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": ["Hello World"], "expected": 3, "explanation": "'e', 'o', 'o' are vowels"},
            {"input": ["PYTHON"], "expected": 1, "explanation": "'O' is the only vowel"},
            {"input": ["xyz"], "expected": 0, "explanation": "No vowels present"}
        ],
        "hidden_test_cases": [
            {"input": ["AEIOUaeiou"], "expected": 10},
            {"input": [""], "expected": 0},
            {"input": ["The quick brown fox jumps over the lazy dog"], "expected": 11}
        ],
        "solution": "def count_vowels(s: str) -> int:\n    vowels = set('aeiouAEIOU')\n    return sum(1 for char in s if char in vowels)",
        "explanation": "Convert vowel lookups to a `set` for O(1) membership testing, then sum the matching generator expression.",
        "pythonic_tip": "Using a generator expression `sum(1 for c in s if c in vowels)` avoids creating an intermediate list in memory."
    },
    {
        "id": "py-006",
        "title": "Is Palindrome",
        "topic": "Strings",
        "difficulty": "Easy",
        "description": "Write a function `is_palindrome(s: str) -> bool` that checks if a string is a palindrome.\nIgnore spaces, punctuation, and casing. For example, `'A man, a plan, a canal: Panama'` is a palindrome.",
        "starter_code": "def is_palindrome(s: str) -> bool:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": ["A man, a plan, a canal: Panama"], "expected": True, "explanation": "Alphanumeric characters form 'amanaplanacanalpanama'"},
            {"input": ["race a car"], "expected": False, "explanation": "Not a palindrome"},
            {"input": ["Madam"], "expected": True, "explanation": "'madam' matches reverse"}
        ],
        "hidden_test_cases": [
            {"input": [""], "expected": True},
            {"input": ["0P"], "expected": False},
            {"input": ["Was it a car or a cat I saw?"], "expected": True}
        ],
        "solution": "def is_palindrome(s: str) -> bool:\n    cleaned = ''.join(c.lower() for c in s if c.isalnum())\n    return cleaned == cleaned[::-1]",
        "explanation": "Filter with `c.isalnum()` and `c.lower()`, then check if the cleaned string equals its reverse.",
        "pythonic_tip": "`str.isalnum()` checks if a character is either letters or digits without needing regular expressions."
    },
    {
        "id": "py-007",
        "title": "Mask Credit Card",
        "topic": "Strings",
        "difficulty": "Medium",
        "description": "Write a function `mask_string(s: str) -> str` that masks all characters with `#` except the last 4 characters.\nIf the string has length 4 or fewer, return it unchanged.",
        "starter_code": "def mask_string(s: str) -> str:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": ["1234567812345678"], "expected": "############5678", "explanation": "First 12 digits masked"},
            {"input": ["1234"], "expected": "1234", "explanation": "Length 4 is not masked"},
            {"input": ["45"], "expected": "45", "explanation": "Short string unchanged"}
        ],
        "hidden_test_cases": [
            {"input": ["12345"], "expected": "#2345"},
            {"input": [""], "expected": ""},
            {"input": ["SuperSecretPassword"], "expected": "###############word"}
        ],
        "solution": "def mask_string(s: str) -> str:\n    if len(s) <= 4:\n        return s\n    return '#' * (len(s) - 4) + s[-4:]",
        "explanation": "Multiply `'#'` by `len(s) - 4` and concatenate with the last 4 characters slice `s[-4:]`.",
        "pythonic_tip": "String repetition with `'#' * count` is idiomatic and clean in Python."
    },

    # --- Topic: Conditionals & Logic ---
    {
        "id": "py-008",
        "title": "FizzBuzz Single Number",
        "topic": "Conditionals",
        "difficulty": "Easy",
        "description": "Write a function `fizz_buzz_val(n: int) -> str` that returns:\n- `'FizzBuzz'` if `n` is divisible by both 3 and 5\n- `'Fizz'` if `n` is divisible by 3\n- `'Buzz'` if `n` is divisible by 5\n- The number as a string (e.g. `'7'`) if not divisible by either.",
        "starter_code": "def fizz_buzz_val(n: int) -> str:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [15], "expected": "FizzBuzz", "explanation": "Divisible by 3 and 5"},
            {"input": [9], "expected": "Fizz", "explanation": "Divisible by 3"},
            {"input": [10], "expected": "Buzz", "explanation": "Divisible by 5"}
        ],
        "hidden_test_cases": [
            {"input": [7], "expected": "7"},
            {"input": [30], "expected": "FizzBuzz"},
            {"input": [1], "expected": "1"}
        ],
        "solution": "def fizz_buzz_val(n: int) -> str:\n    if n % 15 == 0:\n        return 'FizzBuzz'\n    elif n % 3 == 0:\n        return 'Fizz'\n    elif n % 5 == 0:\n        return 'Buzz'\n    return str(n)",
        "explanation": "Always test the compound condition `n % 15 == 0` first before testing individual divisors.",
        "pythonic_tip": "Alternatively, you can concatenate: `res = ('Fizz' if n % 3 == 0 else '') + ('Buzz' if n % 5 == 0 else ''); return res or str(n)`."
    },
    {
        "id": "py-009",
        "title": "Leap Year Checker",
        "topic": "Conditionals",
        "difficulty": "Easy",
        "description": "Write a function `is_leap_year(year: int) -> bool` that determines if a given year is a leap year.\nA year is a leap year if it is divisible by 4, except end-of-century years which must be divisible by 400.\n(E.g., 2000 is leap, 1900 is NOT, 2024 is leap).",
        "starter_code": "def is_leap_year(year: int) -> bool:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [2024], "expected": True, "explanation": "2024 is divisible by 4"},
            {"input": [1900], "expected": False, "explanation": "Century year not divisible by 400"},
            {"input": [2000], "expected": True, "explanation": "Century year divisible by 400"}
        ],
        "hidden_test_cases": [
            {"input": [2023], "expected": False},
            {"input": [1600], "expected": True},
            {"input": [2100], "expected": False}
        ],
        "solution": "def is_leap_year(year: int) -> bool:\n    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)",
        "explanation": "Combine boolean operators: divisible by 4 and not 100, or divisible by 400.",
        "pythonic_tip": "Directly return boolean expressions instead of writing `if cond: return True else: return False`."
    },
    {
        "id": "py-010",
        "title": "Grade Calculator",
        "topic": "Conditionals",
        "difficulty": "Easy",
        "description": "Write a function `get_grade(score: int) -> str`:\n- 90 to 100: `'A'`\n- 80 to 89: `'B'`\n- 70 to 79: `'C'`\n- 60 to 69: `'D'`\n- Below 60: `'F'`\nIf score is not between 0 and 100 inclusive, return `'Invalid'`.",
        "starter_code": "def get_grade(score: int) -> str:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [95], "expected": "A", "explanation": "Score >= 90"},
            {"input": [82], "expected": "B", "explanation": "Score 80-89"},
            {"input": [58], "expected": "F", "explanation": "Below 60"}
        ],
        "hidden_test_cases": [
            {"input": [105], "expected": "Invalid"},
            {"input": [-1], "expected": "Invalid"},
            {"input": [70], "expected": "C"}
        ],
        "solution": "def get_grade(score: int) -> str:\n    if not (0 <= score <= 100):\n        return 'Invalid'\n    if score >= 90:\n        return 'A'\n    elif score >= 80:\n        return 'B'\n    elif score >= 70:\n        return 'C'\n    elif score >= 60:\n        return 'D'\n    return 'F'",
        "explanation": "Validate bounds first with chained comparison `0 <= score <= 100`, then check descending score thresholds.",
        "pythonic_tip": "Python supports chained comparisons like `0 <= score <= 100` which are much more readable than `score >= 0 and score <= 100`."
    },

    # --- Topic: Loops & Iterations ---
    {
        "id": "py-011",
        "title": "Sum of Digits",
        "topic": "Loops & Iterations",
        "difficulty": "Easy",
        "description": "Write a function `sum_digits(n: int) -> int` that calculates the sum of all digits of a non-negative integer `n`.\nE.g., `sum_digits(1234)` -> `1 + 2 + 3 + 4 = 10`.",
        "starter_code": "def sum_digits(n: int) -> int:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [1234], "expected": 10, "explanation": "1+2+3+4 = 10"},
            {"input": [0], "expected": 0, "explanation": "Sum of 0 is 0"},
            {"input": [999], "expected": 27, "explanation": "9+9+9 = 27"}
        ],
        "hidden_test_cases": [
            {"input": [5], "expected": 5},
            {"input": [1000000], "expected": 1},
            {"input": [4832], "expected": 17}
        ],
        "solution": "def sum_digits(n: int) -> int:\n    return sum(int(d) for d in str(n))",
        "explanation": "Convert number to string, iterate through each character, convert back to int, and sum them.",
        "pythonic_tip": "You can also solve this mathematically using modulo `% 10` and integer division `// 10` in a while loop."
    },
    {
        "id": "py-012",
        "title": "Factorial Calculation",
        "topic": "Loops & Iterations",
        "difficulty": "Easy",
        "description": "Write a function `factorial(n: int) -> int` that computes the factorial of non-negative integer `n`.\nRemember `0! = 1` and `5! = 5 * 4 * 3 * 2 * 1 = 120`.",
        "starter_code": "def factorial(n: int) -> int:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [5], "expected": 120, "explanation": "5! = 120"},
            {"input": [0], "expected": 1, "explanation": "0! is defined as 1"},
            {"input": [1], "expected": 1, "explanation": "1! is 1"}
        ],
        "hidden_test_cases": [
            {"input": [3], "expected": 6},
            {"input": [7], "expected": 5040},
            {"input": [10], "expected": 3628800}
        ],
        "solution": "def factorial(n: int) -> int:\n    result = 1\n    for i in range(2, n + 1):\n        result *= i\n    return result",
        "explanation": "Initialize product to 1 and multiply incrementally up to `n`.",
        "pythonic_tip": "In the standard library, `math.factorial(n)` exists, but writing it iteratively tests fundamental loop mechanics."
    },
    {
        "id": "py-013",
        "title": "Prime Number Checker",
        "topic": "Loops & Iterations",
        "difficulty": "Medium",
        "description": "Write a function `is_prime(n: int) -> bool` that returns `True` if `n` is a prime number, and `False` otherwise.\n(Numbers <= 1 are NOT prime. 2 and 3 are prime).",
        "starter_code": "def is_prime(n: int) -> bool:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [7], "expected": True, "explanation": "7 has no divisors other than 1 and 7"},
            {"input": [4], "expected": False, "explanation": "4 is divisible by 2"},
            {"input": [1], "expected": False, "explanation": "1 is not prime"}
        ],
        "hidden_test_cases": [
            {"input": [2], "expected": True},
            {"input": [29], "expected": True},
            {"input": [100], "expected": False}
        ],
        "solution": "def is_prime(n: int) -> bool:\n    if n <= 1:\n        return False\n    if n <= 3:\n        return True\n    if n % 2 == 0 or n % 3 == 0:\n        return False\n    i = 5\n    while i * i <= n:\n        if n % i == 0 or n % (i + 2) == 0:\n            return False\n        i += 6\n    return True",
        "explanation": "Check up to the square root of n (sqrt(n)). Numbers <= 1 are non-prime. Stepping by 6 covers primes 6k +/- 1.",
        "pythonic_tip": "Only testing divisors up to `int(n**0.5) + 1` reduces time complexity from O(n) to O(√n)."
    },

    # --- Topic: Lists & Sequences ---
    {
        "id": "py-014",
        "title": "Find Second Largest Number",
        "topic": "Lists & Tuples",
        "difficulty": "Medium",
        "description": "Write a function `second_largest(numbers: list[int]) -> int | None` that returns the second distinct largest number from a list of integers.\nIf there are fewer than 2 distinct numbers, return `None`.",
        "starter_code": "def second_largest(numbers: list[int]):\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [[10, 20, 4, 45, 99]], "expected": 45, "explanation": "99 is largest, 45 is second largest"},
            {"input": [[5, 5, 5]], "expected": None, "explanation": "Only one distinct number"},
            {"input": [[1, 2]], "expected": 1, "explanation": "1 is second largest"}
        ],
        "hidden_test_cases": [
            {"input": [[]], "expected": None},
            {"input": [[100]], "expected": None},
            {"input": [[-10, -5, -2, -1]], "expected": -2}
        ],
        "solution": "def second_largest(numbers: list[int]):\n    unique = sorted(set(numbers))\n    if len(unique) < 2:\n        return None\n    return unique[-2]",
        "explanation": "Eliminate duplicates using `set()`, sort ascending, and select the second element from the end with index `[-2]`.",
        "pythonic_tip": "`set()` removes duplicates in O(n) time, and `unique[-2]` indexes directly from the right without needing `len()`."
    },
    {
        "id": "py-015",
        "title": "Remove Duplicates While Preserving Order",
        "topic": "Lists & Tuples",
        "difficulty": "Easy",
        "description": "Write a function `remove_duplicates(items: list) -> list` that removes all duplicate elements from a list while maintaining the original insertion order.",
        "starter_code": "def remove_duplicates(items: list) -> list:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [[1, 2, 2, 3, 4, 4, 1]], "expected": [1, 2, 3, 4], "explanation": "Duplicates removed in order"},
            {"input": [["a", "b", "a", "c"]], "expected": ["a", "b", "c"], "explanation": "Strings preserved in order"}
        ],
        "hidden_test_cases": [
            {"input": [[]], "expected": []},
            {"input": [[1, 1, 1]], "expected": [1]},
            {"input": [[5, 4, 3, 2, 1]], "expected": [5, 4, 3, 2, 1]}
        ],
        "solution": "def remove_duplicates(items: list) -> list:\n    return list(dict.fromkeys(items))",
        "explanation": "Since Python 3.7, dictionaries preserve insertion order. `dict.fromkeys(items)` removes duplicates in O(n) time while keeping order.",
        "pythonic_tip": "`list(dict.fromkeys(items))` is the ultimate Pythonic one-liner for ordered deduplication."
    },
    {
        "id": "py-016",
        "title": "Chunk a List",
        "topic": "Lists & Tuples",
        "difficulty": "Medium",
        "description": "Write a function `chunk_list(lst: list, size: int) -> list[list]` that splits a list into smaller chunks of length `size`.\nThe last chunk may contain fewer elements if the list does not divide evenly.\nIf `size <= 0`, return `[]`.",
        "starter_code": "def chunk_list(lst: list, size: int) -> list[list]:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [[1, 2, 3, 4, 5], 2], "expected": [[1, 2], [3, 4], [5]], "explanation": "Chunked by 2"},
            {"input": [[1, 2, 3], 3], "expected": [[1, 2, 3]], "explanation": "Single chunk"},
            {"input": [[], 2], "expected": [], "explanation": "Empty list produces empty chunks"}
        ],
        "hidden_test_cases": [
            {"input": [[1, 2, 3, 4], 1], "expected": [[1], [2], [3], [4]]},
            {"input": [[1, 2, 3], 0], "expected": []},
            {"input": [["a", "b", "c", "d", "e", "f", "g"], 3], "expected": [["a", "b", "c"], ["d", "e", "f"], ["g"]]}
        ],
        "solution": "def chunk_list(lst: list, size: int) -> list[list]:\n    if size <= 0:\n        return []\n    return [lst[i:i + size] for i in range(0, len(lst), size)]",
        "explanation": "Use `range(0, len(lst), size)` step parameter to jump by chunk size, then slice `lst[i:i + size]` in a list comprehension.",
        "pythonic_tip": "List comprehensions combined with slice step parameters produce clean and highly optimized bytecode."
    },
    {
        "id": "py-017",
        "title": "Merge Two Sorted Lists",
        "topic": "Lists & Tuples",
        "difficulty": "Medium",
        "description": "Write a function `merge_sorted(list1: list[int], list2: list[int]) -> list[int]` that merges two already sorted lists of integers into a single sorted list.",
        "starter_code": "def merge_sorted(list1: list[int], list2: list[int]) -> list[int]:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [[1, 3, 5], [2, 4, 6]], "expected": [1, 2, 3, 4, 5, 6], "explanation": "Alternating values merged"},
            {"input": [[], [1, 2]], "expected": [1, 2], "explanation": "One empty list"},
            {"input": [[5], [1, 2, 3]], "expected": [1, 2, 3, 5], "explanation": "Appended in sorted order"}
        ],
        "hidden_test_cases": [
            {"input": [[], []], "expected": []},
            {"input": [[1, 2, 3], [4, 5, 6]], "expected": [1, 2, 3, 4, 5, 6]},
            {"input": [[-5, 0, 5], [-10, 2]], "expected": [-10, -5, 0, 2, 5]}
        ],
        "solution": "def merge_sorted(list1: list[int], list2: list[int]) -> list[int]:\n    return sorted(list1 + list2)",
        "explanation": "Concatenate lists with `+` and call Python's Timsort via `sorted()`. Timsort runs in O(N) when merging two sorted sub-runs.",
        "pythonic_tip": "Python's `sorted()` uses Timsort, which detects pre-sorted runs and executes near O(N) linear time."
    },

    # --- Topic: Dictionaries & Sets ---
    {
        "id": "py-018",
        "title": "Word Frequency Counter",
        "topic": "Dictionaries & Sets",
        "difficulty": "Easy",
        "description": "Write a function `word_frequencies(words: list[str]) -> dict[str, int]` that returns a dictionary mapping each lowercased word to the number of times it appears in the list.",
        "starter_code": "def word_frequencies(words: list[str]) -> dict[str, int]:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [["apple", "banana", "apple", "cherry"]], "expected": {"apple": 2, "banana": 1, "cherry": 1}, "explanation": "apple occurs twice"},
            {"input": [["Dog", "dog", "DOG"]], "expected": {"dog": 3}, "explanation": "Case insensitive lowercased"}
        ],
        "hidden_test_cases": [
            {"input": [[]], "expected": {}},
            {"input": [["one"]], "expected": {"one": 1}},
            {"input": [["a", "b", "a", "c", "b", "a"]], "expected": {"a": 3, "b": 2, "c": 1}}
        ],
        "solution": "def word_frequencies(words: list[str]) -> dict[str, int]:\n    counts = {}\n    for word in words:\n        w = word.lower()\n        counts[w] = counts.get(w, 0) + 1\n    return counts",
        "explanation": "Use `dict.get(key, 0)` to provide a safe default value if the key does not yet exist in the dictionary.",
        "pythonic_tip": "`dict.get(key, 0)` avoids verbose `if key in dict:` checks."
    },
    {
        "id": "py-019",
        "title": "Invert a Dictionary",
        "topic": "Dictionaries & Sets",
        "difficulty": "Medium",
        "description": "Write a function `invert_dict(d: dict) -> dict` that swaps keys and values in a dictionary.\nAssume all original values are unique and hashable (e.g. strings or ints).",
        "starter_code": "def invert_dict(d: dict) -> dict:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [{"a": 1, "b": 2, "c": 3}], "expected": {1: "a", 2: "b", 3: "c"}, "explanation": "Keys and values swapped"},
            {"input": [{"first": "apple", "second": "banana"}], "expected": {"apple": "first", "banana": "second"}, "explanation": "String values swapped to keys"}
        ],
        "hidden_test_cases": [
            {"input": [{}], "expected": {}},
            {"input": [{"x": 100}], "expected": {100: "x"}}
        ],
        "solution": "def invert_dict(d: dict) -> dict:\n    return {v: k for k, v in d.items()}",
        "explanation": "Use a dictionary comprehension iterating over `d.items()` and yielding `{value: key}`.",
        "pythonic_tip": "Dictionary comprehension `{v: k for k, v in d.items()}` is concise, fast, and idiomatic."
    },
    {
        "id": "py-020",
        "title": "Find Common Elements in Sets",
        "topic": "Dictionaries & Sets",
        "difficulty": "Easy",
        "description": "Write a function `common_elements(list1: list, list2: list) -> list` that returns a sorted list of unique elements present in both `list1` and `list2`.",
        "starter_code": "def common_elements(list1: list, list2: list) -> list:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [[1, 2, 3, 4], [3, 4, 5, 6]], "expected": [3, 4], "explanation": "3 and 4 are common"},
            {"input": [[1, 2], [3, 4]], "expected": [], "explanation": "No common elements"}
        ],
        "hidden_test_cases": [
            {"input": [[1, 1, 1], [1, 1]], "expected": [1]},
            {"input": [[], [1, 2]], "expected": []},
            {"input": [[10, 50, 20], [20, 30, 10]], "expected": [10, 20]}
        ],
        "solution": "def common_elements(list1: list, list2: list) -> list:\n    return sorted(list(set(list1) & set(list2)))",
        "explanation": "Convert both lists to sets and use the set intersection operator `&`.",
        "pythonic_tip": "Set operators `&` (intersection), `|` (union), and `-` (difference) express math set operations directly."
    },

    # --- Topic: Functions & Functional Tools ---
    {
        "id": "py-021",
        "title": "Filter Even Numbers",
        "topic": "Functions & Logic",
        "difficulty": "Easy",
        "description": "Write a function `filter_evens(nums: list[int]) -> list[int]` that returns a new list containing only the even numbers from `nums`, preserving their order.",
        "starter_code": "def filter_evens(nums: list[int]) -> list[int]:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [[1, 2, 3, 4, 5, 6]], "expected": [2, 4, 6], "explanation": "2, 4, 6 are even"},
            {"input": [[1, 3, 5]], "expected": [], "explanation": "No even numbers"},
            {"input": [[0, -2, -3]], "expected": [0, -2], "explanation": "0 and negative evens included"}
        ],
        "hidden_test_cases": [
            {"input": [[]], "expected": []},
            {"input": [[2, 4, 8]], "expected": [2, 4, 8]},
            {"input": [[100, 101, 102]], "expected": [100, 102]}
        ],
        "solution": "def filter_evens(nums: list[int]) -> list[int]:\n    return [x for x in nums if x % 2 == 0]",
        "explanation": "Filter with a list comprehension checking if `x % 2 == 0`.",
        "pythonic_tip": "List comprehensions are preferred in Python over `list(filter(lambda x: x % 2 == 0, nums))` for readability."
    },
    {
        "id": "py-022",
        "title": "Cumulative Sum (Running Total)",
        "topic": "Functions & Logic",
        "difficulty": "Medium",
        "description": "Write a function `running_sum(nums: list[int]) -> list[int]` that returns a list where each element at index `i` is the sum of elements from index 0 through `i`.\nE.g., `[1, 2, 3, 4]` -> `[1, 3, 6, 10]`.",
        "starter_code": "def running_sum(nums: list[int]) -> list[int]:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [[1, 2, 3, 4]], "expected": [1, 3, 6, 10], "explanation": "1, 1+2=3, 3+3=6, 6+4=10"},
            {"input": [[1, 1, 1, 1]], "expected": [1, 2, 3, 4], "explanation": "Running sum of 1s"},
            {"input": [[]], "expected": [], "explanation": "Empty list"}
        ],
        "hidden_test_cases": [
            {"input": [[5]], "expected": [5]},
            {"input": [[3, -1, 2, -1]], "expected": [3, 2, 4, 3]},
            {"input": [[0, 0, 0]], "expected": [0, 0, 0]}
        ],
        "solution": "def running_sum(nums: list[int]) -> list[int]:\n    res = []\n    total = 0\n    for n in nums:\n        total += n\n        res.append(total)\n    return res",
        "explanation": "Maintain a running total variable and append it on each iteration, achieving linear O(N) complexity.",
        "pythonic_tip": "In the standard library, `itertools.accumulate(nums)` does this out of the box."
    },
    {
        "id": "py-023",
        "title": "Check Anagrams",
        "topic": "Strings",
        "difficulty": "Easy",
        "description": "Write a function `is_anagram(s1: str, s2: str) -> bool` that checks if two strings are anagrams of each other (contain the exact same letters in any order).\nIgnore case and spaces.\nE.g., `'listen'` and `'silent'` are anagrams.",
        "starter_code": "def is_anagram(s1: str, s2: str) -> bool:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": ["listen", "silent"], "expected": True, "explanation": "Same letters"},
            {"input": ["hello", "world"], "expected": False, "explanation": "Different letters"},
            {"input": ["Astronomer", "Moon starer"], "expected": True, "explanation": "Ignores case and spaces"}
        ],
        "hidden_test_cases": [
            {"input": ["a", "a"], "expected": True},
            {"input": ["rat", "car"], "expected": False},
            {"input": ["", ""], "expected": True}
        ],
        "solution": "def is_anagram(s1: str, s2: str) -> bool:\n    c1 = sorted(s1.lower().replace(' ', ''))\n    c2 = sorted(s2.lower().replace(' ', ''))\n    return c1 == c2",
        "explanation": "Normalize both strings by removing spaces and lowercasing, then compare their sorted characters.",
        "pythonic_tip": "`collections.Counter` allows checking anagrams in linear O(N) time without sorting: `Counter(s1) == Counter(s2)`."
    },
    {
        "id": "py-024",
        "title": "Capitalize Words",
        "topic": "Strings",
        "difficulty": "Easy",
        "description": "Write a function `capitalize_words(sentence: str) -> str` that capitalizes the first letter of every word in a sentence while keeping subsequent letters lowercase.\nWords are separated by spaces.",
        "starter_code": "def capitalize_words(sentence: str) -> str:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": ["hello world"], "expected": "Hello World", "explanation": "Both words capitalized"},
            {"input": ["python CODING"], "expected": "Python Coding", "explanation": "Subsequent letters lowercased"},
            {"input": [""], "expected": "", "explanation": "Empty string"}
        ],
        "hidden_test_cases": [
            {"input": ["a b c"], "expected": "A B C"},
            {"input": ["already Capitalized"], "expected": "Already Capitalized"},
            {"input": ["single"], "expected": "Single"}
        ],
        "solution": "def capitalize_words(sentence: str) -> str:\n    if not sentence:\n        return ''\n    return ' '.join(word.capitalize() for word in sentence.split(' '))",
        "explanation": "Split words by space, call `.capitalize()` on each word, and join them back with `' '`.",
        "pythonic_tip": "Beware of `sentence.title()`, which can produce odd results with apostrophes (e.g. `they're` -> `They'Re`). Splitting and using `.capitalize()` is safer."
    },
    {
        "id": "py-025",
        "title": "Find Missing Number",
        "topic": "Functions & Logic",
        "difficulty": "Medium",
        "description": "Given a list `nums` containing `n` distinct numbers taken from the range `0` to `n`, write a function `missing_number(nums: list[int]) -> int` that returns the only number in the range that is missing from the list.\nE.g., `[3, 0, 1]` has `n = 3`, numbers are 0, 1, 2, 3 -> missing is `2`.",
        "starter_code": "def missing_number(nums: list[int]) -> int:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [[3, 0, 1]], "expected": 2, "explanation": "0, 1, 2, 3 -> 2 is missing"},
            {"input": [[0, 1]], "expected": 2, "explanation": "0, 1, 2 -> 2 is missing"},
            {"input": [[9,6,4,2,3,5,7,0,1]], "expected": 8, "explanation": "8 is missing from 0..9"}
        ],
        "hidden_test_cases": [
            {"input": [[0]], "expected": 1},
            {"input": [[1]], "expected": 0},
            {"input": [[1, 2]], "expected": 0}
        ],
        "solution": "def missing_number(nums: list[int]) -> int:\n    n = len(nums)\n    expected_sum = n * (n + 1) // 2\n    return expected_sum - sum(nums)",
        "explanation": "Calculate the expected sum using Gauss' formula $n(n+1)/2$ and subtract the actual sum. The difference is the missing number in O(N) time and O(1) space.",
        "pythonic_tip": "Mathematical difference avoids creating extra sets or sorting, giving optimal O(1) auxiliary memory."
    },

    # --- Topic: Basic Algorithms ---
    {
        "id": "py-026",
        "title": "Two Sum (Basic)",
        "topic": "Basic Algorithms",
        "difficulty": "Medium",
        "description": "Write a function `two_sum(nums: list[int], target: int) -> list[int] | None` that finds two indices such that `nums[i] + nums[j] == target` (`i != j`).\nReturn the indices as `[i, j]` with `i < j`.\nIf no pair exists, return `None`.",
        "starter_code": "def two_sum(nums: list[int], target: int):\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [[2, 7, 11, 15], 9], "expected": [0, 1], "explanation": "nums[0] + nums[1] = 2 + 7 = 9"},
            {"input": [[3, 2, 4], 6], "expected": [1, 2], "explanation": "nums[1] + nums[2] = 2 + 4 = 6"}
        ],
        "hidden_test_cases": [
            {"input": [[3, 3], 6], "expected": [0, 1]},
            {"input": [[1, 2, 3], 10], "expected": None},
            {"input": [[-1, -2, -3, -4], -6], "expected": [1, 3]}
        ],
        "solution": "def two_sum(nums: list[int], target: int):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return None",
        "explanation": "Use a hash map to store each number and its index. For each number, check if its complement (`target - num`) has already been seen in O(N) time.",
        "pythonic_tip": "`enumerate(nums)` provides both index and item cleanly without manual index counting."
    },
    {
        "id": "py-027",
        "title": "Find Maximum Subarray Sum (Kadane's)",
        "topic": "Basic Algorithms",
        "difficulty": "Medium",
        "description": "Write a function `max_sub_array(nums: list[int]) -> int` that finds the sum of the contiguous subarray with the largest sum.\nThe list will have at least 1 number.\nE.g. `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` has max sum `6` (from `[4, -1, 2, 1]`).",
        "starter_code": "def max_sub_array(nums: list[int]) -> int:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "expected": 6, "explanation": "Subarray [4, -1, 2, 1] sums to 6"},
            {"input": [[1]], "expected": 1, "explanation": "Single element"},
            {"input": [[5, 4, -1, 7, 8]], "expected": 23, "explanation": "Full array sum"}
        ],
        "hidden_test_cases": [
            {"input": [[-1]], "expected": -1},
            {"input": [[-2, -1]], "expected": -1},
            {"input": [[1, 2, 3, 4]], "expected": 10}
        ],
        "solution": "def max_sub_array(nums: list[int]) -> int:\n    current_sum = max_sum = nums[0]\n    for x in nums[1:]:\n        current_sum = max(x, current_sum + x)\n        max_sum = max(max_sum, current_sum)\n    return max_sum",
        "explanation": "Kadane's algorithm: at each step, decide whether to add the current element to the running subarray or start a fresh subarray at this element.",
        "pythonic_tip": "`max(x, current_sum + x)` elegantly handles both positive and all-negative arrays."
    },
    {
        "id": "py-028",
        "title": "Roman Numeral to Integer",
        "topic": "Dictionaries & Sets",
        "difficulty": "Medium",
        "description": "Write a function `roman_to_int(s: str) -> int` that converts a Roman numeral string into an integer.\nRoman values: I=1, V=5, X=10, L=50, C=100, D=500, M=1000.\nSubtractive rule applies: IV=4, IX=9, XL=40, XC=90, CD=400, CM=900.",
        "starter_code": "def roman_to_int(s: str) -> int:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": ["III"], "expected": 3, "explanation": "1 + 1 + 1 = 3"},
            {"input": ["LVIII"], "expected": 58, "explanation": "L = 50, V = 5, III = 3"},
            {"input": ["MCMXCIV"], "expected": 1994, "explanation": "M = 1000, CM = 900, XC = 90, IV = 4"}
        ],
        "hidden_test_cases": [
            {"input": ["IV"], "expected": 4},
            {"input": ["IX"], "expected": 9},
            {"input": ["XL"], "expected": 40}
        ],
        "solution": "def roman_to_int(s: str) -> int:\n    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}\n    total = 0\n    for i in range(len(s)):\n        if i + 1 < len(s) and vals[s[i]] < vals[s[i + 1]]:\n            total -= vals[s[i]]\n        else:\n            total += vals[s[i]]\n    return total",
        "explanation": "If a numeral is followed by a larger numeral, subtract its value; otherwise, add it.",
        "pythonic_tip": "Mapping symbols to numbers with a dict and checking `i + 1 < len(s)` prevents index errors while evaluating prefix subtractions."
    },
    {
        "id": "py-029",
        "title": "Compress String (Run-Length Encoding)",
        "topic": "Strings",
        "difficulty": "Medium",
        "description": "Write a function `compress_string(s: str) -> str` that performs basic string compression using the counts of repeated characters.\nE.g., `'aabcccccaaa'` becomes `'a2b1c5a3'`.\nIf the compressed string is not smaller than original or if string is empty, return original string.",
        "starter_code": "def compress_string(s: str) -> str:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": ["aabcccccaaa"], "expected": "a2b1c5a3", "explanation": "Compressed version is shorter"},
            {"input": ["abcdef"], "expected": "abcdef", "explanation": "Compressed 'a1b1c1d1e1f1' is longer, return original"},
            {"input": [""], "expected": "", "explanation": "Empty string"}
        ],
        "hidden_test_cases": [
            {"input": ["aaaa"], "expected": "a4"},
            {"input": ["a"], "expected": "a"},
            {"input": ["aabbcc"], "expected": "aabbcc"}
        ],
        "solution": "def compress_string(s: str) -> str:\n    if not s:\n        return ''\n    parts = []\n    count = 1\n    for i in range(1, len(s)):\n        if s[i] == s[i - 1]:\n            count += 1\n        else:\n            parts.append(f\"{s[i-1]}{count}\")\n            count = 1\n    parts.append(f\"{s[-1]}{count}\")\n    compressed = ''.join(parts)\n    return compressed if len(compressed) < len(s) else s",
        "explanation": "Iterate through characters tracking current run count. Append formatted chunks `f\"{char}{count}\"` to a list and join them.",
        "pythonic_tip": "Always collect substrings into a list and call `''.join(parts)` instead of repeated string concatenations `s += ...`."
    },
    {
        "id": "py-030",
        "title": "Valid Parentheses",
        "topic": "Basic Algorithms",
        "difficulty": "Medium",
        "description": "Write a function `is_valid_parentheses(s: str) -> bool` that determines if input string of brackets `'()', '{}', '[]'` is valid.\nOpen brackets must be closed by the same type of bracket and in the correct order.",
        "starter_code": "def is_valid_parentheses(s: str) -> bool:\n    # Write your code here\n    pass\n",
        "sample_test_cases": [
            {"input": ["()[]{}"], "expected": True, "explanation": "Properly nested and closed"},
            {"input": ["(]"], "expected": False, "explanation": "Mismatched closing bracket"},
            {"input": ["([)]"], "expected": False, "explanation": "Incorrect closing order"}
        ],
        "hidden_test_cases": [
            {"input": [""], "expected": True},
            {"input": ["{[]}"], "expected": True},
            {"input": ["]"], "expected": False}
        ],
        "solution": "def is_valid_parentheses(s: str) -> bool:\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack",
        "explanation": "Use a stack (Python `list`). Push opening brackets; when encountering a closing bracket, pop the top element and verify it matches.",
        "pythonic_tip": "Python lists function directly as LIFO stacks with `.append()` and `.pop()` running in amortized O(1)."
    }
]
