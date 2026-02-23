# American Flag Star Generator

This generator calculates the optimal geometric arrangement of an arbitrary number of stars $N$ and creates a true-proportion SVG of the American flag featuring the calculated star arrangement.

## Features

- **Algorithmic Layout Calculation**:
  Finds the best visual layout for any number of stars. The algorithm searches for rectangular grid arrays (like the 48-star flag's 6x8 configuration) as well as staggered, interlocking rows (like the current 50-star flag's interleaved 6 and 5 stars).
- **Correct Proportions**:
  The flag dimensions follow strict government specifications for the hoist, fly, canton (the blue field), and stripe widths.
- **Vector Output**:
  Draws mathematically precise 5-pointed stars directly to a scalable `.svg` file.

## Usage

Simply run the script with Python 3 with the desired number of stars as the first argument:

```bash
python3 flag_maker.py <number_of_stars>
```

For example, to generate the standard 50-star flag:

```bash
python3 flag_maker.py 50
```

To create a flag with 63 stars:

```bash
python3 flag_maker.py 63
```

By default, if no number is supplied, it assumes $N=50$.
The script will output the structural pattern it used to the terminal and generate a `bandera.svg` vector image file in the same directory.

## How It Works

The magic of the script happens inside the `find_best_pattern(n)` function. It iterates over all possible combinations of rows and columns, testing both:

1. Standard grid layouts (e.g. 5x5 for 25 stars).
2. Staggered interlocking arrays (where adjacent rows differ by exactly 1 star, e.g. rows of 6, then 5, then 6...).

For every valid configuration:
- It checks the aspect ratio of the star cluster block against the aspect ratio of the blue canton (which is roughly ~1.411 to 1). The algorithm scores each pattern based on how perfectly it avoids empty, unbalanced blue space.
- The layout is then parsed and the individual stars are evenly spaced across the X / Y coordinates within the SVG canvas.
