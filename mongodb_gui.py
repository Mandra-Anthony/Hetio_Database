import tkinter as tk
from tkinter import messagebox, scrolledtext
from mongodb_queries import get_disease_info


def search_disease():
    disease_id = entry.get().strip()

    disease_id_parts = disease_id.split("::")
    if len(disease_id_parts) != 2 or ':' not in disease_id_parts[1]:
        messagebox.showerror("Error", "Please enter a valid Disease ID")
        return

    disease_part = disease_id_parts[0].capitalize()
    alpha_numeric_part = disease_id_parts[1].split(':')

    if len(alpha_numeric_part) != 2:
        messagebox.showerror("Error", "Please enter a valid Disease ID")
        return

    alpha_part = alpha_numeric_part[0].upper()
    numeric_part = alpha_numeric_part[1]

    if disease_part != "Disease" or not alpha_part.isalpha() or not (
            2 <= len(numeric_part) <= 7) or not numeric_part.isdigit():
        messagebox.showerror("Error", "Please enter a valid Disease ID")
        return

    normalized_disease_id = f"{disease_part}::{alpha_part}:{numeric_part}"
    print(f"Normalized Disease ID: {normalized_disease_id} .....")  # Debug

    result = get_disease_info(normalized_disease_id)
    if "error" in result:
        messagebox.showerror("Error", result["error"])
        return

    text_result.delete(1.0, tk.END)
    text_result.insert(tk.END, f"Disease Name: {result['Disease Name']}\n")
    print(f"Disease Name: {result['Disease Name']}\n")  # Debug

    text_result.insert(tk.END, "\nDrugs that treat or palliate the disease:\n")
    if not result["Drugs"]:
        text_result.insert(tk.END, "  - No drugs found\n")
    else:
        for i in range(len(result["Drugs"])):
            text_result.insert(tk.END, f"  {i + 1}. {result['Drugs'][i]}\n")

    text_result.insert(tk.END, "\nGenes that cause, upregulate, or associate with the disease:\n")
    if not result["Genes"]:
        text_result.insert(tk.END, "  - No genes found\n")
    else:
        for i in range(len(result["Genes"])):
            text_result.insert(tk.END, f"  {i + 1}. {result['Genes'][i]}\n")

    text_result.insert(tk.END, "\nAnatomy parts affected by the disease:\n")
    if not result["Anatomy"]:
        text_result.insert(tk.END, "  - No anatomy parts found\n")
    else:
        for i in range(len(result["Anatomy"])):
            text_result.insert(tk.END, f"  {i + 1}. {result['Anatomy'][i]}\n")


root = tk.Tk()
root.title("HetioNet")
root.iconphoto(False, tk.PhotoImage(file="icon.png")) # Icon

tk.Label(root, text="Enter Disease ID:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

tk.Button(root, text="Search", command=search_disease).pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=5, fill=tk.BOTH, expand=True)

# text widget
text_result = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=20, width=80)
text_result.pack(pady=5, fill=tk.BOTH, expand=True)

root.mainloop()
