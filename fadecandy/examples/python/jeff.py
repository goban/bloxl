#!/usr/bin/python

import time, random, sys
from os import path
from functools import reduce

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import opc


BLOXL_HOST = 'localhost'
BLOXL_PORT = '7890'


def get_client():
    return opc.Client('{0}:{1}'.format(BLOXL_HOST, BLOXL_PORT))


client = get_client()


NUMBER_LEDS = 800
NUMBER_SQUARES = 200
NUMBER_LEDS_PER_SQ = 4

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
DEFAULT_DELAY = SHORT_DELAY


def delay(t=None):
    if t:
        time.sleep(t)


WHEEL_MAXIMUM = 255
WHEEL_DIVISIONS = [85, 170]


def wheel(WheelPos):
    if WheelPos < WHEEL_DIVISIONS[0]:
        color = ((WheelPos * 3), (WHEEL_MAXIMUM - WheelPos * 3), 0)
        return color
    else:
        if WheelPos < WHEEL_DIVISIONS[1]:
            WheelPos -= WHEEL_DIVISIONS[0]
            color = ((WHEEL_MAXIMUM - WheelPos * 3), 0, (WheelPos * 3))
            return color
        else:
            WheelPos -= WHEEL_DIVISIONS[1]
            color = (0, (WheelPos * 3), (WHEEL_MAXIMUM - WheelPos * 3))
            return color


RANDOM_COLOR_MINIMUM = 33
RANDOM_COLOR_MAXIMUM = 255


def random_color():
    return random.randint(RANDOM_COLOR_MINIMUM, RANDOM_COLOR_MAXIMUM)


def random_pixels():
    return wheel(random_color())


def flatten_list(lst):
    return reduce(lambda x, y: x + y, lst)


class Bloxl(object):

    def __init__(self):

        self.height = NUMBER_ROWS
        self.width = NUMBER_COLUMNS
        self.max_x_coordinate = self.width - 1
        self.max_y_coordinate = self.height - 1

        self.leds_height = self.height * 2
        self.leds_width = self.width * 2
        self.leds_max_x_coordinate = self.leds_width - 1
        self.leds_max_y_coordinate = self.leds_height - 1

        self.grid = [[SqBlox(rownum, colnum) for colnum in range(NUMBER_COLUMNS)] for rownum in range(NUMBER_ROWS)]

    def iterate_squares(self):
        for i in range(self.height):
            for j in range(self.width):
                yield self.grid[i][j]

    def iterate_leds(self):
        for sq in self.iterate_squares():
            for led in sq.leds:
                yield led

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
        return self.pick_random_coord_if_none()

    def get_random_led_coordinate_x(self):
        return random.randint(0, self.leds_max_x_coordinate)

    def get_random_led_coordinate_y(self):
        return random.randint(0, self.leds_max_y_coordinate)

    def pick_random_led_coord_if_none(self, coord_x=None, coord_y=None):
        if not coord_x:
            coord_x = self.get_random_LED_coordinate_x()
        if not coord_y:
            coord_y = self.get_random_LED_coordinate_y()
        return coord_x, coord_y

    def random_led_coord(self):
        return self.pick_random_coord_if_none()

    def step_right(self, x, y, max_x=None):
        if not max_x:
            max_x = self.max_x_coordinate
        if x >= max_x:
            return None
        return x+1, y

    def step_left(self, x, y, min_x=None):
        if not min_x:
            min_x = 0
        if x <= min_x:
            return None
        return x-1, y

    def step_down(self, x, y, max_y=None):
        if not max_y:
            max_y = self.max_y_coordinate
        if y >= max_y:
            return None
        return x, y+1

    def step_up(self, x, y, min_y):
        if not min_y:
            min_y = 0
        if x <= min_y:
            return None
        return x, y-1

    def step_led_right(self, x, y, max_x=None):
        if not max_x:
            max_x = self.leds_max_x_coordinate
        if x >= max_x:
            return None
        return x+1, y

    def step_led_left(self, x, y, min_x=None):
        if not min_x:
            min_x = 0
        if x <= min_x:
            return None
        return x-1, y

    def step_led_down(self, x, y, max_y=None):
        if not max_y:
            max_y = self.leds_max_y_coordinate
        if y >= max_y:
            return None
        return x, y+1

    def step_led_up(self, x, y, min_y):
        if not min_y:
            min_y = 0
        if x <= min_y:
            return None
        return x, y-1

    def can_step_up(self, x, y):
        return self.step_up(x, y) is not None

    def can_step_down(self, x, y):
        return self.step_down(x, y) is not None

    def can_step_left(self, x, y):
        return self.step_left(x, y) is not None

    def can_step_right(self, x, y):
        return self.step_right(x, y) is not None

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

    def put_pixels(self):
        client.put_pixels(self.bloxl.get_flat_pixels())

    def get_flat_pixels(self):
        return flatten_list([sq.get_pixels() for sq in flatten_list(self.grid)])

    def get_flat_colors(self):
        return flatten_list([sq.get_colors() for sq in flatten_list(self.grid)])

    def blanket_pixels(self, pixels=None, display=True, delay_after=DEFAULT_DELAY, delay_before=DEFAULT_DELAY_BEFORE):
        for led in self.iterate_leds():
            led.set_pixels(pixels)
        self.display(display, delay_after, delay_before)

    def blanket_color(self, color, display=True, delay_after=DEFAULT_DELAY, delay_before=DEFAULT_DELAY_BEFORE):
        for led in self.iterate_leds():
            led.set_color(color)
        self.display(display, delay_after, delay_before)

    def hide_all(self, display=True, delay_after=DEFAULT_DELAY, delay_before=DEFAULT_DELAY_BEFORE):
        for led in self.iterate_leds():
            led.hide()
        self.display(display, delay_after, delay_before)

    def random_all(self):
        for led in self.iterate_leds():
            led.random_color()


