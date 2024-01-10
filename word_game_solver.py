# An app with some tools for a 4x4 letter grid word game.
# A "words.txt" file is needed for the app to work
# (not included in the repo because I'm not sure if it's copyrighted).
# The point was to come up with an algorithm by myself, so no AI was used.

import random

class Grid:
    def __init__(self, grid: str = None) -> None:
        # If a custom string is not given as a parameter then a random grid is 
        # created.
        if grid:
            # Make into list and split that list into a list of four lists
            grid = [c for c in grid]
            self.grid = [grid[4*k:4*k+4] for k in range(4)]

        else:
            dice = [
                ["V", "A", "I", "K", "Y", "L"],
                ["U", "N", "H", "M", "I", "K"],
                ["A", "N", "E", "E", "A", "A"],
                ["R", "U", "L", "N", "N", "A"],

                ["A", "A", "L", "Ä", "Ä", "G"],
                ["S", "I", "T", "Ä", "N", "Ö"],
                ["S", "I", "T", "S", "O", "E"],
                ["R", "I", "D", "L", "E", "S"],

                ["J", "O", "A", "T", "T", "O"],
                ["K", "A", "P", "H", "O", "S"],
                ["V", "I", "K", "M", "A", "T"],
                ["T", "U", "O", "M", "I", "C"],

                ["J", "A", "I", "S", "B", "U"],
                ["N", "A", "S", "F", "P", "K"],
                ["R", "E", "T", "L", "Y", "T"],
                ["E", "A", "I", "N", "M", "K"]
            ]
            random.shuffle(dice)

            grid = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]
            for r in range(4):
                for c in range(4):
                    grid[r][c] = random.choice(dice.pop(0))
        
            self.grid = grid
        # print(self.grid)
    
    def __str__(self) -> str:
        return str("\n".join(" ".join(row) for row in self.grid))

    def has(self, word: str) -> bool:
        """Returns whether a given word appears on the grid or not."""

        grid = self.grid
        word = word.upper()

        current_letter_index = 0
        potential_paths = []

        # Create roots for paths.
        for r in range(4):
            for c in range(4):
                if grid[r][c] == word[current_letter_index]:
                    potential_paths.append([(r, c)])

        for _ in range(len(word)-1):
            current_letter_index += 1
            # print(f"Looking for letter {word[current_letter_index]}.")
            # print(f"Current paths are {potential_paths}.")
            paths_backup = potential_paths[:]

            for path in potential_paths:
                replacements = []
                # print(f"  Trying to expand path {path}.")
                row = path[-1][0]
                column = path[-1][1]

                for r in range(max(row-1, 0), min(row+2, 4)):
                    for c in range(max(column-1, 0), min(column+2, 4)):
                        if (r, c) not in path \
                        and grid[r][c] == word[current_letter_index]:
                            # print(f"    Next letter was found at ({r}, {c}).")
                            # For each adjacent and unused letter.
                            new_path = path[:]
                            new_path.append((r, c))
                            replacements.append(new_path)
                
                # print(f"    Path {path} will be replaced with {replacements}.")
                # Each path is replaced with 0 or more paths that are
                # one letter longer. A path that doesn't expand is killed.
                paths_backup.remove(path)
                for r in replacements:
                    paths_backup.append(r)

            potential_paths = paths_backup[:]
            if potential_paths == []:
                return False
    
        # print(f"Final paths: {potential_paths}.")

        return True

class FileReader:
    def __init__(self) -> None:
        pass

    def read_words(self, filename: str) -> list:
        lines = []
        with open(filename) as file:
            content = file.read()
            for line in content.split("\n"):
                lines.append(line)
        return lines

class Stats:
    def __init__(self) -> None:
        pass

    def find_all_words(self, grid: Grid) -> list:
        words = FileReader().read_words("words.txt")
        list = [word for word in words if grid.has(word)]
        list.sort(key=len, reverse=True)
        return list

    def find_commonness(self, word: str) -> int:
        """Returns how many times a given word per a million grids."""
        found = 0
        for _ in range(1000000):
            if Grid().has(word):
                found += 1
        return found

class Application:
    def __init__(self) -> None:
        pass

    def instructions(self) -> None:
        print("0: Quit.")
        print("1: Find out how common a given word is.")
        print("2: Find all words on a given grid.")

    def run(self):
        print()
        self.instructions()
        while True:
            print()
            try:
                command = int(input("Enter a command: "))
            except:
                continue

            if command == 0:
                break
            if command == 1:
                word = input("Please write a word: ")
                print()
                a = f'1000000 grids were simulated, "{word}" was found on '
                a += f'{Stats().find_commonness(word)} of them.'
                print(a)

            if command == 2:
                print("Please write the grid below:")
                print()
                i = "".join([
                    input().upper(),
                    input().upper(),
                    input().upper(),
                    input().upper()
                ])
                grid = Grid(i)
                words = Stats().find_all_words(grid)
                print()
                print(f"A total of {len(words)} words were found:\n")
                for w in words:
                    print(w)
            if command == 3:
                # A secret debugging mode
                while True:
                    grid = Grid()
                    print(grid)
                    print()
                    if grid.has("aie"):
                        print("aie!")
                        break

if __name__ == "__main__":
    Application().run()