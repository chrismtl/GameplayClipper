import matchers.unique_matcher as um
import matchers.switch_matcher as sm
 
MATCH_FUNCTIONS = {
    "fixtemplate_rgb": um.match_template_mask,
    "fixtemplate_gray": um.match_template_gray_no_mask,
    "switch": sm.match_switch,
    # Add other strategies here, e.g.:
    # "colorblob": color_matcher.match_colorblob,
    # "ocr": ocr_matcher.match_ocr
}

def get_match_functions_name():
    return list(MATCH_FUNCTIONS.keys())