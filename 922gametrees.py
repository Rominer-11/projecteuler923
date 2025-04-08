from anytree import Node, RenderTree, PreOrderIter
from anytree.exporter import DotExporter
from collections import deque

def build_board(a, b, k):
    R = k * a
    return [b * (k - (r // a)) for r in range(R)]

def legal_moves(board_state, turn):
    a, b, k, r, c = board_state
    L = build_board(a, b, k)
    R_total = len(L)
    moves = []
    if turn == 'R':
        moves.extend((a, b, k, r, c_new) for c_new in range(c+1, L[r]))
    elif turn == 'D':
        moves.extend((a, b, k, r_new, c) for r_new in range(r+1, R_total) if c < L[r_new])
    return moves

def format_state(state, turn):
    return f"{turn}: " + " | ".join([f"{s[3]},{s[4]}" for s in state])

def generate_game_tree(state_tuple, turn, max_depth=4):
    root = Node(format_state(state_tuple, turn), state=state_tuple, turn=turn, depth=0)
    queue = deque([root])

    while queue:
        current = queue.popleft()
        if current.depth >= max_depth:
            continue

        next_turn = 'D' if current.turn == 'R' else 'R'
        for i, board in enumerate(current.state):
            for move in legal_moves(board, current.turn):
                new_state = current.state[:i] + (move,) + current.state[i+1:]
                label = format_state(new_state, next_turn)
                child = Node(label, parent=current, state=new_state, turn=next_turn, depth=current.depth + 1)
                queue.append(child)

    return root

def main():
    board = (2, 2, 2, 0, 0)
    board2 = (2, 2, 2, 0, 0)
    state = (board,board2)
    max_depth = 60

    print("Building game tree...")
    root = generate_game_tree(state, 'R', max_depth=max_depth)

    print("\nText Visualization:\n")
    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name}")

    # Export to Graphviz (creates .dot file or .png if you have Graphviz installed)
    DotExporter(root).to_dotfile("game_tree.dot")
    print("\nDot file exported to 'game_tree.dot'")
    print("To render a PNG: run `dot -Tpng game_tree.dot -o game_tree.png`")

if __name__ == '__main__':
    main()
