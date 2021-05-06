import argparse
import random
from multiprocessing import Pool
from typing import List

from networkx import symmetric_difference

from src import GreedySolver, HierarchicalSolver
from utils import ensure_substring_free


def create_dna_test(string: str, length: int, prob: float) -> List[str]:
    strings = []
    for i in range(len(string) - length + 1):
        if random.random() > prob:  # remove with probability prob
            strings.append(string[i:i + length])
    return ensure_substring_free(strings)


def create_slice_test(string: str, repetitions: int, min_len: int, max_len: int, shift: bool = False) -> List[str]:
    strings = []
    n = len(string)
    for _ in range(repetitions):
        if shift:
            new_pos = random.randrange(len(string))
            string = string[new_pos:] + string[:new_pos]

        pos = 0
        while n - pos > max_len:
            string_len = random.randint(min_len, max_len)
            strings.append(string[pos:pos + string_len])
            pos += string_len
        strings.append(string[pos:])

    return ensure_substring_free(strings)


def print_data(data, description: str, quiet: bool):
    if isinstance(data, list):
        ln = sum(map(len, data))
    else:
        ln = len(data)

    if quiet:
        print(description, ln)
    else:
        print(description + ':', data, 'len:', ln)


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

    just_input = subparsers.add_parser('input')
    just_input.add_argument(
        '--input',
        nargs='+',
        required=True,
        help='Input strings'
    )

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
    slices_from_random.add_argument(
        '--shift',
        action='store_true',
        help='Randomly shift every repetition'
    )

    args = parser.parse_args()
    if args.test_type == 'input':
        strings = args.input
    elif args.test_type == 'dna':
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
            ''.join(random.choices(args.alphabet, k=args.input_len)),
            args.repetitions, args.min_len, args.max_len, args.shift
        )
    else:
        raise ValueError(f'Unknown command {args.test_type}')
    if args.shuffle:
        random.shuffle(strings)
    print_data(strings, 'Instance', args.quiet)

    hg_gha = HierarchicalSolver(strings)
    hg_ca = HierarchicalSolver(strings)
    with Pool(processes=4) as pool:
        async_solvers = map(pool.apply_async, [
            GreedySolver(strings).greedy,
            GreedySolver(strings).t_greedy,
            hg_gha.gha,
            hg_ca.trivial_ca,
        ])
        solutions = list(map(lambda x: getattr(x, 'get')(), async_solvers))

    if args.check_correctness:
        for i, solution in enumerate(solutions):
            for string in strings:
                if string not in solution:
                    raise Exception(f'Solver #{i} produced incorrect solution: {string} in not in {solution}')
        if not args.quiet:
            print('Solutions are valid!')

    print_data(solutions[0], 'GREEDY', args.quiet)
    print_data(solutions[1], 'TGREEDY', args.quiet)
    print_data(solutions[2], 'GHA', args.quiet)
    print_data(solutions[3], 'CA + trivial', args.quiet)
    print('Collapsing Conjecture holds?',
          'Yes' if len(symmetric_difference(hg_ca.hg.graph, hg_gha.hg.graph).edges()) == 0 else 'No')


if __name__ == '__main__':
    main()
