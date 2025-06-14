import os
import cv2

def create_template():
    print("\n🛠️ Template Creator")
    event_class = input("Enter event class name (e.g. kill): ").strip()

    try:
        # Define paths
        crop_path = os.path.join("data", "events", "crop", f"{event_class}_crop.png")
        mask_path = os.path.join("data", "events", "masks", f"{event_class}_mask.png")
        output_path = os.path.join("data", "events", "templates", f"{event_class}_template.png")

        # Load crop (in color) and mask (in grayscale)
        crop = cv2.imread(crop_path, cv2.IMREAD_COLOR)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

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
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, template)
        print(f"✅ Template saved to: {output_path}")
        input("Press Enter to continue...")

    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to continue...")
