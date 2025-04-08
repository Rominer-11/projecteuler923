/**
 * Board class
 * @author August Cho
 * @version 2025-03-25
 */
public class board
{
	private int a;
	private int b;
	private int k;
	private int[][] board;

	public board(int a, int b, int k)
	{
		this.a = a;
		this.b = b;
		this.k = k;

		this.board = new int[a * k][b * k];

		this.init();

		this.printBoard();
	}

	/**
	 * Initializes board to staircase form
	 */
	public void init()
	{
		int step = 0;

		for (int row = 0; row < board.length; row++)
		{
			for (int col = 0; col < (board[0].length - (step * b)); col++)
			{
				board[row][col] = 1;
			}
			if ((row + 1) % a == 0)
			{
				step++;
			}
		}
	}

	public void printBoard()
	{
		for (int row = 0; row < board.length; row++)
		{
			for (int col = 0; col < board[0].length; col++)
			{
				System.out.print(board[row][col] + " ");
			}
			System.out.print("\n");
		}
		System.out.print("\n");
	}
}
