ui_wall = [
    "......",
    "......",
    "......",
    "......"
]

ui_ghost = [
    " .-.  ",
    "| OO| ",
    "|   | ",
    "'^^^' "
]

ui_hero = [
    " .--. ",
    "/ _.-'",
    "\\  '-.",
    " '--' "
]

ui_empty = [
    "      ",
    "      ",
    "      ",
    "      "
]

ui_pill = [
    "      ",
    " .-.  ",
    " '-'  ",
    "      "
]

wall_color = "blue"
ghost_color = "red"
pacman_color = "yellow"
pill_color = "grey"

import random
from termcolor import colored

class PacManGame:
    def __init__(self):
        self.game_map = self._get_initial_map()
        self.ghosts_on_pills = []
        self.game_finished = False
        self.win = False

    def _get_initial_map(self):
        return [
            "|--------|",
            "|G..|..G.|",
            "|...PP...|",
            "|G....@|.|",
            "|...P..|.|",
            "|--------|"
        ]

    def render_map(self, final_board_color=None):
        for row in self.game_map:
            for piece in range(4):
                for point in row:
                    color = final_board_color if final_board_color else self._get_color_for_point(point)
                    ui_element = self._get_ui_element_for_point(point, piece)
                    print(colored(ui_element, color), end='')
                print("", end='\n')

    def _get_color_for_point(self, point):
        if point == 'G':
            return ghost_color
        elif point == '|' or point == '-':
            return wall_color
        elif point == '@':
            return pacman_color
        elif point == 'P':
            return pill_color
        return None # For empty space, no specific color

    def _get_ui_element_for_point(self, point, piece):
        if point == 'G':
            return ui_ghost[piece]
        elif point == '|' or point == '-':
            return ui_wall[piece]
        elif point == '@':
            return ui_hero[piece]
        elif point == '.':
            return ui_empty[piece]
        elif point == 'P':
            return ui_pill[piece]
        return ui_empty[piece] # Default for unknown or empty

    def _find_all_ghosts(self):
        ghosts = []
        for x in range(len(self.game_map)):
            for y in range(len(self.game_map[x])):
                if self.game_map[x][y] == 'G':
                    ghosts.append([x, y])
        return ghosts

    def _find_pacman(self):
        for x in range(len(self.game_map)):
            for y in range(len(self.game_map[x])):
                if self.game_map[x][y] == '@':
                    return x, y
        return -1, -1

    def move_ghosts(self):
        all_ghosts = self._find_all_ghosts()
        new_ghosts_on_pills = []
        pacman_caught = False

        for ghost in all_ghosts:
            old_ghost_x, old_ghost_y = ghost
            was_on_pill = (old_ghost_x, old_ghost_y) in self.ghosts_on_pills

            possible_directions = [
                [old_ghost_x, old_ghost_y + 1],
                [old_ghost_x + 1, old_ghost_y],
                [old_ghost_x, old_ghost_y - 1],
                [old_ghost_x - 1, old_ghost_y]
            ]

            random.shuffle(possible_directions)
            moved = False
            for next_ghost_x, next_ghost_y in possible_directions:
                if 0 <= next_ghost_x < len(self.game_map) and 0 <= next_ghost_y < len(self.game_map[0]):
                    target = self.game_map[next_ghost_x][next_ghost_y]
                    if target not in ('|', '-', 'G'):
                        is_pacman = target == '@'
                        is_pill = target == 'P'
                        if is_pacman:
                            pacman_caught = True
                            break # Pacman caught, no more ghost movement needed for this turn

                        # Restore original content at old ghost position
                        if was_on_pill:
                            self.game_map[old_ghost_x] = self.game_map[old_ghost_x][:old_ghost_y] + "P" + self.game_map[old_ghost_x][old_ghost_y+1:]
                        else:
                            self.game_map[old_ghost_x] = self.game_map[old_ghost_x][:old_ghost_y] + "." + self.game_map[old_ghost_x][old_ghost_y+1:]

                        # Place ghost at new position
                        self.game_map[next_ghost_x] = self.game_map[next_ghost_x][:next_ghost_y] + "G" + self.game_map[next_ghost_x][next_ghost_y+1:]

                        # If ghost moved onto a pill, remember it
                        if is_pill:
                            new_ghosts_on_pills.append((next_ghost_x, next_ghost_y))
                        moved = True
                        break
            if not moved and was_on_pill:
                # If ghost didn't move but was on a pill, keep it in memory
                new_ghosts_on_pills.append((old_ghost_x, old_ghost_y))

            if pacman_caught:
                break

        self.ghosts_on_pills = new_ghosts_on_pills
        return pacman_caught

    def move_pacman(self, key):
        pacman_x, pacman_y = self._find_pacman()
        next_pacman_x, next_pacman_y = pacman_x, pacman_y

        if key == 'a':
            next_pacman_y -= 1
        elif key == 's':
            next_pacman_x += 1
        elif key == 'w':
            next_pacman_x -= 1
        elif key == 'd':
            next_pacman_y += 1
        else:
            return False, False # Not a valid move key

        if not (0 <= next_pacman_x < len(self.game_map) and 0 <= next_pacman_y < len(self.game_map[0])):
            return False, False # Out of bounds

        target = self.game_map[next_pacman_x][next_pacman_y]
        if target in ('|', '-'):
            return False, False # Hit a wall
        if target == 'G':
            return True, False # Caught by a ghost

        # Move Pacman
        self.game_map[pacman_x] = self.game_map[pacman_x][:pacman_y] + "." + self.game_map[pacman_x][pacman_y+1:]
        self.game_map[next_pacman_x] = self.game_map[next_pacman_x][:next_pacman_y] + "@" + self.game_map[next_pacman_x][next_pacman_y+1:]
        return False, True # Pacman moved successfully

    def count_pills(self):
        return sum(row.count('P') for row in self.game_map)

    def play(self):
        while not self.game_finished:
            self.render_map()
            pacman_caught_by_ghost = self.move_ghosts()
            if pacman_caught_by_ghost:
                self.win = False
                self.game_finished = True
                break

            key = input("Move (w/a/s/d): ").strip().lower()
            pacman_caught_by_ghost, pacman_moved = self.move_pacman(key)

            if pacman_caught_by_ghost:
                self.win = False
                self.game_finished = True
                break

            if self.count_pills() == 0:
                self.win = True
                self.game_finished = True
                break

        self.render_map(final_board_color="green" if self.win else "red")
        if self.win:
            print("You win! :)")
        else:
            print("You lost! :/")

if __name__ == "__main__":
    game = PacManGame()
    game.play()
