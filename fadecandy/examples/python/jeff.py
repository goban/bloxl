#!/usr/bin/python

import time, random, sys
from os import path
from functools import reduce
from unidecode import unidecode

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import opc

from colr import color


BLOXL_HOST = 'localhost'
BLOXL_PORT = '7890'


def get_client():
    return opc.Client('{0}:{1}'.format(BLOXL_HOST, BLOXL_PORT))


client = get_client()


NUMBER_LEDS = 800
NUMBER_SQUARES = 200
NUMBER_LEDS_PER_SQ = 4
NUMBER_ROWS_SQUARE = 2

NUMBER_ROWS = 20
NUMBER_COLUMNS = 10

HIDDEN_PIXEL = (0, 0, 0)

TINY_DELAY = 0.05
SHORT_DELAY = 0.1
MEDIUM_DELAY = 0.3
LONG_DELAY = 0.5
LONGER_DELAY = 0.8
LONGEST_DELAY = 1.5

DEFAULT_DELAY_BEFORE = None
DEFAULT_DELAY = None


def delay(t=None):
    if t:
        time.sleep(t)


WHEEL_MAXIMUM = 255
WHEEL_DIVISIONS = [85, 170]


def wheel(WheelPos):
    if WheelPos < WHEEL_DIVISIONS[0]:
        color = ((WheelPos * 3), (WHEEL_MAXIMUM - WheelPos * 3), 0)
    else:
        if WheelPos < WHEEL_DIVISIONS[1]:
            WheelPos -= WHEEL_DIVISIONS[0]
            color = ((WHEEL_MAXIMUM - WheelPos * 3), 0, (WheelPos * 3))
        else:
            WheelPos -= WHEEL_DIVISIONS[1]
            color = (0, (WheelPos * 3), (WHEEL_MAXIMUM - WheelPos * 3))
    return color


RANDOM_COLOR_MINIMUM = 1
RANDOM_COLOR_MAXIMUM = 255


def random_color():
    return random.randint(RANDOM_COLOR_MINIMUM, RANDOM_COLOR_MAXIMUM)


def random_pixels():
    return wheel(random_color())


def flatten_list(lst):
    return reduce(lambda x, y: x + y, lst)


