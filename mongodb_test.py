from pymongo import MongoClient


MONGODB_URI = "mongodb+srv://jameefahim:bigdata@hetionet.q0qji.mongodb.net/?retryWrites=true&w=majority&appName=HetioNet"

# Connect to MongoDB
client = MongoClient(MONGODB_URI)

# Connect to the database
db = client["493"]


def get_disease_info(db, disease_id):
    # Match the disease node by its ID and get the name
    disease = db.nodes.find_one(
        {"id": disease_id, "kind": "Disease"}, {"name": 1, "_id": 0}
    )
    if not disease:
        return f"No disease found with ID {disease_id}"

    # Print the Disease Name
    print(f"Disease Name: {disease['name']}")

    # Metaedges to find drugs that treat (CtD) or palliate (CpD) the disease
    drug_edges = db.edges.find(
        {"target": disease_id, "metaedge": {"$in": ["CtD", "CpD"]}}
    )
    drug_names = set()
    for edge in drug_edges:
        # Retrieve compound ID
        compound = db.nodes.find_one(
            {"id": edge["source"], "kind": "Compound"}, {"name": 1, "_id": 0}
        )
        if compound:
            drug_names.add(compound["name"])

    print("Drugs that treat or palliate the disease:")
    if not drug_names:
        print("  - No drugs found")
    else:
        for drug in drug_names:
            print(f"  - {drug}")

    # Metaedges to find genes
    gene_edges = db.edges.find(
        {"source": disease_id, "metaedge": {"$in": ["DdG", "DuG", "DaG"]}}
    )
    gene_names = set()
    for edge in gene_edges:
        gene = db.nodes.find_one({"id": edge["target"]}, {"name": 1, "_id": 0})
        if gene:
            gene_names.add(gene["name"])

    print("Genes that cause, upregulate, or associate with the disease:")
    for gene in gene_names:
        print(f"  - {gene}")

    # Finds the anatomy parts affected by the disease
    anatomy_edges = db.edges.find({"source": disease_id, "metaedge": "DlA"})
    anatomy_names = set()
    for edge in anatomy_edges:
        anatomy = db.nodes.find_one({"id": edge["target"]}, {"name": 1, "_id": 0})
        if anatomy:
            anatomy_names.add(anatomy["name"])

    print("Anatomy parts affected by the disease:")
    for anatomy in anatomy_names:
        print(f"  - {anatomy}")


# Execute
disease_id = "Disease::DOID:1686" # TODO: Only the Number
get_disease_info(db, disease_id)

