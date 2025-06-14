from matchers.template_matcher import match_template_mask, match_template_gray_no_mask

MATCH_FUNCTIONS = {
    "fixtemplate_rgb": match_template_mask,
    "fixtemplate_gray": match_template_gray_no_mask,
    # Add other strategies here, e.g.:
    # "colorblob": color_matcher.match_colorblob,
    # "ocr": ocr_matcher.match_ocr
}

def get_match_functions_name():
    return list(MATCH_FUNCTIONS.keys())