class Bloxl(object):

    def __init__(
            self, height=NUMBER_ROWS, width=NUMBER_COLUMNS,
            number_leds_per_sq=NUMBER_LEDS_PER_SQ, square_number_rows=NUMBER_ROWS_SQUARE
    ):

        self.height = height
        self.width = width
        self.max_x_coordinate = self.width - 1
        self.max_y_coordinate = self.height - 1

        self.leds_height = self.height * (number_leds_per_sq / 2)
        self.leds_width = self.width * (number_leds_per_sq / 2)
        self.leds_max_x_coordinate = self.leds_width - 1
        self.leds_max_y_coordinate = self.leds_height - 1

        self.number_leds_per_sq = number_leds_per_sq
        self.square_number_rows = square_number_rows
        self.square_led_divisor = self.number_leds_per_sq // self.square_number_rows
        self.number_leds_per_row = self.width * square_number_rows

        self.grid = [
            [
                SqBlox(
                    rownum, colnum, number_leds=number_leds_per_sq, number_rows=square_number_rows
                ) for colnum in range(NUMBER_COLUMNS)
            ] for rownum in range(NUMBER_ROWS)
        ]

    def iterate_squares(self):
        for i in range(self.height):
            for j in range(self.width):
                yield self.grid[i][j]

    def iterate_leds(self):
        for sq in self.iterate_squares():
            for led in sq.leds:
                yield led

    def all_leds(self):
        return [l for l in self.iterate_leds()]

    def get_random_coordinate_x(self):
        return random.randint(0, self.max_x_coordinate)

    def get_random_coordinate_y(self):
        return random.randint(0, self.max_y_coordinate)

    def pick_random_coord_if_none(self, coord_x=None, coord_y=None):
        if not coord_x:
            coord_x = self.get_random_coordinate_x()
        if not coord_y:
            coord_y = self.get_random_coordinate_y()
        return coord_x, coord_y

    def random_coord(self):
        """
        Get a random square
        """
        return self.pick_random_coord_if_none()

    def get_random_led_coordinate_x(self):
        return random.randint(0, self.leds_max_x_coordinate)

    def get_random_led_coordinate_y(self):
        return random.randint(0, self.leds_max_y_coordinate)

    def pick_random_led_coord_if_none(self, coord_x=None, coord_y=None):
        if not coord_x:
            coord_x = self.get_random_led_coordinate_x()
        if not coord_y:
            coord_y = self.get_random_led_coordinate_y()
        return coord_x, coord_y

    def random_led_coord(self):
        return self.pick_random_coord_if_none()

    def put_pixels(self):
        client.put_pixels(self.get_flat_pixels())

    def get_flat_pixels(self):
        return flatten_list([sq.get_pixels() for sq in flatten_list(self.grid)])

    def get_flat_colors(self):
        return flatten_list([sq.get_colors() for sq in flatten_list(self.grid)])

    def blanket_pixels(self, pixels=None):
        for led in self.iterate_leds():
            led.set_pixels(pixels)

    def blanket_color(self, color):
        for led in self.iterate_leds():
            led.set_color(color)

    def hide_all(self):
        for led in self.iterate_leds():
            led.hide()

    def random_all(self):
        for led in self.iterate_leds():
            led.random_color()

    def legal_led_coord(self, x=0, y=0, max_x=None, max_y=None, min_x=None, min_y=None):
        if x < 0 or y < 0 or x > self.leds_max_x_coordinate or y > self.leds_max_y_coordinate or \
                x > max_x or y > max_y or x < min_x or y < min_y:
            return False
        return True

    def get_led_at_coord(self, x=0, y=0, max_x=None, max_y=None, min_x=None, min_y=None):
        if self.legal_led_coord(x, y, max_x, max_y, min_x, min_y):
            sd = self.square_led_divisor
            self.grid[x // sd][y // sd].get_led_at_coord(x % sd, y % sd)

    def set_led_pixels(self, coord_x=0, coord_y=0, pixels=HIDDEN_PIXEL):
        self.get_led_at_coord(coord_x, coord_y).set_pixels(pixels)

    def set_led_color(self, coord_x=0, coord_y=0, color=0):
        self.get_led_at_coord(coord_x, coord_y).set_color(color)

    def legal_sq_coord(self, x=0, y=0, max_x=None, max_y=None, min_x=None, min_y=None):
        if x < 0 or y < 0 or x > self.max_x_coordinate or y > self.max_y_coordinate or \
                x > max_x or y > max_y or x < min_x or y < min_y:
            return False
        return True

    def get_sq_at_coord(self, x=0, y=0, max_x=None, max_y=None, min_x=None, min_y=None):
        if self.legal_sq_coord(x, y, max_x, max_y, min_x, min_y):
            return self.grid[x][y]
        return None

    def set_sq_pixels(self, coord_x=0, coord_y=0, pixels=HIDDEN_PIXEL):
        self.get_sq_at_coord(coord_x, coord_y).blanket_pixels(pixels)

    def set_sq_color(self, coord_x=0, coord_y=0, color=0):
        self.get_sq_at_coord(coord_x, coord_y).blanket_color(color)

    def step_right(self, x, y, max_x=None):
        return self.get_sq_at_coord(x+1, y, max_x=max_x)

    def step_left(self, x, y, min_x=None):
        return self.get_sq_at_coord(x-1, y, min_x=min_x)

    def step_down(self, x, y, max_y=None):
        return self.get_sq_at_coord(x, y+1, max_y=max_y)

    def step_up(self, x, y, min_y=0):
        return self.get_sq_at_coord(x, y-1, min_y=min_y)

    def step_led_right(self, x, y, max_x=None):
        return self.get_led_at_coord(x+1, y, max_x=max_x)

    def step_led_left(self, x, y, min_x=None):
        return self.get_led_at_coord(x-1, y, min_x=min_x)

    def step_led_down(self, x, y, max_y=None):
        return self.get_led_at_coord(x, y+1, max_y=max_y)

    def step_led_up(self, x, y, min_y=0):
        return self.get_led_at_coord(x, y-1, min_y=min_y)

    def print_repr(self):
        x = 0
        for led in self.iterate_leds():
            print(led.str_repr(), end='')
            if x % self.number_leds_per_row == 0:
                print()


def get_bloxl(bloxl):
    if bloxl:
        return bloxl
    return Bloxl()


def blank_bloxl():
    return Bloxl()


class SqBlox(object):

    def __init__(self, rownum, colnum, number_leds=NUMBER_LEDS_PER_SQ, number_rows=NUMBER_ROWS_SQUARE):

        self.number_leds = number_leds
        self.number_rows = number_rows
        self.number_columns = self.number_leds // self.number_rows

        leds = []
        for x in range(self.number_rows):
            for y in range(self.number_leds // self.number_rows):
                leds.append(
                    LedBlox(rownum, colnum, x, y)
                )
        self.leds = leds

        self.max_x_coordinate = self.number_columns - 1
        self.max_y_coordinate = self.number_rows - 1

    def legal_coord(self, x, y):
        return x >= 0 and y >= 0 and x <= self.max_x_coordinate and y <= self.max_y_coordinate

    def get_led_at_coord(self, x, y):
        for led in self.leds:
            if led.sq_x_num == x and led.sq_y_num == y:
                return led
        return None

    def get_pixels(self):
        return [e.pixels for e in self.leds]

    def get_colors(self):
        return [e.color_val for e in self.leds]

    def blanket_pixels(self, pixels=None):
        for led in self.leds:
            led.set_pixels(pixels)

    def blanket_color(self, color):
        for led in self.leds:
            led.set_color(color)

    def blanket_random(self):
        for led in self.leds:
            led.random_color()

    def hide_all(self):
        for led in self.leds:
            led.hide()

    def is_hidden(self):
        for led in self.leds:
            if led.is_hidden():
                return True
        return False


class LedBlox(object):

    def __init__(self, rownum, colnum, sq_x_num, sq_y_num, pixels=None, color=None):

        self.rownum = rownum
        self.colnum = colnum

        self.sq_x_num = sq_x_num
        self.sq_y_num = sq_y_num

        self.pixels = None
        self.set_pixels(pixels)

        self.color_val = None
        self.set_color(color)

    def set_color(self, color=None):
        if color:
            self.color_val = color
            self.set_pixels(wheel(color))

    def set_pixels(self, pixels=None):
        if pixels:
            self.pixels = pixels

    def hide(self):
        self.set_pixels(pixels=HIDDEN_PIXEL)

    def is_hidden(self):
        return self.pixels == HIDDEN_PIXEL

    def random_color(self):
        self.set_pixels(random_pixels())

    def str_repr(self):
        return color(' ', fore='white', back=self.pixels)


class PixelChange(object):

    def __init__(self, coord_x, coord_y, grid_type='squares', color=None, pixels=None, hide=False):
        """
        Grid type is squares or leds
        """
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.grid_type = grid_type
        self.color = color
        self.pixels = pixels
        self.hide = hide


def hidden_pixel_change(coord_x, coord_y, grid_type='squares'):
    return PixelChange(coord_x, coord_y, grid_type=grid_type, pixels=HIDDEN_PIXEL, hide=True)


def random_pixel_color_change(coord_x, coord_y, grid_type='squares', color=None):
    if color is None:
        color = random_color()
    return PixelChange(coord_x, coord_y, grid_type=grid_type, color=color, hide=False)


def random_bloxl_led_position_color_change(bloxl, color=None):
    if color is None:
        color = random_color()
    coord_x, coord_y = bloxl.random_coord()
    return PixelChange(coord_x, coord_y, color)


class LEDShape(object):

    def __init__(self, pixels_to_update):
        self.pixels_to_update = pixels_to_update
        self.shape_type = 'leds'

    def iterate_pixels(self, repeat_sequence=False):
        for pixel in self.pixels_to_update:
            yield pixel
        if repeat_sequence:
            while True:
                for pixel in self.pixels_to_update:
                    yield pixel

    def iterate_coordinates(self, repeat_sequence=False):
        for pixel in self.iterate_pixels(repeat_sequence):
            yield pixel.coord_x, pixel.coord_y


class SquaresShape(LEDShape):

    def __init__(self, pixels_to_update):
        super(LEDShape, self).__init__(pixels_to_update)
        self.shape_type = 'squares'


class ColorSequence(object):

    def __init__(
            self, starting_color=HIDDEN_PIXEL, use_to_sequence='function', auto_wheel=False,
            repeat_sequence=False, step_value=1):
        self.starting_color = starting_color
        self.current_color = starting_color
        self.use_to_sequecne = use_to_sequence
        self.position_sequence = -1
        self.auto_wheel = auto_wheel
        self.repeat_sentence = repeat_sequence
        self.step_value = step_value

    def color_sequence(self):
        return []

    def get_next_color(self):
        return None

    def next_color_in_sequence(self):
        self.position_sequence += 1
        if self.use_to_sequecne == 'function':
            next_color = self.get_next_color()
            if next_color:
                return self.get_next_color()
        if self.use_to_sequecne == 'sequence':
            seq = self.color_sequence()
            if self.position_sequence < len(seq):
                return seq[self.position_sequence]
            if self.repeat_sentence:
                return seq[len(seq) % self.position_sequence]
        return None

    def get_color_representation(self, col=None):
        col = self.current_color
        if self.auto_wheel:
            return wheel(col)
        return col

    def iterate_colors(self):
        yield self.get_color_representation()
        has_next_color = True
        while has_next_color:
            next_color = self.next_color_in_sequence()
            if next_color:
                yield next_color
            else:
                has_next_color = False

    def get_starting_color(self):
        if self.starting_color:
            return self.starting_color
        next_color = self.get_next_color()
        if next_color:
            return next_color
        return HIDDEN_PIXEL

    def get_initial_bloxl(self, bloxl=None):
        sc = self.get_starting_color()
        if sc:
            b = get_bloxl(bloxl)
            b.blanket_color(sc)
            return b


class BloxlUpdate(object):

    def __init__(
            self, bloxl=None, led_changes=None, square_changes=None, display=True,
            delay_after=DEFAULT_DELAY, delay_before=DEFAULT_DELAY_BEFORE
    ):

        self.bloxl = bloxl
        if not bloxl:
            self.bloxl = blank_bloxl()
        self.led_changes = led_changes
        self.square_changes = square_changes
        self.display = display
        self.delay_after = delay_after
        self.delay_before = delay_before

    def apply_bloxl_changes(self):
        if self.led_changes:
            for led_change in self.led_changes:
                pixels = led_change.pixels
                if pixels:
                    self.bloxl.set_led_pixels(led_change.coord_x, led_change.coord_y, led_change.pixels)
                else:
                    color = led_change.color
                    if color:
                        self.bloxl.set_led_pixels(led_change.coord_x, led_change.coord_y, wheel(color))
        if self.square_changes:
            for square_change in self.square_changes:
                pixels = square_change.pixels
                if pixels:
                    self.bloxl.set_sq_pixels(led_change.coord_x, led_change.coord_y, led_change.pixels)
                else:
                    color = led_change.color
                    if color:
                        self.bloxl.set_sq_pixels(wheel(color))

    def display(self):

        if self.delay_before:
            delay(self.delay_before)

        self.apply_bloxl_changes()

        if self.display:
            self.bloxl.put_pixels()

        if self.delay_after:
            delay(self.delay_after)


class BloxlUpdateSequence(object):

    def __init__(
            self, bloxl_update_initial=None, display=True,
            delay_after=DEFAULT_DELAY, delay_before=DEFAULT_DELAY_BEFORE, default_display_time=100000,
            color_sequences=[], squares_shapes=[], leds_shapes=[]
    ):
        self.bloxl_update_initial = bloxl_update_initial
        if not self.bloxl_update_initial:
            starting_bloxl_state = self.get_starting_bloxl_state()
            if starting_bloxl_state:
                self.bloxl_update_initial = BloxlUpdate(
                    bloxl=starting_bloxl_state,
                    display=display,
                    delay_before=delay_before,
                    delay_after=delay_after
                )

        self.current_bloxl_update = None
        self.bloxl_updates = []
        if self.bloxl_update_initial:
            self.current_bloxl_update = self.bloxl_update_initial
            self.bloxl_updates = [bloxl_update_initial]

        self.sequence_number = 0

        self.display = display
        self.delay_after = delay_after
        self.delay_before = delay_before

        self.default_display_time = default_display_time

        self.color_sequences = color_sequences
        self.squares_shapes = squares_shapes
        self.leds_shapes = leds_shapes

    def get_starting_bloxl_state(self):
        return blank_bloxl()

    def bloxl_transformer(self):
        return self.get_current_bloxl()

    def get_current_bloxl(self):
        return self.current_bloxl_update.bloxl

    def get_next_bloxl_update(self):
        next_bloxl_update = self.bloxl_transformer()
        if next_bloxl_update:
            return BloxlUpdate(
                bloxl=next_bloxl_update,
                display=self.display,
                delay_before=self.delay_before,
                delay_after=self.delay_after
            )
        return None

    def yield_sequence(self):
        if self.current_bloxl_update:
            yield self.current_bloxl_update
        updating = True
        while updating:
            next_update = self.get_next_bloxl_update()
            if next_update:
                yield self.current_bloxl_update
            else:
                updating = False

    def display_sequence(self, max_time=None):
        if not max_time:
            max_time = self.default_display_time
        t_end = time.time() + max_time
        for bloxl_update in self.yield_sequence():
            if time.time() > t_end:
                return 'Time Up'
            if bloxl_update:
                bloxl_update.display()
            else:
                return 'Sequence Over'
        return 'Sequence Over'

    def get_color_sequence(self):
        if self.color_sequences:
            return self.color_sequences[0]
        return None


class BlanketColorSequence(BloxlUpdateSequence):

    def get_starting_bloxl_state(self):
        seq = self.get_color_sequence()
        if seq:
            return seq.get_initial_bloxl()

    def bloxl_transformer(self):
        seq = self.get_color_sequence()
        if seq:
            next_color = seq.get_next_color()
            if next_color:
                b = self.get_current_bloxl()
                b.blanket_color(next_color)
                return b


class FadingColorSequence(ColorSequence):

    def get_next_color(self, step_value=1):
        color = self.current_color
        if color >= WHEEL_MAXIMUM:
            return RANDOM_COLOR_MINIMUM
        return color + step_value


def get_fading_color_sequence(starting_color=HIDDEN_PIXEL, step_value=1):
    return FadingColorSequence(
        starting_color=starting_color,
        auto_wheel=True,
        repeat_sequence=True,
        step_value=step_value
    )


def fading_bloxl_update_sequence(starting_color=HIDDEN_PIXEL, step_value=1):
    return BlanketColorSequence(
        color_sequences=[get_fading_color_sequence(starting_color, step_value)]
    )




    '''
    def spiral(self):

        x = 0
        y = 0
        number_steps = 0

        filled_rows_top = 0
        filled_rows_right = 0
        filled_rows_bottom = 0
        filled_rows_left = 0

        while number_steps < NUMBER_SQUARES:

            while self.can_step_right(x, y):
                yield (x, y)
                x, y = self.step_right(x, y)
                number_steps += 1
            filled_rows_top += 1

            while self.can_step_down(x, y):
                yield (x, y)
                x, y = self.step_down(x, y)
                number_steps += 1
            filled_rows_right += 1

            while self.can_step_left(x, y):
                yield (x, y)
                x, y = self.step_left(x, y)
                number_steps += 1
            filled_rows_bottom += 1


            while self.can_step_up(x, y):
                yield (x, y)
                x, y = self.step_up(x, y)
                number_steps += 1
            filled_rows_left += 1
    '''