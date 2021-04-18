import argparse
import random
from multiprocessing import Pool
from typing import List

from src import GreedySolver, HierarchicalSolver
from utils import ensure_substring_free


def create_dna_test(string: str, length: int, prob: float) -> List[str]:
    strings = []
    for i in range(len(string) - length + 1):
        if random.random() > prob:  # remove with probability prob
            strings.append(string[i:i + length])
    return ensure_substring_free(strings)


def create_slice_test(string: str, repetitions: int, min_len: int, max_len: int) -> List[str]:
    strings = []
    n = len(string)
    for _ in range(repetitions):
        pos = 0
        while n - pos > max_len:
            string_len = random.randint(min_len, max_len)
            strings.append(string[pos:pos + string_len])
            pos += string_len

    return ensure_substring_free(strings)


def print_data(data, description: str, quiet: bool):
    if isinstance(data, list):
        ln = sum(map(len, data))
    else:
        ln = len(data)

    if quiet:
        print(description, ln)
    else:
        print(description, data, 'len:', ln)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--check-correctness',
        action='store_true',
        help='check the correctness of solution'
    )
    parser.add_argument(
        '--shuffle',
        action='store_true',
        help='shuffle input sequence'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='print only lengths'
    )
    subparsers = parser.add_subparsers(dest='test_type')

    dna_from_given = subparsers.add_parser('dna')
    dna_from_given.add_argument(
        '--input',
        required=True,
        help='Input DNA string',
    )
    dna_from_given.add_argument(
        '--len',
        required=True,
        type=int,
        help='Size of a single string'
    )
    dna_from_given.add_argument(
        '--prob',
        required=True,
        type=float,
        help='Probability of elimination'
    )

    dna_from_random = subparsers.add_parser('random_dna')
    dna_from_random.add_argument(
        '--alphabet',
        required=False,
        help='Alphabet for strings in problem',
        default='AGCT'
    )
    dna_from_random.add_argument(
        '--input-len',
        required=True,
        type=int,
        help='Size of an input string'
    )
    dna_from_random.add_argument(
        '--len',
        required=True,
        type=int,
        help='Size of a single string'
    )
    dna_from_random.add_argument(
        '--prob',
        required=True,
        type=float,
        help='Probability of elimination'
    )

    from_random = subparsers.add_parser('random')
    from_random.add_argument(
        '--alphabet',
        required=False,
        help='Alphabet for strings in problem',
        default='AGCT'
    )
    from_random.add_argument(
        '--amount',
        required=True,
        type=int,
        help='Amount of strings in input'
    )
    from_random.add_argument(
        '--len',
        required=True,
        type=int,
        help='Size of a single string'
    )

    slices_from_given = subparsers.add_parser('slice_dna')
    slices_from_given.add_argument(
        '--input',
        required=True,
        help='Input DNA string',
    )
    slices_from_given.add_argument(
        '--repetitions',
        required=True,
        type=int,
        help='Amount of blocks'
    )
    slices_from_given.add_argument(
        '--min-len',
        required=True,
        type=int,
        help='Min size of a single string'
    )
    slices_from_given.add_argument(
        '--max-len',
        required=True,
        type=int,
        help='Max size of a single string'
    )

    slices_from_random = subparsers.add_parser('slice_random')
    slices_from_random.add_argument(
        '--alphabet',
        required=False,
        help='Alphabet for strings in problem',
        default='01'
    )
    slices_from_random.add_argument(
        '--input-len',
        required=True,
        type=int,
        help='Size of an input string'
    )
    slices_from_random.add_argument(
        '--repetitions',
        required=True,
        type=int,
        help='Amount of blocks'
    )
    slices_from_random.add_argument(
        '--min-len',
        required=True,
        type=int,
        help='Min size of a single string'
    )
    slices_from_random.add_argument(
        '--max-len',
        required=True,
        type=int,
        help='Max size of a single string'
    )

    args = parser.parse_args()
    if args.test_type == 'dna':
        strings = create_dna_test(args.input, args.len, args.prob)
    elif args.test_type == 'random_dna':
        strings = create_dna_test(''.join(random.choices(args.alphabet, k=args.input_len)), args.len, args.prob)
    elif args.test_type == 'random':
        strings = ensure_substring_free(
            [''.join(random.choices(args.alphabet, k=args.len)) for _ in range(args.amount)]
        )
    elif args.test_type == 'slice_dna':
        strings = create_slice_test(args.input, args.repetitions, args.min_len, args.max_len)
    elif args.test_type == 'slice_random':
        strings = create_slice_test(
            ''.join(random.choices(args.alphabet, k=args.input_len)), args.repetitions, args.min_len, args.max_len
        )
    else:
        raise ValueError(f'Unknown command {args.command}')
    if args.shuffle:
        random.shuffle(strings)
    print_data(strings, 'Instance', args.quiet)

    with Pool(processes=3) as pool:
        async_solvers = map(pool.apply_async, [
            GreedySolver(strings).greedy,
            GreedySolver(strings).t_greedy,
            HierarchicalSolver(strings).gha,
        ])
        greedy, t_greedy, gha = map(lambda x: getattr(x, 'get')(), async_solvers)

    if args.check_correctness:
        for i, solution in enumerate([greedy, t_greedy, gha]):
            for string in strings:
                if string not in solution:
                    raise Exception(f'Solver #{i} produced incorrect solution: {string} in not in {solution}')
        print('Solutions are valid!')

    print_data(greedy, 'GREEDY', args.quiet)
    print_data(t_greedy, 'TGREEDY', args.quiet)
    print_data(gha, 'GHA', args.quiet)


if __name__ == '__main__':
    main()
