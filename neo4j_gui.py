import tkinter as tk
from neo4j import GraphDatabase
from tkinter import messagebox, scrolledtext
import re


# Neo4j connection
class Neo4jApp:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # Function to find compounds that can treat diseases (Example query)
    def find_compounds_for_disease(self, disease_id):
        with self.driver.session() as session:
            query = """
            MATCH (c:Compound)-[cr:CuG|CdG]->(g:Gene)
            MATCH (d:Disease {id: $disease_id})  // Use a parameter for the disease ID
            WHERE NOT (c)-[:CtD]->(d)  // Exclude existing treatment relationships
            MATCH (d)-[dr:DaG|DuG|DdG]->(g)  // Find relationships between the disease and genes
            RETURN DISTINCT c.name AS Compound, d.name AS Disease, g.name AS Target_Gene
            """
            result = session.run(query, disease_id=disease_id)
            compounds = [(record["Compound"], record["Disease"], record["Target_Gene"]) for record in result]
            return compounds


# GUI Setup
class Neo4jGUI:

    def __init__(self, root, db_app):
        self.db_app = db_app
        self.root = root
        self.root.title("Neo4j Hetio_Database GUI")

        # Label for Disease Input
        self.label = tk.Label(root, text="Enter Disease ID:")
        self.label.pack(pady=5)

        # Input Field for Disease
        self.disease_input = tk.Entry(root, width=50)
        self.disease_input.pack(pady=5)

        # Button to Query Neo4j
        self.query_button = tk.Button(root, text="Find Compounds", command=self.query_db)
        self.query_button.pack()

        frame = tk.Frame(root)
        frame.pack(pady=5, fill=tk.BOTH, expand=True)

        # Text Area to Display Results
        self.result_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=100, width=100)
        self.result_text.pack()

    # Function to handle the query and display results
    def query_db(self):
        user_input = self.disease_input.get()
        if not user_input:
            messagebox.showwarning("Input Error", "Please enter a disease ID.")
            return

        # Normalize the disease ID format
        disease_id = self.normalize_disease_id(user_input)

        try:
            results = self.db_app.find_compounds_for_disease(disease_id)
            self.result_text.delete(1.0, tk.END)  # Clear previous results
            if results:
                for compound, disease, gene in results:
                    self.result_text.insert(tk.END, f"Compound: {compound}, Disease: {disease}, Gene: {gene}\n")
            else:
                self.result_text.insert(tk.END, "No compounds found for this disease.\n")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # Function to normalize disease ID input
    def normalize_disease_id(self, input_id):
        # Remove any leading/trailing whitespaces
        input_id = input_id.strip()

        # Ensure format of "Disease::[A-Za-z]:[0-9]" (case insensitive for "Disease")
        # This will ensure that the disease part is capitalized, while the rest follows the pattern.
        match = re.match(r"([a-zA-Z]+)::([a-zA-Z]+):(\d+)", input_id)
        if match:
            disease = match.group(1).capitalize()
            alpha_part = match.group(2)
            number_part = match.group(3)
            normalized_id = f"{disease}::{alpha_part}:{number_part}"
            return normalized_id
        else:
            messagebox.showerror("Input Error", "Invalid Disease ID format.")
            return None


if __name__ == "__main__":
    # Create Neo4j connection
    uri = "neo4j+s://c98ca196.databases.neo4j.io"  # Change to your Neo4j instance
    user = "neo4j"  # Your Neo4j username
    password = "nvuNsT8Rg2uHyykjoICaNmYEU45FkWciX45pmkMYob8"  # Your Neo4j password

    # Initialize the Neo4j database connection
    app = Neo4jApp(uri, user, password)

    # Initialize the GUI
    root = tk.Tk()
    gui = Neo4jGUI(root, app)
    root.mainloop()

    # Close the Neo4j connection when done
    app.close()