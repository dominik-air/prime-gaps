import argparse
import primesieve
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from functools import wraps
from timeit import default_timer as timer
from typing import Dict, Tuple

# a reasonable prime bound in terms of computation time
MAX_PRIME = int(100 * 10e9)
# type hints
n_gaps = int
gap_size = int
gap_histogram = Dict[gap_size, n_gaps]


def parser_input() -> Tuple[int, int]:
    """Takes in the user input from the command line.

    Returns:
        tuple: First element is the number of frames and the latter is the prime number iteration step.
    """
    parser = argparse.ArgumentParser(description="Creates a gif of prime gaps log-plot. "
                                                 "The number of primes being taken into consideration is frames * i.")
    parser.add_argument("--frames", default=100, type=int, help="The number of frames of the output gif. Default = 100")
    parser.add_argument("--i", default=1000, type=int, help="Prime iteration step. Default = 1000")

    args = parser.parse_args()

    return args.frames, args.i


def time_it(func: callable) -> callable:
    """Decorator used to time functions.

    Args:
        func (callable): The function which will be timed.

    Returns:
        callable: Wrapper returning a tuple of the original function func return values and the computation time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timer()
        result = func(*args, **kwargs)
        end = timer()
        return result, end-start
    return wrapper


def calc_gaps(n: int) -> gap_histogram:
    """Calculates prime number gaps histogram from 0 up to nth prime number.

    Args:
        n (int): The nth prime number to which the function will calculate gaps.

    Returns:
        gap_histogram: Dictionary mapping gap sizes with their number of occurrences.
    """
    it: primesieve.Iterator = primesieve.Iterator()
    gap_histogram_data: dict = {}
    prime: int = it.next_prime()
    for i in range(int(n)):
        prev = prime
        prime = it.next_prime()
        gap = prime - prev
        if gap_histogram_data.get(gap):
            gap_histogram_data[gap] += 1
        else:
            gap_histogram_data[gap] = 1
    return gap_histogram_data


def gaps_generator(step: int, n: int = MAX_PRIME) -> gap_histogram:
    """Generates prime number gaps histogram from 0 to the nth prime number by a given step.

    Args:
        step (int): The prime number iteration step.
        n (int): The nth prime number to which the generator will generate gaps.

    Yields:
        gap_histogram: Dictionary mapping gaps sizes with their number of occurrences.
    """
    i: int = 0
    while i <= int(n):
        yield calc_gaps(i)
        i += step


@time_it
def main():
    def animate(i):
        """Animation helper function"""

        data = next(gaps_gen)
        xs = data.keys()
        ys = data.values()

        ax.clear()
        ax.scatter(xs, ys)

        plt.yscale('log')
        plt.xlabel('gap length')
        plt.ylabel('# of gaps')

        # gets an appropriate number of primes repr
        n_primes = i * prime_i
        if n_primes >= int(10e5):
            n_primes = str(round(n_primes / int(10e5), 2)) + 'M'
        elif n_primes >= int(10e2):
            n_primes = str(round(n_primes / int(10e2))) + 'k'

        plt.title(f'prime gap line for {n_primes} primes')

        # prints the progress
        print(f'{100*i/frames}%')

    # figure setup
    plt.style.use('ggplot')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # get data from user via cmd
    frames, prime_i = parser_input()
    # prime generator init
    gaps_gen = gaps_generator(prime_i)
    # performs the animation
    ani = animation.FuncAnimation(fig, animate, frames=frames, interval=10)
    ani.save(f'gap_{frames}frames_{prime_i}i.gif', writer='imagemagick')


if __name__ == '__main__':
    _, t = main()
    print(f'done in {round(t, 2)}s')
