from tetris.drawer import TetrisDrawer
import pygame

from tetris.game import TetrisGame


class StandardTetrisDrawer(TetrisDrawer):
    """
    Standard tetris drawer for pygame
    """

    def __init__(self, game: TetrisGame):
        super().__init__(game)

        # Block dimensions
        self.block_size = 32

        self.border_size = 10

        # How many lines are displayed
        self.displayed_line_count = 20

        self.colors = [
            (32, 32, 32),       # Background color
            (32, 224, 224),     # Standard Tetromino colors
            (224, 224, 32),
            (192, 64, 192),
            (64, 192, 64),
            (192, 64, 64),
            (64, 128, 192),
            (255, 192, 64)
        ]

        self.border_color = (96, 96, 96)

        # Create a surface to draw on
        s = self.block_size
        lc = self.displayed_line_count
        self.surface = pygame.Surface((game.state.field.width*s + 200 + 2*self.border_size, lc*s + 2*self.border_size))
        self.surface = self.surface.convert(self.surface)

        # Load font
        self.font = pygame.font.Font(None, 24)

    def draw(self):
        # Clear surface
        # self.surface.fill(self.colors[0])
        s = self.block_size
        lc = self.displayed_line_count
        c = self.colors

        pygame.draw.rect(self.surface, self.border_color,
                         (0, 0, self.game.state.field.width * s + 2 * self.border_size, lc * s + 2 * self.border_size))
        pygame.draw.rect(self.surface, c[0], (self.border_size, self.border_size, self.game.state.field.width*s, lc*s))
        pygame.draw.rect(self.surface, self.border_color,
                         (self.game.state.field.width * s + 2 * self.border_size, 0, 200, 640 + 2 * self.border_size))

        # Index of top-most row to be drawn
        start_height = self.game.state.field.height - lc

        # Render the field
        field_surface = self.draw_matrix(self.game.state.field.field[lc:])
        self.surface.blit(field_surface, (self.border_size, self.border_size))

        # Render the ghost piece
        ab = self.game.state.active_brick
        ghost_y_offset = 0
        while not self.game.state.field.check_collision(ab, 0, ghost_y_offset+1):
            ghost_y_offset += 1
        if ghost_y_offset > 0:
            for y in range(0, ab.matrix.shape[0]):
                for x in range(0, ab.matrix.shape[1]):
                    if ab.matrix[y][x]:
                        draw_x = (ab.x + x) * s + self.border_size
                        draw_y = (ab.y + y - start_height + ghost_y_offset) * s + self.border_size
                        pygame.draw.rect(self.surface, self.colors[ab.brick_type+1], (draw_x+3, draw_y+3, s-6, s-6), 3)

        # Render the active piece
        # todo: bug: active piece can be rendered on top of the border
        if ab is not None:
            active_brick_surface = self.draw_matrix(ab.matrix * (ab.brick_type + 1))
            self.surface.blit(active_brick_surface, (ab.x*s+self.border_size, (ab.y-lc)*s+self.border_size))

        # UI
        txt_level = self.font.render("Level: %d" % self.game.scoring_system.level, True, (255, 255, 255))
        txt_score = self.font.render("Score: %d" % self.game.scoring_system.score, True, (255, 255, 255))
        self.surface.blit(txt_level, (350, 30))
        self.surface.blit(txt_score, (350, 60))

        # Next brick
        txt_next = self.font.render("Next:", True, (255, 255, 255))
        self.surface.blit(txt_next, (350, 120))
        pygame.draw.rect(self.surface, self.colors[0], (350, 160, 4 * s, 4 * s))
        nbt = self.game.state.queue.peek(0)
        nbm = self.game.rotation_system.bricks[nbt][0]
        if nbt == 0:
            nbm = nbm[2:, 1:]
        sf_next = self.draw_matrix(nbm * (nbt+1))
        self.surface.blit(sf_next, (350, 160+s))

        # Hold brick
        txt_hold = self.font.render("Hold:", True, (255, 255, 255))
        self.surface.blit(txt_hold, (350, 350))
        pygame.draw.rect(self.surface, self.colors[0], (350, 390, 4 * s, 4 * s))
        if self.game.state.hold_brick is not None:
            hbt = self.game.state.hold_brick.brick_type
            hbm = self.game.rotation_system.bricks[hbt][0]
            if hbt == 0:
                hbm = hbm[2:, 1:]
            sf_hold = self.draw_matrix(hbm * (hbt + 1))
            self.surface.blit(sf_hold, (350, 390 + s))

        return self.surface

    def horizontal_line(self, origin_x, origin_y):
        c = self.colors
        s = self.block_size
        min_x = 0
        max_x = 10
        draw_y = origin_y - (self.game.state.field.height - self.displayed_line_count)
        f = self.game.state.field.field
        for x2 in range(origin_x, -1, -1):
            if f[origin_y - 1][x2] and c[f[origin_y - 1][x2]] == c[f[origin_y][x2]]:
                min_x = x2 + 1
                break
        for x2 in range(origin_x, 10):
            if f[origin_y - 1][x2] and c[f[origin_y - 1][x2]] == c[f[origin_y][x2]]:
                max_x = x2
                break
        pygame.draw.rect(self.surface, (32, 32, 32), (min_x * s, draw_y * s - 1, s * (max_x - min_x), 1))

    def draw_matrix(self, matrix):
        c = self.colors
        s = self.block_size

        # Create surface for rendering of this matrix
        dimensions = (len(matrix[0]) * s, len(matrix) * s)
        sf = pygame.Surface(dimensions)
        sf.set_colorkey((0, 0, 0))

        for y in range(0, len(matrix)):
            for x in range(0, len(matrix[0])):
                val = matrix[y][x]
                if val:
                    # Draw the brick itself
                    self.draw_brick(sf, val - 1, x * s, y * s, True)
                    lb = False
                    tb = False

                    # Connect with same-colored horizontal neighbor (to the left)
                    if x > 0 and c[matrix[y][x - 1]] == c[val]:
                        self.draw_brick(sf, val - 1, x*s - s/2, y * s)
                        lb = True

                    # Connect with vertical neighbor (to the top)
                    if y > 0 and c[matrix[y - 1][x]] == c[val]:
                        self.draw_brick(sf, val - 1, x*s, y*s - s/2)
                        tb = True

                    # Connect with diagonal neighbors (if left and top are also the same color)
                    if lb and tb and c[matrix[y - 1][x - 1]] == c[val]:
                        self.draw_brick(sf, val - 1, x*s - s/2, y*s - s/2)
        return sf

    def draw_brick(self, sf, brick_type, x, y, frame=False):
        s = self.block_size
        if frame:
            pygame.draw.rect(sf, (32, 32, 32), (x, y, s, s))
            pass

        pygame.draw.rect(sf, self.colors[brick_type + 1], (x+3, y+3, s-6, s-6), 3)
        pygame.draw.rect(sf, self.colors[brick_type+1], (x+4, y+4, s-8, s-8))
