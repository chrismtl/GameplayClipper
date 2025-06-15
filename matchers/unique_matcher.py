import os
import cv2
import numpy as np
import utils.image_cacher as imgc
from matchers.match_utils import increment_match_template_id, save_match_log
import data.constants as cst

def match_template_mask(frame_crop, glob_event_name, video_file_name, threshold=0.95):
    """
    Match a color template using a mask over a cropped region (in RBG color).

    Args:
        frame_crop (np.ndarray): RGB cropped frame region.
        event_name (str): Name of the event.
        threshold (float): Matching threshold.

    Returns:
        matched (bool): Whether the match exceeds threshold.
        score (float): Similarity score.
    """
    # Get event name without the game prefix
    event_name = glob_event_name.split("_", 1)[1]
    
    # Load template and mask
    template_path = os.path.join(cst.TEMPLATES_UNIQUE_DIR, f"{glob_event_name}_template.png")
    mask_path = os.path.join(cst.MASKS_DIR, f"{glob_event_name}_mask.png")

    # Load as color
    template = imgc.load(template_path, cv2.IMREAD_COLOR)
    mask = imgc.load(mask_path, cv2.IMREAD_GRAYSCALE)

    if template is None or mask is None:
        raise FileNotFoundError(f"Template or mask not found for event '{event_name}'")

    # Ensure size match
    if frame_crop.shape != template.shape:
        raise ValueError("Frame crop and template must be the same shape for this matching")

    # Apply the mask to both template and frame_crop
    mask_bool = mask > 0
    diff = (frame_crop.astype(np.float32) - template.astype(np.float32)) ** 2
    mask_3ch = np.repeat(mask_bool[:, :, None], 3, axis=2)
    mse = np.sum(diff[mask_3ch]) / (np.count_nonzero(mask_bool) * 3)

    score = 1.0 - (mse / (255.0**2))
    matched = score >= threshold

    # Save only if match is successful
    if matched:
        save_match_log(frame_crop, event_name, video_file_name)
        increment_match_template_id()        

    return matched, score, event_name

def match_template_gray_no_mask(frame_crop, glob_event_name, video_file_name, threshold=0.95):
    """
    Match a grayscale template against a cropped frame using SQDIFF.

    Args:
        frame_crop (np.ndarray): RGB cropped frame region.
        event_name (str): Event name to locate the template.
        video_file_name (str): Video name for logging.
        threshold (float): Match threshold (default: 0.95).

    Returns:
        matched (bool): True if score exceeds threshold.
        score (float): Similarity score (higher is better).
        event_name (str): Same as input.
    """
    # Get event name without the game prefix
    event_name = glob_event_name.split("_", 1)[1]
    
    # Load template
    template_path = os.path.join(cst.TEMPLATES_UNIQUE_DIR, f"{glob_event_name}_template.png")
    template_gray = imgc.load(template_path, cv2.IMREAD_GRAYSCALE)

    if template_gray is None:
        raise FileNotFoundError(f"Template not found for event '{glob_event_name}'")

    # Convert both to grayscale
    frame_gray = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2GRAY)
    # template_gray = cv2.cvtColor(template_color, cv2.COLOR_BGR2GRAY)

    if frame_gray.shape != template_gray.shape:
        print(f"Frame crop shape: {frame_gray.shape}, Template shape: {template_gray.shape}")
        raise ValueError("Frame crop and template must be the same shape")

    # Perform normalized squared difference matching (fastest method for same-size images)
    result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_SQDIFF_NORMED)

    # Get match value (should be a single value in this case)
    min_val, _, _, _ = cv2.minMaxLoc(result)    

    # Invert score: lower is better for TM_SQDIFF_NORMED
    score = 1.0 - min_val
    matched = score >= threshold

    if matched:
        save_match_log(frame_crop, event_name, video_file_name)
        increment_match_template_id()

    return matched, score, event_name