from typing import Tuple, Union

import numpy as np
from PIL import Image, ImageDraw
from PIL.Image import Image as PILImage

from text_renderer.utils.font_text import FontText


def transparent_img(size: Tuple[int, int]) -> PILImage:
    """

    Args:
        size: (width, height)

    Returns:

    """
    return Image.new("RGBA", (size[0], size[1]), (255, 255, 255, 0))


def draw_text_on_bg(
    font_text: FontText,
    text_color: Tuple[int, int, int, int] = (0, 0, 0, 255),
    char_spacing: Union[float, Tuple[float, float]] = -1,
) -> Tuple[PILImage, list]:
    """

    Parameters
    ----------
    font_text : FontText
    text_color : RGBA
        Default is black
    char_spacing : Union[float, Tuple[float, float]]
        Draw character with spacing. If tuple, random choice between [min, max)
        Set -1 to disable

    Returns
    -------
        Tuple[PILImage, list]:
            RGBA Pillow image with text on a transparent image, and character bboxes
    -------

    """
    if char_spacing == -1:
        if font_text.horizontal:
            return _draw_text_on_bg_with_bboxes(font_text, text_color)
        else:
            char_spacing = 0

    chars_size = []
    widths = []
    heights = []

    for c in font_text.text:
        # Use getbbox() instead of deprecated getsize()
        bbox = font_text.font.getbbox(c)
        if bbox[2] > bbox[0]:
            size = (bbox[2] - bbox[0], max(bbox[3] - bbox[1], font_text.font.size))
        else:
            # Fallback for empty or invalid bbox
            size = (0, font_text.font.size)
        chars_size.append(size)
        widths.append(size[0])
        heights.append(size[1])

    if font_text.horizontal:
        width = sum(widths)
        height = max(heights)
    else:
        width = max(widths)
        height = sum(heights)

    char_spacings = []

    cs_height = font_text.size[1]

    if isinstance(char_spacing, list) or isinstance(char_spacing, tuple):
        sample_spacing = np.random.uniform(*char_spacing)
        sample_spacing_pixels = int(sample_spacing * cs_height)
    else:
        sample_spacing_pixels = int(char_spacing * cs_height)

    for i in range(len(font_text.text)):
        char = font_text.text[i]
        if char.isspace():
            char_spacings.append(0)
        else:
            char_spacings.append(sample_spacing_pixels)

    if font_text.horizontal:
        width += sum(char_spacings[:-1])
    else:
        height += sum(char_spacings[:-1])

    text_mask = transparent_img((width, height))
    draw = ImageDraw.Draw(text_mask)
    char_bboxes = []

    c_x = 0
    c_y = 0

    if font_text.horizontal:
        y_offset = font_text.offset[1]
        for i, c in enumerate(font_text.text):
            char_info = {"char": c}
            if not c.isspace():
                # Calculate tight bbox for non-space characters
                char_bbox = _get_tight_char_bbox(
                    font_text, c, c_x, c_y - y_offset, chars_size[i]
                )
                char_info["bbox"] = char_bbox
            char_bboxes.append(char_info)

            draw.text((c_x, c_y - y_offset), c, fill=text_color, font=font_text.font)
            c_x += chars_size[i][0] + char_spacings[i]
    else:
        x_offset = font_text.offset[0]
        for i, c in enumerate(font_text.text):
            char_info = {"char": c}
            if not c.isspace():
                # Calculate tight bbox for non-space characters
                char_bbox = _get_tight_char_bbox(
                    font_text, c, c_x - x_offset, c_y, chars_size[i]
                )
                char_info["bbox"] = char_bbox
            char_bboxes.append(char_info)

            draw.text((c_x - x_offset, c_y), c, fill=text_color, font=font_text.font)
            c_y += chars_size[i][1] + char_spacings[i]
        text_mask = text_mask.rotate(90, expand=True)

    return text_mask, char_bboxes


def _draw_text_on_bg_with_bboxes(
    font_text: FontText,
    text_color: Tuple[int, int, int, int] = (0, 0, 0, 255),
) -> Tuple[PILImage, list]:
    """
    Draw text and calculate character bboxes for text without spacing
    """
    text_width, text_height = font_text.size
    text_mask = transparent_img((text_width, text_height))
    draw = ImageDraw.Draw(text_mask)

    xy = font_text.xy
    x_offset, y_offset = xy

    # Calculate character bboxes
    char_bboxes = []
    current_x = 0

    for c in font_text.text:
        char_info = {"char": c}

        if not c.isspace():
            bbox = font_text.font.getbbox(c)
            char_width = bbox[2] - bbox[0] if bbox[2] > bbox[0] else 0
            char_height = (
                bbox[3] - bbox[1] if bbox[3] > bbox[1] else font_text.font.size
            )

            char_bbox = _get_tight_char_bbox(
                font_text, c, current_x + x_offset, y_offset, (char_width, char_height)
            )
            char_info["bbox"] = char_bbox
        else:
            bbox = font_text.font.getbbox(c)
            char_width = bbox[2] - bbox[0] if bbox[2] > bbox[0] else 0

        char_bboxes.append(char_info)
        current_x += char_width

    draw.text(
        xy,
        font_text.text,
        font=font_text.font,
        fill=text_color,
        anchor=None,
    )

    return text_mask, char_bboxes


def _get_tight_char_bbox(
    font_text: FontText, char: str, x: int, y: int, char_size: Tuple[int, int]
) -> list:
    """
    Calculate tight bounding box for a single character
    """
    char_width, char_height = char_size

    # Create a larger canvas to ensure we capture the full character
    padding = 5
    canvas_width = char_width + 2 * padding
    canvas_height = char_height + 2 * padding

    char_mask = Image.new("L", (canvas_width, canvas_height), 0)
    char_draw = ImageDraw.Draw(char_mask)
    char_draw.text((padding, padding), char, fill=255, font=font_text.font)

    mask_array = np.array(char_mask)

    if np.any(mask_array > 0):
        coords = np.where(mask_array > 0)
        min_y, max_y = int(coords[0].min()), int(coords[0].max())
        min_x, max_x = int(coords[1].min()), int(coords[1].max())

        # Remove padding offset and add global position
        x1, y1 = int(x + min_x - padding), int(y + min_y - padding)
        x2, y2 = int(x + max_x - padding), int(y + min_y - padding)
        x3, y3 = int(x + max_x - padding), int(y + max_y - padding)
        x4, y4 = int(x + min_x - padding), int(y + max_y - padding)

        return [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    else:
        return [
            [int(x), int(y)],
            [int(x + char_width), int(y)],
            [int(x + char_width), int(y + char_height)],
            [int(x), int(y + char_height)],
        ]
