import os
from engine.events_detector import detect_all_videos, detect_single_video
from engine.query_extractor import query
from matchers.matcher_registry import get_match_functions_name
from tools.roi_selector import roi_selector
from tools.cropper import cropper
from tools.template_creator import create_template
from tools.clip_extractor import extract_clips

def detect_events_menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n🧠 DETECT EVENTS")
        print("1) Detect from all videos")
        print("2) Detect from specific video")
        print("3) Back to Main Menu")

        choice = input(">> ").strip()

        if choice == "1":
            detect_all_videos()
        elif choice == "2":
            detect_single_video()
        elif choice == "3":
            print("🔙 Returning to main menu...")
            break
        else:
            print("❌ Invalid choice.")
        
        input("Press Enter to continue...")

def create_event_menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n📦 CREATE EVENT")
        print("1) Select ROI")
        print("2) Create crop from ROI")
        print("3) Create template from mask")
        print("4) Back to Main Menu")
        choice = input(">> ").strip()

        if choice == "1":
            roi_selector()
        elif choice == "2":
            match_fn_list = get_match_functions_name()  # Assuming this function is defined to get the list of match functions
            cropper(match_fn_list)
        elif choice == "3":
            create_template()
        elif choice == "4":
            print("🔙 Returning to main menu...")
            break
        else:
            print("❌ Invalid choice.")
            input("Press Enter to continue...")

def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n🎮 GAMEPLAY EVENT CLIPPER")
        print("1) Detect")
        print("2) Extract")
        print("3) Query")
        print("4) Create")
        print("5) Exit")
        print("\nAction: ")
        choice = input(">> ").strip()

        if choice == "1":
            detect_events_menu()
        elif choice == "2":
            extract_clips()
        elif choice == "3":
            query()
        elif choice == "4":
            create_event_menu()
        elif choice == "5":
            os.system("cls" if os.name == "nt" else "clear")
            print("👋 Exiting...")
            break
        else:
            input("❌ 1 to 5 only.")

if __name__ == "__main__":
    main()
