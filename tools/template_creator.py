import os
import cv2
import utils.image_cacher as imgc
import utils.constants as cst

def create_template():
    print("\n🛠️ Template Creator")
    while True:
        event_name = input("Enter event name (e.g. kill): ").strip()
        parts = event_name.split("_", 1)
        if len(parts)==2:
            game_name, _ = parts
            break
        print("❌ Invalid event name...")
    try:
        # Define paths
        crop_path = os.path.join("data", game_name, cst.CROPS_DIR, f"{event_name}_crop.png")
        mask_path = os.path.join("data", game_name, cst.MASKS_DIR, f"{event_name}_mask.png")

        # Load crop (in color) and mask (in grayscale)
        crop = imgc.load(crop_path, cv2.IMREAD_COLOR)
        mask = imgc.load(mask_path, cv2.IMREAD_GRAYSCALE)

        if crop is None:
            raise FileNotFoundError(f"Crop not found: {crop_path}")
        if mask is None:
            raise FileNotFoundError(f"Mask not found: {mask_path}")

        if crop.shape[:2] != mask.shape:
            raise ValueError("❌ Crop and mask must be the same height and width!")

        # Apply mask to each channel
        template = cv2.bitwise_and(crop, crop, mask=mask)

        # Show images
        cv2.imshow("Crop (Color)", crop)
        cv2.imshow("Mask (Grayscale)", mask)
        cv2.imshow("Template (Masked Color)", template)
        print("🖼️ Showing images... Press any key in the image window to continue.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Save result
        output_path = os.path.join("data", game_name, cst.TEMPLATES_UNIQUE_DIR, f"{event_name}_template.png")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, template)
        print(f"✅ Template saved to: {output_path}")
        input("Press Enter to continue...")

    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to continue...")
