# Memory Simulator

This project is a memory simulator implemented using Python and Tkinter. It allows users to configure cache levels, initialize memory components, and simulate cache behavior with various policies (Random, LRU, FIFO).

## Features

- Select and configure different cache levels (L1, L2, L3).
- Initialize caches with specified sizes, block counts, and access times.
- Validate memory configuration.
- Simulate memory access with random or user-entered hexadecimal addresses.
- Display cache contents and monitor hit/miss rates.
- Choose between different cache replacement policies: Random, LRU, FIFO.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Rania483/memory-simulator.git
    cd memory-simulator
    ```

2. Ensure you have Python installed. This project is compatible with Python 3.x.

3. Install the required dependencies (Tkinter is included with Python):
    ```bash
    pip install tk
    ```

## Usage

1. Run the `memory_simulator.py` script:
    ```bash
    python memory_simulator.py
    ```

2. Follow the GUI instructions to:
    - Select cache levels.
    - Initialize cache sizes, block counts, and access times.
    - Configure DRAM, virtual memory, and disk sizes.
    - Choose a cache implementation policy.
    - Generate or enter hexadecimal memory addresses for simulation.

## Example

Here's an example of how to use the memory simulator:

1. Select cache levels (L1, L2, L3).
2. Initialize cache and memory values.
3. Choose a cache replacement policy.
4. Generate or enter memory addresses to see cache behavior and statistics.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

[Rania](https://github.com/Rania483)

## Acknowledgments

- Thanks to the open-source community for the resources and tools that made this project possible.
