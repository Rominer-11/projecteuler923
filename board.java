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
	private char[][] board;

	public board(int a, int b, int k)
	{
		this.a = a;
		this.b = b;
		this.k = k;

		this.board = new char[a+1][b+1];

		this.init();
	}

	/**
	 * Initializes board to staircase form
	 */
	public void init()
	{
		int stepWidth = b / k;
		int stepHeight = a / k;

		for (int step = 0; step < k; step++)
		{
			for (int row = 0; row < stepHeight; row++)
			{
				printBoard();
				board[row][board.length - (step * stepWidth) - 1] = 'o';
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
