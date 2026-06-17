"""
Text2Flow GUI - Tkinter-based desktop application
Allows users to create and render flowcharts with SVG/PNG output
"""

import tkinter as tk
import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui_app.app import Text2FlowGUI


def main():
    """Entry point for GUI application"""
    root = tk.Tk()
    Text2FlowGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
