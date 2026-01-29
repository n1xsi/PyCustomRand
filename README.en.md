<div align="center">

  # PyCustomRand
  
  ![Python](https://custom-icon-badges.demolab.com/badge/Python-3.8+-blue?logo=pythonn)
  [![Last Commit](https://img.shields.io/github/last-commit/n1xsi/pycustomrand.svg)](https://github.com/n1xsi/pycustomrand/commits/main)
  [![Run Tests](https://github.com/n1xsi/PyCustomRand/actions/workflows/python-app.yml/badge.svg)](https://github.com/n1xsi/PyCustomRand/actions/workflows/python-app.yml)

</div>

🌐 **Languages:**
🇷🇺 <a href="README.md">Русский</a> | *🇬🇧 English*

<br>

**PyCustomRand** is a Python library for generating **pseudo-random numbers**, based on an algorithm that utilizes system time with nanosecond precision.

This author's project was created to study algorithms and alternative approaches to random number generation and rounding.
I was not satisfied with the fact that Python's standard `random` module generates insufficiently random numbers (*especially during multiple sequential generations*), and the built-in `round` module rounds
numbers rather "roughly" ( *`round(1.5)` = 2 and at the same time `round(2.5)` = 2* ). Therefore, I decided to write *my own* library for pseudo-random number generation — simpler and with higher entropy.

> [!WARNING]
> PyCustomRand is *currently* **not** a cryptographically secure library and is **not intended** for use in security systems!
> Use the [secrets](https://docs.python.org/3/library/secrets.html#module-secrets) module for such purposes.

## 📌 Why use this library when Python has its own `random` and `round`?
PyCustomRand was written as an alternative to these two built-in modules. Here are the main features and capabilities of the library:

*   The library is **simpler** to understand — the entire code is commented, lightweight, and clear. The PRNG (Pseudo-Random Number Generator) implementation is based on a *simple* algorithm using system time, making the library easy to customize, extend, or adapt to your needs.
*   In most cases, PyCustomRand produces a more *"entropic"* result during sequential generations compared to the built-in `random` module.
    * <details>
        <summary>📊 Comparison with diagrams</summary>
        
        PyCustomRand demonstrates **173%** higher distribution consistency compared to the standard `random` library in tests with **1,000,000** iterations.

        <img src="https://i.imgur.com/qxYdxmD.png">
        
        The data for the diagram was obtained using the built-in diagnostics module (`check_distribution`). The results showed that PyCustomRand had a maximum deviation **2.7 times** lower than the standard `random` (0.0267% vs 0.0730%).

        <table align="center" style="border-collapse: collapse;">
          <!-- Header Row -->
          <tr>
            <th align="center" style="font-family: sans-serif">
              PyCustomRand
            </th>
            <th align="center" style="font-family: sans-serif">
              Python Built-in
            </th>
          </tr>
          <!-- Image Row -->
          <tr>
            <td align="center" width="50%">
                <img src="https://i.imgur.com/kH26JEO.jpeg" width="100%" alt="PyCustomRand">
            </td>
            <td align="center" width="50%">
                <img src="https://i.imgur.com/LdFoREN.jpeg" width="100%" alt="Python Built-in">
            </td>
          </tr>
        </table>
      </details>
*   The library includes all the most important functions from the [original](https://docs.python.org/3/library/random.html) Python library, but improved and simplified in places (e.g., `random_integer` can return a generated result divisible by a specified number within the range; the result of `random_float` can be rounded, etc.).
    * <details>
        <summary>📑 List of functions</summary>
      
        *   Integer generation (`gen_random_number`, `randrange`, `random_integer`).
        *   Float generation (`random`, `random_float`).
        *   Statistical distributions: Normal (Gauss), Triangular, Exponential, Binomial.
        *   Sequence tools: random element selection (`choice`), weighted selection (`choices`), shuffling (`shuffle`), and unique element selection (`sample`).
        *   PRNG sequence initialization ("seeding") (`set_seed`, `_get_next_seed_state`).
      </details>
*   The library also includes additional utilities useful for web/game development: generation of UUID v4, random HEX colors (e.g., `#ff05a1`), random bytes, random boolean values (`True`/`False`) with customizable probability.
*   It features a custom rounding module — `true_round`. This function rounds numbers using the standard mathematical method (0.5 is always rounded up by magnitude) and also fixes floating-point errors (e.g., the "2.675 problem").
*   The code is covered by unit tests (as indicated by the badge at the beginning of the README), and it has a built-in diagnostics module (`check_distribution`) allowing you to check the uniformity of the generator's distribution at any time.

However, the project does have some downsides:
*   Time-based randomness requires a small wait time (`time.sleep()` for 0.1 microseconds), so for massive iterations, PyCustomRand will be slightly slower than the built-in `random` module.
*   Some functions in PyCustomRand (selection, distributions) are written so simply that they might not be fully optimized for massive samples (plus the accumulating micro-wait mentioned above).

## 📦 Installation
Installation is done via the standard Python package manager:
```bash
pip install pycustomrand
```

<details>
  <summary>➕ Alternative installation methods</summary>
  If you encounter issues with the Python package manager or other errors, PyCustomRand can be installed in other ways:
  
  <br>

  * Download the package from the official PyPI page:
  https://pypi.org/project/pycustomrand/#files

  * Download the package **directly** from the *Releases* section:
  https://github.com/n1xsi/PyCustomRand/releases

  * Clone the repository:
  ```bash
  git clone https://github.com/n1xsi/PyCustomRand.git
  ```
</details>


## 📚 Documentation
Below is a description of all available library functions with examples. For convenience, they can be imported directly from the package (`from pycustomrand import FUNC_NAME`).

### 1. State Management (Seeding)
Initializing the generator allows for reproducible sequences (e.g., for tests or saving world generation).

*   `set_seed(seed=None)`
    Sets the initial state of the generator.
    *   `seed`: Any object that can be converted to a string — number/string/list, etc. If `None`, the seed is reset, and system time (random sequence) is used.

*   `_get_next_seed_state(current_seed)`
    Internal function to update the seed state (LCG algorithm).

<details>
    <summary>🧩 Examples 1</summary>
  
```python
from pycustomrand import set_seed, random

print(random())  # Random number, e.g., 0.3730190220377659

set_seed("test")  # Set seed for testing
print(random())   # The first result after setting seed "test" will ALWAYS be 0.1647608190844912
print(random())   # The second result will also ALWAYS be 0.943716375817365 (via _get_next_seed_state)

set_seed()       # Reset seed
print(random())  # Random number, e.g., 0.2458062256227575
```

</details>

### 2. Integers
*   `gen_random_number(length=1)`
    Generates a number of the specified `length` by concatenating random digits.

*   `randrange(start, stop=None, step=1)`
    Full analog of standard `range` — returns an element from `range(start, stop, step)`. The upper bound is **exclusive**. Can be called with a single argument.

*   `random_integer(start, end, step=1)` (alias: `randint`)
    Returns a random integer `N` such that `start <= N <= end` (**both bounds included**).
    *   `step`: Generation step. For example, `step=2` will return only even (or odd) numbers. Optional argument.

<details>
    <summary>🧩 Examples 2</summary>
  
```python
from pycustomrand import gen_random_number, randrange, random_integer

print(gen_random_number(5))  # Random number with length 5, e.g., 92103

print(randrange(10))        # Random number from [0, 10)
print(randrange(1, 10))     # Random number from [1, 10)
print(randrange(0, 10, 2))  # Random even number from [0, 10)

print(random_integer(1, 10))     # Random integer from [1, 10]
print(random_integer(0, 10, 2))  # Random even integer from [0, 10]

# randint is an alias for random_integer
# randint(1, 10) is equivalent to random_integer(1, 10)
```

</details>

### 3. Real Numbers (Floats)
*   `random()`
    Returns a random `float` in the range `[0.0, 1.0)`.

*   `random_float(start, end, digits=None)`
    Returns a `float` in the range `[start, end)` or `[start, end]` depending on rounding (if `digits` is present).
    *   `start`, `end`: Start and end of the range, can be integers or floats.
    *   `digits`: If specified, the result is rounded to this number of decimal places using `true_round`.

<details>
    <summary>🧩 Examples 3</summary>
  
```python
from pycustomrand import random, random_float

print(random())  # Random number in [0, 1), e.g., 0.2260351121787103

print(random_float(0, 10))            # Random float in [0, 10), e.g., 4.014874483651235
print(random_float(0, 10, digits=3))  # Same, but rounded to 3 decimals, e.g., 6.722
```

</details>

### 4. Sequences
*   `choice(array)`
    Returns one random element from the sequence.

*   `choices(array, k, weights=None)`
    Returns a list of `k` random elements with replacement (repetition allowed).
    *   `weights`: A list of weights (probabilities) for each element (corresponding by index). If `None`, all elements are considered equal.

*   `shuffle(array)`
    Shuffles a mutable sequence (list) in-place.

*   `sample(array, k, counts=None)`
    Returns a list of `k` **unique** random elements.
    *   `counts`: A list with the count of each element in the array (corresponding by index).

<details>
    <summary>🧩 Examples 4</summary>
  
```python
from pycustomrand import choice, choices, shuffle, sample

array = ["apple", "banana", "cherry", "orange"]

print(choice(array))  # Random element, e.g., "cherry"

print(choices(array, k=2))  # List of k random elements, e.g., ['apple', 'cherry']
print(choices(array, k=2, weights=[1, 2, 3, 4]))  # Weighted selection, e.g., ['orange', 'banana']
# "orange" (weight 4) will appear 4x more often than "apple" (weight 1)

shuffle(array)  # Shuffles in-place
print(array)    # e.g., ['cherry', 'banana', 'apple', 'orange']

print(sample(array, k=2))  # List of k unique elements, e.g., ['cherry', 'apple']
print(sample(array, k=2, counts=[1, 2, 3, 4]))  # Unique selection with counts, e.g., ['banana', 'orange']
# "orange" (with the number in the array of 4) will produce four times more than "apple" (the number in the array of 1)
```

</details>

### 5. Probabilistic Distributions
These functions are used to model real-world processes (physics, economics, games).

*   `triangular(low=0.0, high=1.0, mode=None)` — Triangular distribution.
    Generates a number in `[low, high]`, but the number `mode` (peak) appears most often.
    Used in simple modeling. *Example*: Sword damage from 5 to 15, but usually hits 10 — `triangular(5, 15, 10)`.

*   `gauss(mu=0.0, sigma=1.0)` — Normal distribution (Gaussian Bell).
    Most values group around the mean (`mu`), and `sigma` (standard deviation) shows the spread.
    Used for natural phenomena. *Examples*: Human height, IQ, measurement errors, the spread of bullets when firing.

*   `expovariate(lambd=1.0)` — Exponential distribution.
    Describes the time between events in a Poisson process. Small values appear often, large ones rarely (long tail).
    Used in timers. *Examples*: Time between bus arrivals, monster spawn times (they usually come up often, but sometimes there are long lulls  ).
    *   `lambd`: Event intensity (must be > 0).

*   `binomialvariate(n=1, p=0.5)` — Binomial distribution (alias: `binomial`).
    Number of successes in a sequence of `n` independent trials with success probability `p`.
    *Example*: Number of heads in 10 coin flips — `binomialvariate(n=10, p=0.5)`.

<details>
    <summary>🧩 Examples 5</summary>
  
```python
from pycustomrand import triangular, gauss, expovariate, binomialvariate

print(triangular(low=0.0, high=1.0, mode=0.5))  # A random floating-point number from a triangular distribution (range [0.0, 1.0])
# The most common value is ±0.5, for example: 0.6508330793068139

print(gauss(mu=0.0, sigma=1.0))  # A random floating-point number from a normal "bell" distribution (total range 0.0 ±~3.0)
# The most common value is 0.0 ± 1.0, for example: 1.0665809173007805 or -1.650128903962443

print(expovariate(lambd=1.0))  # A random floating-point number from an exponential distribution (total range 0.0 ±~4.0)
# The lowest value from 0.0 to 1.0 is most often found, for example: 0.405175514533143

print(binomialvariate(n=10, p=0.5))  # A random number from a binomial distribution (range [0, 10]), for example: 5
# The lower the probability of p, the more often a number from the first half of the range [0, 10] will fall out, and the higher the number from the second half.

# binomial is an alias for binomialvariate, works with "import pycustomrand", "from pycustomrand import *" or "from pycustomrand import binomial"
# binomial(n=10, p=0.5)) is equivalent to binomialvariate(n=10, p=0.5)
```

</details>

### 6. Utilities (Extras)
*   `random_bytes(count)`: Generates `count` random bytes.
*   `random_uuid4()`: Generates a unique identifier (UUID v4).
*   `random_color_hex()`: Random color in HEX format.
*   `random_bool(true_chance=0.5)`: Returns True or False with probability `true_chance`.

<details>
    <summary>🧩 Examples 6</summary>
  
```python
from pycustomrand import random_bytes, random_uuid4, random_color_hex, random_bool

print(random_bytes(10))    # e.g., b'\x8b\x91\x19\xe42\xcd\x80\x82b\xba'

print(random_uuid4())      # e.g., '0e1d2eeb-1627-4cfa-8130-afe74e1c5ce9'

print(random_color_hex())  # e.g., '#0ca3e7'

print(random_bool())       # e.g., True
```

</details>


### 🎯 About the `true_round` Module
This module solves the "Banker's Rounding" problem in Python 3, where `round(x.5)` rounds to the nearest even number.
`true_round` uses **true mathematical rounding** (hence the name).

For convenience, the module can be imported directly (`from pycustomrand import true_round`).

| Number | Standard `round()` | PyCustomRand `true_round()` | Note |
| :--- | :---: | :---: | :--- |
| **2.5** | 2 | **3** | Mathematical rounding (0.5 → up) |
| **3.5** | 4 | **4** | Matches |
| **2.675** (to 2 digits) | 2.67 | **2.68** | Fixes Floating Point Error |
| **1.005** (to 2 digits) | 1.0  | **1.01** | Correct boundary handling |
| **0.00049** (to 3 digits) | 0.0 | **0.001** | Precision with small numbers |


## 🧪 Testing and Diagnostics
PyCustomRand provides internal tools to check library functionality and entropy quality.

### 1. Running All Unit Tests
To ensure all functions work correctly, run the built-in tests from the repository root:

```bash
python -m unittest discover tests
```

### 1.1. Running specific module tests
Run tests for the random generator:
```bash
python -m unittest tests/test_random.py
```

Run tests for the rounding module:
```bash
python -m unittest tests/test_round.py
```

### 1.2. Running a specific test case
If you are modifying the library, and you constantly fail to check any one specific test, then you don't have to waste time running all the tests - you just need to run one specific test of a specific module, for example:
```python
from tests.test_round import TestTrueRound
import unittest

# Run only "test_negative_numbers"
unittest.main(defaultTest='TestTrueRound.test_negative_numbers')
```

### 2. Distribution Check (Diagnostics)
The library includes the `@check_distribution` decorator (`pycustomrand.diagnostics`). It visually evaluates the uniformity of number generation. Example:

```python
from pycustomrand.diagnostics import check_distribution
import pycustomrand as pcr

# The decorator runs the function 100,000 times and splits results into 20 buckets
@check_distribution(count=100_000, buckets=20)
def check_float_random():
    return pcr.random()

if __name__ == "__main__":
    check_float_random()
```

The console result shows:
*   Current iteration (every 5 seconds);
*   Total generation time;
*   Table with hit counts per "bucket";
*   Percentage deviation from ideal distribution;
*   Verdict: "Excellent uniform distribution" or a warning about bias.

<details>
  <summary>📊 Example of diagnostic result</summary>
  <div align="center">
    <img src="https://i.imgur.com/WUzDRfY.png" width="40%">
  </div>
</details>


## 📂 Repository Structure
The project has the following file structure:

```
PyCustomRand/                # Repo root
├── .github/
│   └── workflows/
│       └── python-app.yml   # GH Actions config: auto-run tests on Push/PR
│
├── pycustomrand/            # Package source code
│   ├── __init__.py            # Entry point: package init and aliases
│   ├── custom_round.py        # Math rounding algorithm (true_round)
│   ├── diagnostics.py         # Decorator for distribution checking
│   └── random_generator.py    # Library core: PseudoRandom class and logic
│
├── tests/                   # Unit Tests
│   ├── __init__.py            # Empty file
│   ├── test_random.py         # Tests for generator, seeds, ranges, utils
│   └── test_round.py          # Tests for rounding correctness
│
├── .gitignore               # Git exclusion rules
├── LICENSE                  # MIT License text
├── pyproject.toml           # Build config for PyPI
├── README.en.md             # Project documentation (English)
└── README.md                # Project documentation (Russian)
```

## 🤝 Contribution
Any help in developing the library is welcomed. If you have ideas for improving algorithms, optimizing code, or have found a bug, feel free to create an Issue/Pull Request.

**How to contribute:**
1.  **Fork** the repository;
2.  Create a new branch for your feature (`git checkout -b feature/SomeFeature`);
3.  Make changes;
4.  **Run tests** to ensure nothing is broken:
    ```bash
    python -m unittest discover tests
    ```
5.  Push changes (`git push origin feature/SomeFeature`);
6.  Open a **Pull Request**.

## 📄 License
This project is open-source software distributed under the **MIT License**.

    Copyright © 2025 Ivan (n1xsi)

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions: ...

The full license text is available in the [LICENSE](LICENSE) file.
