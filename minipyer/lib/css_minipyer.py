# minipyer.lib.css_minipyer.py
# CodeWriter21
# Used some codes from https://github.com/zacharyvoase/cssmin

import re as _re

from typing import Union as _Union, Optional as _Optional, Callable as _Callable

from .minipyer import Minipyer as _Minipyer


def remove_comments(css: _Union[bytes, str]) -> _Union[bytes, str]:
    """
    Removes all comments from a CSS code.

    :param css: The CSS code to remove comments from.
    :return: The CSS code with comments removed.
    """

    css_ = css
    if isinstance(css, str):
        css_ = css.encode('utf-8')

    end = 0
    while b'/*' in css_:
        start = css_.find(b'/*', max(end, 0))
        end = css_.find(b'*/', start)
        print(start, end, css_.find(b'/*'), css_.find(b'*/'))
        if start < 0:
            break
        if end < 0:
            end = len(css_)
        # Skips preserved comments.
        if len(css_) > start + 1 and css_[start + 2:start + 3] == '!':
            end = start + 2
            continue
        css_length = len(css_)
        css_ = css_[:start] + css_[end + 2:]
        end -= css_length - len(css_)

    if isinstance(css, str):
        css_ = css_.decode('utf-8')

    return css_


def remove_unnecessary_whitespace(css: _Union[bytes, str]) -> _Union[bytes, str]:
    """
    Removes unnecessary whitespace from a CSS code.

    :param css: The CSS code to remove unnecessary whitespace from.
    :return: The CSS code with unnecessary whitespace removed.
    """

    css_ = css
    if isinstance(css, str):
        css_ = css.encode('utf-8')

    css_ = _re.sub(rb'\s*([!:;,{}>+~\(\)\[\]])\s*', rb'\1', css_)
    css_ = _re.sub(rb'\s+', b' ', css_)

    if isinstance(css, str):
        css_ = css_.decode('utf-8')

    return css_


def remove_unnecessary_semicolons(css: _Union[bytes, str]) -> _Union[bytes, str]:
    """
    Removes unnecessary semicolons from a CSS code.

    :param css: The CSS code to remove unnecessary semicolons from.
    :return: The CSS code with unnecessary semicolons removed.
    """

    css_ = css
    if isinstance(css, str):
        css_ = css.encode('utf-8')

    css_ = _re.sub(rb';+', b';', css_)
    css_ = _re.sub(rb'\s*;+\s*}', b'}', css_)

    if isinstance(css, str):
        css_ = css_.decode('utf-8')

    return css_


def remove_empty_rules(css: _Union[bytes, str]) -> _Union[bytes, str]:
    """
    Removes empty rules from a CSS code.

    :param css: The CSS code to remove empty rules from.
    :return: The CSS code with empty rules removed.
    """

    css_ = css
    if isinstance(css, str):
        css_ = css.encode('utf-8')

    css_ = _re.sub(rb'([^\}\{]+)\{\}', rb'', css_)

    if isinstance(css, str):
        css_ = css_.decode('utf-8')

    return css_


def normalize_rgb_colors_to_hex(css: _Union[bytes, str]):
    """
    Convert `rgb(51,102,153)` to `#336699`.

    :param css: The CSS code to normalize RGB colors to hex.
    :return: The CSS code with RGB colors normalized to hex.
    """

    css_ = css
    if isinstance(css, str):
        css_ = css.encode('utf-8')

    regex = _re.compile(rb"rgb\s*\(\s*([0-9,\s]+)\s*\)")
    match = regex.search(css_)
    while match:
        colors = map(lambda s: s.strip(), match.group(1).split(b","))
        hexcolor = b'#%.2x%.2x%.2x' % tuple(map(int, colors))
        css_ = css_.replace(match.group(), hexcolor)
        match = regex.search(css_)

    if isinstance(css, str):
        css_ = css_.decode('utf-8')

    return css_


def rgb_to_hex(rgb: _Union[str, bytes]) -> _Union[str, bytes]:
    """
    Converts rgb color to a hexadecimal color.

    Input Example: '0, 255, 0'

    :param rgb: The rgb color to convert.
    :return: The hexadecimal color.
    """

    rgb_ = rgb
    if isinstance(rgb, str):
        rgb_ = rgb.encode('utf-8')

    rgb_ = rgb_.split(b',')
    if len(rgb_) == 3:
        r, g, b = [int(x) for x in rgb_]
    else:
        raise ValueError('Invalid rgb color.')

    rgb_ = f'#{r:02x}{g:02x}{b:02x}'

    if isinstance(rgb, bytes):
        rgb_ = rgb_.encode('utf-8')

    return rgb_


