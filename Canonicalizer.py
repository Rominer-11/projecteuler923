class Game:
    def __init__(self, L=None, R=None):
        # Left and right options; each should be an instance of Game.
        self.L = L if L is not None else []
        self.R = R if R is not None else []
    
    def __repr__(self):
        # Simple representation: if the game is just a number, then represent that number.
        # Otherwise, show the options.
        if self.is_number():
            return str(self.value())
        return "{" + ", ".join(repr(x) for x in self.L) + " | " + ", ".join(repr(x) for x in self.R) + "}"
    
    def is_number(self):
        # A game is a number if every left option is < every right option and its options are numbers
        # This is a heuristic check.
        if not self.L and not self.R:
            return True
        try:
            lv = max(x.value() for x in self.L) if self.L else float("-inf")
            rv = min(x.value() for x in self.R) if self.R else float("inf")
            return lv < rv
        except Exception:
            return False
    
    def value(self):
        # For numbers in canonical form, one can define the number as any value between the supremum
        # of left options and infimum of right options.
        if not self.is_number():
            raise ValueError("Game is not a number in canonical form")
        left_value = max((x.value() for x in self.L), default=float("-inf"))
        right_value = min((x.value() for x in self.R), default=float("inf"))
        # For simplicity, take the average (this works for games that turn out to be numbers).
        if left_value == float("-inf") and right_value == float("inf"):
            return 0  # The game { | } is 0.
        if left_value == float("-inf"):
            return right_value - 1
        if right_value == float("inf"):
            return left_value + 1
        return (left_value + right_value) / 2

def game_leq(G, H, depth=0, max_depth=10):
    """
    Naively decide whether G <= H using the Conway definition:
    G <= H if no left option of G is >= H and no right option of H is <= G.
    (This is a simplified version and can be tricky in general.)
    
    To keep recursion under control, we limit the recursion depth.
    """
    if depth > max_depth:
        # Fallback: try comparing numerical values if possible.
        try:
            return G.value() <= H.value()
        except Exception:
            # Otherwise, be conservative.
            return True

    # First, check left options of G.
    for gL in G.L:
        # If there is a left option gL with gL > H, then G > H.
        if not game_leq(H, gL, depth+1, max_depth):
            return False
    # Now, check right options of H.
    for hR in H.R:
        # If there is a right option hR with G > hR, then G > H.
        if not game_leq(hR, G, depth+1, max_depth):
            return False
    return True

def remove_dominated(options, compare):
    """
    Given a list of options and a comparison function 'compare'
    (which tests whether option x <= option y), remove any option that is dominated.
    For left options, if x is dominated by y (x <= y), then remove x.
    For right options, the test is reversed.
    """
    pruned = []
    for x in options:
        dominated = False
        for y in options:
            if x is not y and compare(x, y):
                dominated = True
                break
        if not dominated:
            pruned.append(x)
    return pruned

def canonicalize(G):
    """
    Recursively compute the canonical form of a game G.
    This involves:
     - Recursively canonicalizing all options,
     - Removing dominated options,
     - And removing reversible moves (a simplistic test).
    """
    # First, canonicalize the left and right options.
    new_L = [canonicalize(option) for option in G.L]
    new_R = [canonicalize(option) for option in G.R]
    
    # Remove dominated options.
    # For left options, we remove x if there is y such that x <= y.
    new_L = remove_dominated(new_L, game_leq)
    # For right options, we remove x if there is y such that y <= x.
    new_R = remove_dominated(new_R, lambda x, y: game_leq(y, x))
    
    # Remove reversible moves: For left options, if there is a right option (of that option)
    # that is <= the game itself, then x is reversible.
    pruned_L = []
    for option in new_L:
        reversible = False
        for r_option in option.R:
            if game_leq(r_option, G):
                reversible = True
                break
        if not reversible:
            pruned_L.append(option)
    new_L = pruned_L

    # And similarly for right options.
    pruned_R = []
    for option in new_R:
        reversible = False
        for l_option in option.L:
            if game_leq(G, l_option):
                reversible = True
                break
        if not reversible:
            pruned_R.append(option)
    new_R = pruned_R
    
    return Game(new_L, new_R)

# --- Example usage ---

if __name__ == '__main__':
    # Let’s test with some well-known simple games.
    # The game 0 is defined as { | }.
    zero = Game()
    
    # The game 1 is defined as {0 | }.
    one = Game(L=[zero])
    
    # The game -1 is defined as { | 0}.
    minus_one = Game(R=[zero])
    
    print("zero =", zero)
    print("one =", one)
    print("minus_one =", minus_one)
    
    # Construct a slightly more complicated game.
    # For example, define G = { -1, 0 | 0, 1 }.
    G = Game(L=[minus_one, zero], R=[zero, one])
    
    print("\nOriginal game G =", G)
    # Now canonicalize G.
    G_canon = canonicalize(G)
    print("Canonical form of G =", G_canon)
    
    # You can test comparisons:
    print("\nComparisons:")
    print("zero <= one?", game_leq(zero, one))
    print("minus_one <= zero?", game_leq(minus_one, zero))
    print("G <= one?", game_leq(G_canon, one))