def blank_bloxl():
    return Bloxl()


class SqBlox(object):

    def __init__(self, rownum, colnum):

        self.leds = [LedBlox(sqnum, rownum, colnum) for sqnum in range(NUMBER_LEDS_PER_SQ)]

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

    def __init__(self, sqnum, rownum, colnum, pixels=None, color=None, wheel_val=None):

        self.sqnum = sqnum
        self.rownum = rownum
        self.colnum = colnum

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


def hidden_pixel_change(coord_x, coord_y):
    return PixelChange(coord_x, coord_y, HIDDEN_PIXEL)


def random_pixel_color_change(coord_x, coord_y, color=None):
    if color is None:
        color = random_color()
    return PixelChange(coord_x, coord_y, color)


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
        self.pixels_to_update = pixels_to_update
        self.shape_type = 'squares'


class ColorSequence(object):

    def __init__(
            self, starting_color=HIDDEN_PIXEL, use_to_sequence='function', auto_wheel=False,
            repeat_sequence=False):
        self.starting_color = starting_color
        self.current_color = starting_color
        self.use_to_sequecne = use_to_sequence
        self.position_sequence = -1
        self.auto_wheel = auto_wheel
        self.repeat_sentence = repeat_sequence

    def color_sequence(self):
        return []

    def get_next_color(self, color):
        return color

    def next_color_in_sequence(self):
        self.position_sequence += 1
        if self.use_to_sequecne == 'function':
            next_color = self.get_next_color(self.current_color)
            if next_color:
                return self.get_next_color(self.current_color)
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


class BloxlUpdate(object):

    def __init__(self, bloxl=None, led_changes=None, square_changes=None, display=True, delay_after=DEFAULT_DELAY, delay_before=DEFAULT_DELAY_BEFORE):

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
                    self.bloxl.set_led_pixels(led_change.pixels, led_change.coord_x, led_change.coord_y)
                else:
                    color = led_change.color
                    if color:
                        self.bloxl.set_led_pixels(wheel(color))
        if self.square_changes:
            for square_change in self.square_changes:
                pixels = square_change.pixels
                if pixels:
                    self.bloxl.set_square_pixels(led_change.pixels, led_change.coord_x, led_change.coord_y)
                else:
                    color = led_change.color
                    if color:
                        self.bloxl.set_square_pixels(wheel(color))

    def display(self):

        if self.delay_before:
            delay(self.delay_before)

        self.apply_bloxl_changes()

        if self.display:
            self.bloxl.put_pixels()

        if self.delay_after:
            delay(self.delay_after)


class BloxlUpdateSequence(object):

    def __init__(self, bloxl_update_initial=None, display=True,
                 delay_after=DEFAULT_DELAY, delay_before=DEFAULT_DELAY_BEFORE):
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

        self.color_sequence = None

    def get_starting_bloxl_state(self):
        return blank_bloxl()

    def bloxl_transformer(self):
        return self.get_current_bloxl()

    def get_current_bloxl(self):
        return self.current_bloxl_update.bloxl

    def get_next_bloxl_update(self):
        next_bloxl_update=self.bloxl_transformer()
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
            max_time = 100000000000
        t_end = time.time() + max_time
        for bloxl_update in self.yield_sequence():
            if time.time() > t_end:
                return 'Time Up'
            bloxl_update.display()
        return 'Sequence Over'


class BlanketColorSequence(BloxlUpdateSequence):

    def get_starting_bloxl_state(self):

        if self.color_sequence:

            b = Bloxl()
            b.blanket_color(self.get_color_sequence().starting_color)
            return b

    def bloxl_transformer(self):

        if self.color_sequence:

            next_color = self.color_sequence.get_next_color()
            if next_color:
                b = self.get_current_bloxl()
                b.blanket_color(next_color)
                return b

class FadingColorSequence(ColorSequence):

    def get_next_color(self, color):
        if color >= WHEEL_MAXIMUM:
            return 0
        return color + 1


def get_fading_color_sequence(starting_color=0):
    return FadingColorSequence(
        starting_color=starting_color,
        auto_wheel=True,
        repeat_sequence=True
    )


def fading_bloxl_update_sequence():
    seq = BlanketColorSequence()
    seq.color_sequence = get_fading_color_sequence(0)
    return seq