def normalize_rgb_to_hex(css: _Union[bytes, str]) -> _Union[bytes, str]:
    """
    Normalizes rgb() colors to hexadecimal.

    :param css: The CSS code to normalize rgb() colors to hexadecimal.
    :return: The CSS code with rgb() colors normalized to hexadecimal.
    """

    css_ = css
    if isinstance(css, str):
        css_ = css.encode('utf-8')

    # Matches any rgb() color.
    css_ = _re.sub(rb'rgb\(([0-9,\s]+)\)', lambda match: rgb_to_hex(match.group(1)), css_)

    if isinstance(css, str):
        css_ = css_.decode('utf-8')

    return css_


def condense_zero_units(css: _Union[bytes, str]) -> _Union[bytes, str]:
    """
    Condenses zero units to a single zero.

    :param css: The CSS code to condense zero units.
    :return: The CSS code with zero units condensed.
    """
    css_ = css
    if isinstance(css, str):
        css_ = css.encode('utf-8')
    # Matches any zero unit.
    css_ = _re.sub(rb'(?<=[\s:])0([a-z%]|)', b'0', css_)
    if isinstance(css, str):
        css_ = css_.decode('utf-8')
    return css_


def condense_multidimensional_zeros(css: _Union[bytes, str]):
    """
    Replace `:0 0 0 0;`, `:0 0 0;` etc. with `:0;`.

    :param css: The CSS code to condense multidimensional zeros.
    :return: The CSS code with multidimensional zeros condensed.
    """

    css_ = css
    if isinstance(css, str):
        css_ = css.encode('utf-8')

    css_ = css_.replace(b":0 0 0 0;", b":0;")
    css_ = css_.replace(b":0 0 0;", b":0;")
    css_ = css_.replace(b":0 0;", b":0;")

    # Revert `background-position:0;` to the valid `background-position:0 0;`.
    css_ = css_.replace(b"background-position:0;", b"background-position:0 0;")

    if isinstance(css, str):
        css_ = css_.decode('utf-8')

    return css_


def condense_floating_points(css: _Union[bytes, str]):
    """
    Replace `0.6` with `.6` where possible.

    :param css: The CSS code to condense floating points.
    :return: The CSS code with floating points condensed.
    """

    css_ = css
    if isinstance(css, str):
        css_ = css.encode('utf-8')

    css_ = _re.sub(rb"(:|\s)0+\.(\d+)", rb"\1.\2", css_)

    if isinstance(css, str):
        css_ = css_.decode('utf-8')

    return css_


def condense_hex_colors(css: _Union[bytes, str]):
    """
    Shorten colors from #AABBCC to #ABC where possible.

    :param css: The CSS code to condense hex colors.
    :return: The CSS code with hex colors condensed.
    """

    css_ = css
    if isinstance(css, str):
        css_ = css.encode('utf-8')

    regex = _re.compile(rb"([^\"'=\s])(\s*)#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])"
                        rb"([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])")
    match = regex.search(css_)
    while match:
        first = match.group(3) + match.group(5) + match.group(7)
        second = match.group(4) + match.group(6) + match.group(8)
        if first.lower() == second.lower():
            css_ = css_.replace(match.group(), match.group(1) + match.group(2) + b'#' + first)
            match = regex.search(css_, match.end() - 3)
        else:
            match = regex.search(css_, match.end())

    if isinstance(css, str):
        css_ = css_.decode('utf-8')

    return css_


def condense_whitespace(css: _Union[bytes, str]):
    """
    Condense multiple adjacent whitespace characters into one.

    :param css: The CSS code to condense whitespaces.
    :return: The CSS code with whitespaces condensed.
    """

    css_ = css
    if isinstance(css, str):
        css_ = css_.encode('utf-8')

    css_ = _re.sub(rb"\s+", b" ", css_)

    if isinstance(css, str):
        css_ = css_.decode('utf-8')

    return css_


def condense_semicolons(css: _Union[bytes, str]):
    """
    Condense multiple adjacent semicolon characters into one.

    :param css: The CSS code to condense semicolons.
    :return: The CSS code with semicolons condensed.
    """

    css_ = css
    if isinstance(css, str):
        css_ = css_.encode('utf-8')

    css_ = _re.sub(rb";;+", rb";", css_)

    if isinstance(css, str):
        css_ = css_.decode('utf-8')

    return css_


def wrap_css_lines(css: _Union[bytes, str], line_length: int):
    """
    Wrap the lines of the given CSS to an approximate length.

    :param css: The CSS code to wrap lines.
    :param line_length: The maximum length of a line.
    :return: The CSS code with lines wrapped.
    """

    css_ = css
    if isinstance(css, str):
        css_ = css_.encode('utf-8')

    lines = []
    line_start = 0
    for i, char in enumerate(css_):
        # It's safe to break after `}` characters.
        if char == b'}' and (i - line_start >= line_length):
            lines.append(css_[line_start:i + 1])
            line_start = i + 1

    if line_start < len(css_):
        lines.append(css_[line_start:])
    css_ = b'\n'.join(lines)

    if isinstance(css, str):
        css_ = css_.decode('utf-8')

    return css_


