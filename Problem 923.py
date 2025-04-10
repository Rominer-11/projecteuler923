import math
import itertools
from collections import defaultdict
from functools import lru_cache
from multiprocessing import Pool
import time
import os

LAST_CACHE_CLEAR = time.time()

# We are so back except not really

# --- Helper: Build board from staircase parameters ---

def build_board(a, b, k):
    R = k * a
    return [b * (k - (r // a)) for r in range(R)]

# --- Legal moves on a single board state ---

def legal_moves(board_state, turn):
    a, b, k, r, c = board_state
    L = build_board(a, b, k)
    R_total = len(L)
    moves = []
    if turn == 'R':
        # Only move one square to the right if within row bounds
        if c + 1 < L[r]:
            moves.append((a, b, k, r, c + 1))
    elif turn == 'D':
        # Only move one square down if within board bounds and if the next row has enough columns
        if r + 1 < R_total and c < L[r + 1]:
            moves.append((a, b, k, r + 1, c))
    return moves

# --- Memoized Disjunctive Sum Outcome ---

@lru_cache(None)
def disj_sum_outcome(state_tuple, turn):
    if all(not legal_moves(board, turn) for board in state_tuple):
        return False

    next_turn = 'D' if turn == 'R' else 'R'
    for i, board in enumerate(state_tuple):
        for new_board in legal_moves(board, turn):
            new_state = state_tuple[:i] + (new_board,) + state_tuple[i+1:]
            if not disj_sum_outcome(new_state, next_turn):
                return True
    return False

# --- Enumerate allowed staircases ---

def allowed_staircases(w):
    return [{'a': a, 'b': b, 'k': k} for a in range(1, w+1) for b in range(1, w+1) for k in range(1, w+1) if a + b + k <= w]

# --- Progress tracking callback ---

class ProgressTracker:
    def __init__(self, total):
        self.total = total
        self.count = 0
        self.last_reported = 0
        self.start_time = time.time()
    
    def update(self, result):
        self.count += 1
        
        progress = self.count / self.total
        if progress >= self.last_reported + 0.01 or self.count == self.total:
            elapsed = time.time() - self.start_time
            remaining = (elapsed / self.count) * (self.total - self.count) if self.count > 0 else 0
            print(f"Progress: {progress:.1%} ({self.count}/{self.total}), Elapsed: {elapsed:.1f}s, Remaining: {remaining:.1f}s")
            self.last_reported = progress

# --- Parallelized Winning Tuple Computation ---
# Modified check_winning_tuple to clear the cache every ~30 seconds

def check_winning_tuple(tup):
    global LAST_CACHE_CLEAR
    current_time = time.time()
    if current_time - LAST_CACHE_CLEAR > 30:
        # Clear the cache for disj_sum_outcome every ~30 seconds
        disj_sum_outcome.cache_clear()
        LAST_CACHE_CLEAR = current_time

    state = tuple((s['a'], s['b'], s['k'], 0, 0) for s in tup)
    return tup if disj_sum_outcome(state, 'R') else None

def count_winning_tuples(m, w):
    stairs = allowed_staircases(w)
    total_combinations = len(stairs) ** m
    print(f"Total combinations to check: {total_combinations}")
    
    tracker = ProgressTracker(total_combinations)
    
    with Pool() as pool:
        results = []
        # Using imap_unordered for better progress tracking
        for result in pool.imap_unordered(check_winning_tuple, itertools.product(stairs, repeat=m), chunksize=1000):
            tracker.update(result)
            if result is not None:
                results.append(result)
    
    winning_tuples = results
    return len(winning_tuples), stairs, winning_tuples

# --- Main Execution ---

if __name__ == '__main__':
    
    m = 3  # Number of boards 
    w = 9  # Weight bound
    
    print("Starting computation...")
    total, stairs, winning_tuples = count_winning_tuples(m, w)
    print(f"\nFor m = {m} and w = {w}:")
    print(f"  Number of allowed staircases: {len(stairs)}")
    print(f"  R(m, w) = {total}  (winning m-tuples for Right)")
    
    if m <= 3:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file_path = os.path.join(script_dir, "winning_staircases.txt")
        
        with open(output_file_path, "w") as f:
            for tup in winning_tuples:
                f.write(str(tup) + "\n")
        
        print(f"Winning tuples written to {output_file_path}")
