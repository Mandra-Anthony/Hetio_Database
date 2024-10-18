import tkinter as tk
from neo4j import GraphDatabase
from tkinter import messagebox
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
            MATCH (c:Compound)-[cr:CuG|CdG]->(g:Gene)  // Compound upregulates or downregulates genes
            MATCH (d:Disease {id: $disease_id})  // Use a parameter for the disease ID
            MATCH (d)-[dr:DdG|DuG]->(g)   // Disease upregulates or downregulates the same gene
            MATCH (d)-[:DlA]->(a:Anatomy)-[ar:AuG|AdG]->(g)  // Disease occurs in a specific anatomical location and anatomy upregulates or downregulates the same gene
            WHERE NOT (c)-[:CtD]->(d)  // Exclude existing treatment relationships
            AND (
                (cr:CuG AND ar:AdG AND dr: DdG) 
                OR (cr:CdG AND ar:AuG AND dr: DuG) // Ensure opposite regulation direction
            )
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
        self.label.pack()

        # Input Field for Disease
        self.disease_input = tk.Entry(root)
        self.disease_input.pack()

        # Button to Query Neo4j
        self.query_button = tk.Button(root, text="Find Compounds", command=self.query_db)
        self.query_button.pack()

        # Text Area to Display Results
        self.result_text = tk.Text(root, height=20, width=100)
        self.result_text.pack()

        # Label to Display Count of Compounds
        self.count_label = tk.Label(root, text="")
        self.count_label.pack()

    # Function to handle the query and display results
    def query_db(self):
        user_input = self.disease_input.get()
        if not user_input:
            messagebox.showwarning("Input Error", "Please enter a disease ID.")
            return

        # Normalize the disease ID format
        disease_id = self.normalize_disease_id(user_input)
        if disease_id is None:
            return

        try:
            results = self.db_app.find_compounds_for_disease(disease_id)
            self.result_text.delete(1.0, tk.END)  # Clear previous results
            # Clear the count label before updating it
            self.count_label.config(text="")

            if results:
                # Display results and count
                for compound, disease, gene in results:
                    self.result_text.insert(tk.END, f"Compound: {compound}, Disease: {disease}, Gene: {gene}\n")
                self.count_label.config(text=f"Total Compounds Found: {len(results)}")
            else:
                self.result_text.insert(tk.END, "No compounds found for this disease.\n")
                self.count_label.config(text="Total Compounds Found: 0")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # Function to normalize disease ID input
    def normalize_disease_id(self, input_id):
        # Remove any leading/trailing whitespaces
        input_id = input_id.strip()

        # Ensure format of "Disease::[A-Za-z]:[0-9]" (case insensitive for "Disease")
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
