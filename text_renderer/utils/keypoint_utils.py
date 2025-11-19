from typing import Any, Dict, List, Optional, Tuple


def char_bboxes_to_keypoints(
    char_bboxes: List[Dict[str, Any]]
) -> List[Tuple[float, float]]:
    """
    Convert character bounding boxes to keypoints for albumentations.

    Each character bbox is a quadrilateral with 4 corner points.
    We convert each corner to a keypoint for albumentations processing.

    Args:
        char_bboxes: List of character bbox dictionaries with format:
                    [{"char": "A", "bbox": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]}, ...]

    Returns:
        List of (x, y) keypoints for albumentations
    """
    keypoints = []

    for char_info in char_bboxes:
        if 'bbox' in char_info and char_info['bbox']:
            bbox = char_info['bbox']
            # Add all 4 corners of the character bbox as keypoints
            for corner in bbox:
                keypoints.append((float(corner[0]), float(corner[1])))

    return keypoints


def keypoints_to_char_bboxes(
    keypoints: List[Tuple[float, float]], original_char_bboxes: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Convert transformed keypoints back to character bounding boxes.

    Args:
        keypoints: List of transformed (x, y) keypoints from albumentations
        original_char_bboxes: Original character bbox list for structure reference

    Returns:
        Updated character bboxes with transformed coordinates
    """
    updated_char_bboxes = []
    keypoint_idx = 0

    for char_info in original_char_bboxes:
        updated_char_info = char_info.copy()

        if 'bbox' in char_info and char_info['bbox']:
            # Extract 4 keypoints for this character's bbox
            if keypoint_idx + 3 < len(keypoints):
                new_bbox = []
                for i in range(4):
                    kp = keypoints[keypoint_idx + i]
                    new_bbox.append([int(round(kp[0])), int(round(kp[1]))])
                updated_char_info['bbox'] = new_bbox
                keypoint_idx += 4
            else:
                # If we don't have enough keypoints, keep original bbox
                updated_char_info['bbox'] = char_info['bbox']

        updated_char_bboxes.append(updated_char_info)

    return updated_char_bboxes


def update_char_bboxes_with_offset(
    char_bboxes: Optional[List[Dict[str, Any]]], x_offset: int = 0, y_offset: int = 0
) -> Optional[List[Dict[str, Any]]]:
    """
    Update character bounding boxes by applying x and y offsets to all coordinates.

    Args:
        char_bboxes: List of character bbox dictionaries
        x_offset: Horizontal offset to add to all x coordinates
        y_offset: Vertical offset to add to all y coordinates

    Returns:
        Updated character bboxes with offset applied, or None if input was None
    """
    if not char_bboxes:
        return char_bboxes

    updated_char_bboxes = []
    for char_info in char_bboxes:
        updated_char_info = char_info.copy()
        if 'bbox' in char_info and char_info['bbox']:
            updated_bbox = []
            for corner in char_info['bbox']:
                updated_bbox.append([corner[0] + x_offset, corner[1] + y_offset])
            updated_char_info['bbox'] = updated_bbox
        updated_char_bboxes.append(updated_char_info)

    return updated_char_bboxes
