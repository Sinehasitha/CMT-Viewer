# 20/ENG/133 Sithamparam S.
import json
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

# Functions 
def show_category_dropdown():
    category_label.pack(pady=(20, 5))
    category_dropdown.pack(pady=5)

def on_category_selected(event):
    selected = category_var.get()
    open_subtopic_window(selected)

def open_subtopic_window(category):
    new_win = Toplevel(root)
    new_win.title(f"CMT Explorer – {category}")
    new_win.geometry("950x680")
    new_win.configure(bg="#FFFFFF")

    header = Frame(new_win, bg="#004080")
    header.pack(fill=X)
    Label(header, text=f"🧠 CMT Tree Viewer - {category}", font=("Calibri", 20, "bold"), bg="#004080", fg="white").pack(pady=10)

    content = Frame(new_win, bg="white")
    content.pack(fill=BOTH, expand=True, padx=20, pady=20)

    if category in ["Diseases", "Drugs", "Anatomy", "Diagnostic Techniques"]:
        Label(content, text=f"Select a {category[:-1]}:", font=("Calibri", 12), bg="white").pack(anchor=W)

        json_files = {
            "Diseases": "C:\\Users\\DELL\\.vscode\\medical informatics\\disease_icd.json", #ICD_Source
            "Drugs": "C:\\Users\\DELL\\.vscode\\medical informatics\\drug_tree.json", #RXNorm_Source
            "Anatomy": "C:\\Users\\DELL\\.vscode\\medical informatics\\anatomy_combined_tree.json", #SNOMED_Source
            "Diagnostic Techniques": "C:\\Users\\DELL\\.vscode\\medical informatics\\diagnostic_techniques_combined.json" #SNOMED_Source
        }

        try:
            with open(json_files[category], "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                data = raw_data.get(category, raw_data)  # if top-level key is missing, use entire file
        except Exception as e:
            Label(content, text=f"Error loading {category.lower()} data: {e}", fg="red", bg="white").pack()
            return

        selected_item = StringVar()
        item_dropdown = ttk.Combobox(content, textvariable=selected_item, state="readonly", font=("Calibri", 11), width=40)
        item_dropdown['values'] = list(data.keys())
        item_dropdown.pack(pady=10, anchor=W)

        tree_frame = Frame(content)
        tree_frame.pack(expand=True, fill="both")

        tree = ttk.Treeview(tree_frame)
        tree.pack(expand=True, fill="both")

        def build_tree(tree_widget, parent, items):
            for item in items:
                title = item.get("title", "Untitled")
                code = item.get("code", "")
                label = f"{code} - {title}" if code else title
                node = tree_widget.insert(parent, 'end', text=label)
                if "children" in item:
                    build_tree(tree_widget, node, item["children"])

        def load_selected_tree(event):
            tree.delete(*tree.get_children())
            name = selected_item.get()
            items = data.get(name, [])
            if isinstance(items, dict):
                items = list(items.values())
            if items:
                build_tree(tree, "", items)
            else:
                tree.insert("", "end", text="⚠ No data found for this selection.")

        item_dropdown.bind("<<ComboboxSelected>>", load_selected_tree)

# GUI Window Setup 
root = Tk()
root.title("CMT Viewer - Medical Informatics Project")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg="#E6F2FA")
root.iconbitmap("C:\\Users\\DELL\\.vscode\\medical informatics\\med.ico")

# Title
Label(root, text="Welcome to the Controlled Medical Terminology Viewer!",
      font=("Calibri", 24, "bold"), bg="#E6F2FA", fg="black").pack(pady=(20, 10))
Label(root, text="Explore unique clinical categories with structured medical knowledge.",
      font=("Calibri", 11), bg="#E6F2FA", fg="#333333").pack()

# Show category button
Button(root, text="Start Exploring!", font=("Arial", 12, "bold"),
       bg="#003366", fg="white", command=show_category_dropdown).pack(pady=20)

# Dropdown for category selection
category_label = Label(root, text="Select a Category:", font=("Arial", 12), bg="#E6F2FA")
category_var = StringVar()
category_dropdown = ttk.Combobox(root, textvariable=category_var, state="readonly", font=("Arial", 11))
category_dropdown['values'] = ["Anatomy", "Diseases", "Drugs", "Diagnostic Techniques"]
category_dropdown.bind("<<ComboboxSelected>>", on_category_selected)

# Footer image
try:
    footer_img = Image.open("C:\\Users\\DELL\\.vscode\\medical informatics\\medic.png")
    footer_img = footer_img.resize((600, 400))
    footer_photo = ImageTk.PhotoImage(footer_img)
    img_label = Label(root, image=footer_photo, bg="#E6F2FA")
    img_label.pack(side="bottom", pady=10)
except:
    pass

root.mainloop()
