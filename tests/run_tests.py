#!/usr/bin/env python3
import unittest
import sys
import os
import time
import argparse

class KaceTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.verbosity = verbosity
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        self.success_count += 1
        if self.verbosity > 0:
            self.stream.writeln(f"\033[92m[PASS]\033[0m {test.shortDescription() or str(test)}")

    def addError(self, test, err):
        super().addError(test, err)
        self.error_count += 1
        if self.verbosity > 0:
            self.stream.writeln(f"\033[91m[ERROR]\033[0m {test.shortDescription() or str(test)}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.failure_count += 1
        if self.verbosity > 0:
            self.stream.writeln(f"\033[91m[FAIL]\033[0m {test.shortDescription() or str(test)}")

    def printErrors(self):
        if self.errors or self.failures:
            self.stream.writeln("\n" + "="*50)
            self.stream.writeln("\033[91mFAILED TESTS DETAILS\033[0m")
            self.stream.writeln("="*50)
            super().printErrors()


class KaceTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return KaceTestResult(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        self.stream.writeln("Running KACE Test Suite...\n")
        start_time = time.time()
        result = super().run(test)
        time_taken = time.time() - start_time

        self.stream.writeln("\n" + "="*50)
        self.stream.writeln("RESULT:")
        
        total = result.success_count + result.failure_count + result.error_count
        self.stream.writeln(f"\033[92m{result.success_count} PASSED\033[0m")
        if result.failure_count > 0:
            self.stream.writeln(f"\033[91m{result.failure_count} FAILED\033[0m")
        if result.error_count > 0:
            self.stream.writeln(f"\033[91m{result.error_count} ERRORS\033[0m")
            
        self.stream.writeln(f"\nTime taken: {time_taken:.2f}s")
        self.stream.writeln("="*50)
        return result


def main():
    parser = argparse.ArgumentParser(description="KACE Automated Test Runner")
    parser.add_argument("--verbose", action="store_true", help="Show detailed test output")
    parser.add_argument("--board", type=str, help="Run validation for a specific board (Hardware testing)")
    parser.add_argument("--all-boards", action="store_true", help="Run validation for all known boards")
    parser.add_argument("--update-snapshots", action="store_true", help="Update golden regression snapshots")
    args = parser.parse_args()

    # Pass args via env vars for tests to read
    if args.update_snapshots:
        os.environ['KACE_UPDATE_SNAPSHOTS'] = '1'
    if args.board:
        os.environ['KACE_TEST_BOARD'] = args.board
    if args.all_boards:
        os.environ['KACE_TEST_ALL_BOARDS'] = '1'

    verbosity = 2 if args.verbose else 1
    # Even in non-verbose mode, our custom runner will print PASS/FAIL per test if verbosity > 0

    loader = unittest.TestLoader()
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add parent directory to sys.path so we can import 'core', 'firmware', etc.
    sys.path.insert(0, os.path.dirname(test_dir))

    suite = loader.discover(start_dir=test_dir, pattern="test_*.py")

    runner = KaceTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    sys.exit(not result.wasSuccessful())


if __name__ == "__main__":
    main()
