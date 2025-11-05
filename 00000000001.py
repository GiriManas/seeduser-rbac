import pickle

# ✅ Save
with open("transactions_by_account.pkl", "wb") as f:
    pickle.dump(transactions_by_account, f)

# ✅ Load later
with open("transactions_by_account.pkl", "rb") as f:
    transactions_by_account = pickle.load(f)