from pymongo import MongoClient

MONGODB_URI = "mongodb+srv://jameefahim:bigdata@hetionet.q0qji.mongodb.net/?retryWrites=true&w=majority&appName=HetioNet"

# Connect to MongoDB
client = MongoClient(MONGODB_URI)

# Connect to the database 493
db = client["493"]

def get_disease_info(disease_id):
    print(f"Querying for disease ID: {disease_id} .....")  # Debug
    # Match the disease node by its ID and get the name
    disease = db.nodes.find_one({"id": disease_id, "kind": "Disease"}, {"name": 1, "_id": 0})
    if not disease:
        return {"error": f"No disease found with ID {disease_id}"}

    result = {
        "Disease Name": disease['name'],
        "Drugs": [],
        "Genes": [],
        "Anatomy": []
    }

    # Find drugs that treat (CtD) or palliate (CpD) the disease
    drug_edges = db.edges.find({"target": disease_id, "metaedge": {"$in": ["CtD", "CpD"]}})
    for edge in drug_edges:
        compound = db.nodes.find_one({"id": edge["source"], "kind": "Compound"}, {"name": 1, "_id": 0})
        if compound:
            result["Drugs"].append(compound["name"])

    # Find genes that cause (DdG), upregulate (DuG), or associate (DaG) with the disease
    gene_edges = db.edges.find({"source": disease_id, "metaedge": {"$in": ["DdG", "DuG", "DaG"]}})
    for edge in gene_edges:
        gene = db.nodes.find_one({"id": edge["target"]}, {"name": 1, "_id": 0})
        if gene:
            result["Genes"].append(gene["name"])

    # Find the anatomy parts affected by the disease
    anatomy_edges = db.edges.find({"source": disease_id, "metaedge": "DlA"})
    for edge in anatomy_edges:
        anatomy = db.nodes.find_one({"id": edge["target"]}, {"name": 1, "_id": 0})
        if anatomy:
            result["Anatomy"].append(anatomy["name"])

    return result
