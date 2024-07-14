defmodule MarsRover do
  @moduledoc """
  For Multiverse

  This is a solution to the problem documented in the following file:
  Multiverse engineering take-home challenge (2).pdf

  Accepts input from STDIN and outputs results to STDOUT.

  Author: Iain Argent (iainargent007@gmail.com)
  """

  @doc """
  update the rover's position from its
  last location and the direction it was facing
  returns a pair of integers with the new position
  """
  def go_forward(xloc, yloc, dir) do
    case dir do
      ~c"N" -> [xloc, yloc + 1]
      ~c"E" -> [xloc + 1, yloc]
      ~c"S" -> [xloc, yloc - 1]
      ~c"W" -> [xloc - 1, yloc]
    end
  end

  @doc """
  implements a simple circular list for finding
  the next direction in a list of directions
  when rotating left or right
  returns a char with the new direction
  """
  def direction_change(dirs, curdir, isRight) do
    curpos = Enum.find_index(dirs, fn x -> x == curdir end)

    increment =
      if isRight do
        1
      else
        -1
      end

    Enum.at(dirs, rem(curpos + increment, length(dirs)))
  end

  @doc """
  recursive function which executes one instruction
  at the head of movestr
  returns a string with the report of the final location
  """
  def do_move(gridWidth, gridHeight, xloc, yloc, dir, moves) do
    dirs = [~c"N", ~c"E", ~c"S", ~c"W"]

    case moves do
      [] ->
        "(#{xloc}, #{yloc}, #{dir})"

      [curmove | tail] ->
        case curmove do
          ~c"F" ->
            [newxloc, newyloc] = go_forward(xloc, yloc, dir)
            # check if rover is out of bounds
            if newxloc < 0 or newxloc > gridWidth or newyloc < 0 or newyloc > gridHeight do
              "(#{xloc}, #{yloc}, #{dir}) LOST"
            else
              do_move(gridWidth, gridHeight, newxloc, newyloc, dir, tail)
            end

          ~c"L" ->
            do_move(gridWidth, gridHeight, xloc, yloc, direction_change(dirs, dir, false), tail)

          ~c"R" ->
            do_move(gridWidth, gridHeight, xloc, yloc, direction_change(dirs, dir, true), tail)

          _ ->
            IO.inspect(curmove)
            IO.puts("Bad input #{curmove}")
        end
    end
  end

  @doc """
  Tail recursive function which uses a regex to get
  the initial status and movement commands for a rover
  then calls do_move() to execute the movement commands.
  Finally, calls itself to check if there is more input.
  """
  def read_line(gridx, gridy) do
    case IO.gets("") do
      :eof ->
        :ok

      line ->
        regex = ~r/^\((\d+),\s*(\d+),\s*([NESW])\)\s*([LRF]*)$/

        case Regex.run(regex, line) do
          nil ->
            IO.puts("Invalid input. Please enter a command like '(2, 3, E) LFRFF'.")

          [_, xloc, yloc, dir, movestr] ->
            # IO.puts("You entered: #{xloc}, #{yloc} facing #{dir} with #{movestr}")
            result =
              MarsRover.do_move(
                gridx,
                gridy,
                String.to_integer(xloc),
                String.to_integer(yloc),
                String.to_charlist(dir),
                String.to_charlist(movestr) |> Enum.map(&[&1])
              )

            IO.puts(result)
        end

        read_line(gridx, gridy)
    end
  end

  @doc """
  Get the grid size from the first line,
  then call read_line() to process other input
  """
  def main() do
    gridstr = IO.gets("")
    numbers = String.trim(gridstr) |> String.split()
    [gridx, gridy] = Enum.map(numbers, &String.to_integer/1)
    # IO.puts("You entered: #{gridx} and #{gridy}")
    read_line(gridx, gridy)
  end
end

MarsRover.main()