class CSSMinipyer(_Minipyer):
    remove_comments: _Callable = remove_comments
    condense_whitespace: _Callable = condense_whitespace
    remove_unnecessary_whitespace: _Callable = remove_unnecessary_whitespace
    remove_unnecessary_semicolons: _Callable = remove_unnecessary_semicolons
    condense_zero_units: _Callable = condense_zero_units
    condense_multidimensional_zeros: _Callable = condense_multidimensional_zeros
    condense_floating_points: _Callable = condense_floating_points
    normalize_rgb_colors_to_hex: _Callable = normalize_rgb_colors_to_hex
    condense_hex_colors: _Callable = condense_hex_colors
    wrap_css_lines: _Callable = wrap_css_lines
    condense_semicolons: _Callable = condense_semicolons

    @staticmethod
    def do_pseudoclassbmh(css: _Union[bytes, str]):
        """
        A pseudo class for the Box Model Hack
        (see http://tantek.com/CSS/Examples/boxmodelhack.html)

        :param css: The CSS code to apply the pseudo class.
        :return: The CSS code with the pseudo class applied.
        """
        css_ = css
        if isinstance(css, str):
            css_ = css_.encode('utf-8')

        css_ = css_.replace(b'"\\"}\\""', b"___PSEUDOCLASSBMH___")

        if isinstance(css, str):
            css_ = css_.decode('utf-8')

        return css_

    @staticmethod
    def undo_pseudoclassbmh(css: _Union[bytes, str]):
        """
        A pseudo class for the Box Model Hack
        (see http://tantek.com/CSS/Examples/boxmodelhack.html)

        :param css: The CSS code to remove the pseudo class.
        :return: The CSS code with the pseudo class removed.
        """
        css_ = css
        if isinstance(css, str):
            css_ = css_.encode('utf-8')

        css_ = css_.replace(b"___PSEUDOCLASSBMH___", b'"\\"}\\""')

        if isinstance(css, str):
            css_ = css_.decode('utf-8')

        return css_

    def minipy(self, css: _Optional[_Union[bytes, str]] = None, remove_comments_: bool = True,
               condense_whitespace_: bool = True, remove_unnecessary_whitespace_: bool = True,
               remove_unnecessary_semicolons_: bool = True, condense_zero_units_: bool = True,
               condense_multidimensional_zeros_: bool = True, condense_floating_points_: bool = True,
               normalize_rgb_colors_to_hex_: bool = True, condense_hex_colors_: bool = True,
               wrap_length: int = 0, condense_semicolons_: bool = True) -> _Union[bytes, str]:
        """
        Minipy the CSS code.

        :param css: The CSS code to minipy.
        :param remove_comments_: Whether to remove comments.
        :param condense_whitespace_: Whether to condense whitespace.
        :param remove_unnecessary_whitespace_: Whether to remove unnecessary whitespace.
        :param remove_unnecessary_semicolons_: Whether to remove unnecessary semicolons.
        :param condense_zero_units_: Whether to condense zero units.
        :param condense_multidimensional_zeros_: Whether to condense multidimensional zeros.
        :param condense_floating_points_: Whether to condense floating points.
        :param normalize_rgb_colors_to_hex_: Whether to normalize RGB colors to hex.
        :param condense_hex_colors_: Whether to condense hex colors.
        :param wrap_length: The length at which to wrap the CSS code.
        :param condense_semicolons_: Whether to condense semicolons.
        :return: The minified CSS code.
        """

        css = self.code

        if remove_comments_:
            css = self.remove_comments(css)
        if condense_whitespace_:
            css = self.condense_whitespace(css)
        css = self.do_pseudoclassbmh(css)
        if remove_unnecessary_whitespace_:
            css = self.remove_unnecessary_whitespace(css)
        if remove_unnecessary_semicolons_:
            css = self.remove_unnecessary_semicolons(css)
        if condense_zero_units_:
            css = self.condense_zero_units(css)
        if condense_multidimensional_zeros_:
            css = self.condense_multidimensional_zeros(css)
        if condense_floating_points_:
            css = self.condense_floating_points(css)
        if normalize_rgb_colors_to_hex_:
            css = self.normalize_rgb_colors_to_hex(css)
        if condense_hex_colors_:
            css = self.condense_hex_colors(css)
        if wrap_css_lines:
            css = self.wrap_css_lines(css, wrap_length)
        css = self.undo_pseudoclassbmh(css)
        if condense_semicolons_:
            css = self.condense_semicolons(css)

        return css
