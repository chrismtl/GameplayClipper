import tkinter as tk
from tkinter import ttk, messagebox

from engine.detectors.events_detector import detect_all_videos, detect_single_video
from engine.translators.query_extractor import query
from engine.matchers.matcher_registry import get_match_functions_name
from tools.roi_selector import roi_selector
from tools.cropper import cropper
from tools.template_creator import create_template
from tools.clip_extractor import extract_clips

class GameplayClipperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎮 Gameplay Event Clipper")

        style = ttk.Style(self)
        style.theme_use("clam")

        # Set dark background colors
        style.configure(".", background="#2e2e2e", foreground="#ffffff")
        style.configure("TButton", background="#3a3a3a", foreground="#ffffff")
        style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
        style.configure("TFrame", background="#2e2e2e")

        self.sidebar = ttk.Frame(self, width=220)
        self.sidebar.pack_propagate(False)
        self.sidebar.configure(style="TFrame")
        self.sidebar.pack(side="left", fill="y")

        ttk.Separator(self, orient="vertical").pack(side="left", fill="y")

        self.main_area = ttk.Frame(self)
        self.main_area.configure(style="TFrame")
        self.main_area.pack(side="right", expand=True, fill="both")

        # Sidebar layout
        sbr_button_padx = 20

        # Detect section
        ttk.Label(self.sidebar, text="🧠 Detect", font=("Segoe UI", 12)).pack(pady=(15, 5), padx=sbr_button_padx, anchor="w")
        ttk.Button(self.sidebar, text="From All Videos", width=20, command=self.show_detect_all_page).pack(pady=2, padx=sbr_button_padx)
        ttk.Button(self.sidebar, text="From Specific Video", width=20, command=self.show_detect_single_page).pack(pady=2, padx=sbr_button_padx)

        # Extract section
        ttk.Label(self.sidebar, text="🎞️ Extract", font=("Segoe UI", 12)).pack(pady=(20, 5), padx=sbr_button_padx, anchor="w")
        ttk.Button(self.sidebar, text="Run Extraction", width=20, command=self.show_extract_page).pack(pady=2, padx=sbr_button_padx)

        # Query section
        ttk.Label(self.sidebar, text="🔍 Query", font=("Segoe UI", 12)).pack(pady=(20, 5), padx=sbr_button_padx, anchor="w")
        ttk.Button(self.sidebar, text="Run Query", width=20, command=self.show_query_page).pack(pady=2, padx=sbr_button_padx)

        # Create section
        ttk.Label(self.sidebar, text="📦 Create", font=("Segoe UI", 12)).pack(pady=(20, 5), padx=sbr_button_padx, anchor="w")
        ttk.Button(self.sidebar, text="Select ROI", width=20, command=self.show_create_roi_page).pack(pady=2, padx=sbr_button_padx)
        ttk.Button(self.sidebar, text="Crop from ROI", width=20, command=self.show_create_crop_page).pack(pady=2, padx=sbr_button_padx)
        ttk.Button(self.sidebar, text="Template from Mask", width=20, command=self.show_create_template_page).pack(pady=2, padx=sbr_button_padx)

        # Exit
        ttk.Button(self.sidebar, text="❌ Exit", width=20, command=self.destroy).pack(pady=30, padx=sbr_button_padx)

        # Page container
        self.pages = {
            "detect_all": self.create_empty_page("Detecting from All Videos..."),
            "detect_single": self.create_empty_page("Detecting from a Specific Video..."),
            "extract": self.create_empty_page("Extracting Clips..."),
            "query": self.create_empty_page("Querying Events..."),
            "create_roi": self.create_empty_page("Selecting ROI..."),
            "create_crop": self.create_empty_page("Cropping from ROI..."),
            "create_template": self.create_empty_page("Creating Template from Mask..."),
            "empty": self.create_empty_page("Welcome to the Gameplay Event Clipper"),
        }

        self.current_page = None
        self.switch_page("empty")
        self.state("zoomed")
        self.resizable(False, False)

    def create_empty_page(self, msg):
        frame = ttk.Frame(self.main_area)
        ttk.Label(frame, text=msg, font=("Segoe UI", 16)).pack(pady=40)
        return frame

    def switch_page(self, name):
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = self.pages[name]
        self.current_page.pack(fill="both", expand=True)

    # === Page Switchers ===

    def show_detect_all_page(self):
        self.run_detect_all()
        self.switch_page("detect_all")

    def show_detect_single_page(self):
        self.run_detect_single()
        self.switch_page("detect_single")

    def show_extract_page(self):
        self.run_extract()
        self.switch_page("extract")

    def show_query_page(self):
        self.run_query()
        self.switch_page("query")

    def show_create_roi_page(self):
        self.run_roi_selector()
        self.switch_page("create_roi")

    def show_create_crop_page(self):
        self.run_cropper()
        self.switch_page("create_crop")

    def show_create_template_page(self):
        self.run_template_creator()
        self.switch_page("create_template")

    # === Core Functions ===

    def run_detect_all(self):
        detect_all_videos()
        messagebox.showinfo("Done", "Detection from all videos completed.")

    def run_detect_single(self):
        detect_single_video()
        messagebox.showinfo("Done", "Detection from specific video completed.")

    def run_extract(self):
        extract_clips()
        messagebox.showinfo("Done", "Clip extraction completed.")

    def run_query(self):
        query()
        messagebox.showinfo("Done", "Query executed.")

    def run_roi_selector(self):
        roi_selector()
        messagebox.showinfo("Done", "ROI selection completed.")

    def run_cropper(self):
        cropper(get_match_functions_name())
        messagebox.showinfo("Done", "Crop from ROI completed.")

    def run_template_creator(self):
        create_template()
        messagebox.showinfo("Done", "Template from mask created.")

if __name__ == "__main__":
    app = GameplayClipperApp()
    app.mainloop()
