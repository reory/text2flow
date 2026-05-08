"""
Text2Flow GUI - Tkinter-based desktop application
Allows users to create and render flowcharts with SVG/PNG output
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import threading
import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.parser import parse_edges
from app.services.renderer import render_flowchart


class Text2FlowGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text2Flow - Flowchart Generator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        self.current_image = None
        self.current_edges = None
        
        # Create main layout
        self.create_widgets()
        
    def create_widgets(self):
        """Create GUI components"""
        
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=50)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title = tk.Label(
            header, 
            text="Text2Flow - Convert Text to Flowcharts", 
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title.pack(pady=10)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Input
        left_panel = tk.Frame(main_container, bg="white", relief=tk.SUNKEN, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        input_label = tk.Label(
            left_panel, 
            text="Input Text (use A -> B -> C format):",
            font=("Arial", 10, "bold"),
            bg="white"
        )
        input_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.text_input = scrolledtext.ScrolledText(
            left_panel,
            width=40,
            height=20,
            font=("Courier", 10),
            wrap=tk.WORD
        )
        self.text_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.text_input.insert(tk.END, "Start -> Process -> Decision\nDecision -> Success\nDecision -> Failure")
        
        # Control buttons
        button_frame = tk.Frame(left_panel, bg="white")
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        render_btn = tk.Button(
            button_frame,
            text="Render",
            command=self.render_flowchart,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8
        )
        render_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_input,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8
        )
        clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Right panel - Preview & Export
        right_panel = tk.Frame(main_container, bg="white", relief=tk.SUNKEN, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        preview_label = tk.Label(
            right_panel,
            text="Preview:",
            font=("Arial", 10, "bold"),
            bg="white"
        )
        preview_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Canvas for preview
        self.canvas = tk.Canvas(
            right_panel,
            bg="white",
            cursor="hand2",
            relief=tk.SUNKEN,
            bd=1
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Button-4>", self.on_mousewheel)
        self.canvas.bind("<Button-5>", self.on_mousewheel)
        
        # Export options
        export_frame = tk.Frame(right_panel, bg="white")
        export_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(export_frame, text="Export as:", font=("Arial", 9), bg="white").pack(side=tk.LEFT, padx=(0, 10))
        
        svg_btn = tk.Button(
            export_frame,
            text="Export SVG",
            command=lambda: self.export_diagram("svg"),
            bg="#3498db",
            fg="white",
            font=("Arial", 9),
            padx=10,
            pady=5
        )
        svg_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        png_btn = tk.Button(
            export_frame,
            text="Export PNG",
            command=lambda: self.export_diagram("png"),
            bg="#3498db",
            fg="white",
            font=("Arial", 9),
            padx=10,
            pady=5
        )
        png_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        pdf_btn = tk.Button(
            export_frame,
            text="Export PDF",
            command=lambda: self.export_diagram("pdf"),
            bg="#3498db",
            fg="white",
            font=("Arial", 9),
            padx=10,
            pady=5
        )
        pdf_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg="#ecf0f1",
            anchor=tk.W,
            padx=10,
            pady=5
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def render_flowchart(self):
        """Render flowchart in background thread"""
        text = self.text_input.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text")
            return
        
        # Run in background thread to keep UI responsive
        thread = threading.Thread(target=self._render_thread, args=(text,))
        thread.daemon = True
        thread.start()
        
    def _render_thread(self, text):
        """Background rendering thread"""
        try:
            self.status_var.set("Parsing...")
            self.root.update()
            
            edges = parse_edges(text)
            self.current_edges = edges
            
            self.status_var.set("Rendering...")
            self.root.update()
            
            # Render as SVG for display
            image_bytes = render_flowchart(edges, format="svg")
            
            # Convert SVG to display format
            self.display_svg(image_bytes)
            
            self.status_var.set(f"Successfully rendered {len(edges)} edges")
            self.root.update()
            
        except ValueError as e:
            messagebox.showerror("Parsing Error", str(e))
            self.status_var.set("Error: Parsing failed")
            self.root.update()
        except Exception as e:
            messagebox.showerror("Rendering Error", f"An error occurred:\n{str(e)}")
            self.status_var.set("Error: Rendering failed")
            self.root.update()
    
    def display_svg(self, svg_bytes):
        """Display SVG in canvas"""
        try:
            # Convert SVG to PNG for display
            svg_text = svg_bytes.decode('utf-8')
            
            # For now, display as text info about SVG
            # For full SVG rendering, you'd need to use cairosvg or similar
            self.canvas.delete("all")
            
            # Create a simple text display
            info_text = f"SVG Flowchart\n({len(svg_text)} bytes)"
            self.canvas.create_text(
                self.canvas.winfo_width() // 2,
                self.canvas.winfo_height() // 2,
                text=info_text,
                font=("Arial", 14),
                fill="#2c3e50"
            )
            
            # Store the SVG for export
            self.current_svg = svg_bytes
            self.status_var.set("✓ Rendered as SVG (ready to export)")
            
        except Exception as e:
            self.status_var.set(f"Display error: {str(e)}")
    
    def on_mousewheel(self, event):
        """Handle mouse wheel zoom"""
        pass  # Implement zoom if needed
    
    def export_diagram(self, format_type):
        """Export diagram to file"""
        if self.current_edges is None:
            messagebox.showwarning("No Diagram", "Please render a diagram first")
            return
        
        file_extensions = {
            "svg": ("SVG files", "*.svg"),
            "png": ("PNG files", "*.png"),
            "pdf": ("PDF files", "*.pdf")
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{format_type}",
            filetypes=[file_extensions[format_type], ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            self.status_var.set(f"Exporting as {format_type.upper()}...")
            self.root.update()
            
            image_bytes = render_flowchart(self.current_edges, format=format_type)
            
            with open(file_path, "wb") as f:
                f.write(image_bytes)
            
            messagebox.showinfo("Success", f"Diagram exported to:\n{file_path}")
            self.status_var.set(f"✓ Exported as {format_type.upper()}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")
            self.status_var.set("Export failed")
    
    def clear_input(self):
        """Clear input text"""
        self.text_input.delete("1.0", tk.END)
        self.canvas.delete("all")
        self.current_edges = None
        self.status_var.set("Ready")


def main():
    root = tk.Tk()
    Text2FlowGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
