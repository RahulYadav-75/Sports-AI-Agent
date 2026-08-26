import chromadb
client = chromadb.PersistentClient(
    path="chroma_db"
)
collection = client.get_or_create_collection(
    name="sports_facts"
)
def add_facts():
    facts = [
        "Australia won the 2023 Cricket World Cup.",
        "India won the 2011 Cricket World Cup.",
        "Brazil has won the FIFA World Cup five times.",
        "Argentina won the FIFA World Cup in 2022.",
        "Serena Williams won 23 Grand Slam singles titles.",
        "Novak Djokovic has won multiple Grand Slam singles titles.",
        "Michael Jordan won six NBA championships with the Chicago Bulls.",
        "Usain Bolt holds world records in the 100 metres and 200 metres.",
        "PV Sindhu won an Olympic silver medal in badminton at Rio 2016.",
        "Rafael Nadal won 14 French Open men's singles titles."
    ]
    ids = [
        f"sports_fact_{i}"
        for i in range(len(facts))
    ]
    collection.upsert(
        documents=facts,
        ids=ids
    )
def search_chroma(query, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0]
if __name__ == "__main__":
    add_facts()
    print("Sports facts added to ChromaDB!")