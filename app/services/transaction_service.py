import csv
import io
from sqlalchemy.orm import Session
from app.models.transaction import Transaction

async def handle_csv_upload(db: Session, file, account_id: int):
    # Read and decode the uploaded CSV file
    contents = await file.read()
    decoded = contents.decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))
    
    transactions = []
    for row in reader:
        # Create a new transaction object from the CSV row
        new_txn = Transaction(
            account_id=account_id,
            description=row['description'],
            amount=float(row['amount']),
            category=row['category'],
            transaction_date=row['date'] # Ensure this matches your Transaction model field name
        )
        db.add(new_txn)
        transactions.append(new_txn)
    
    # Commit all new transactions to the database
    db.commit()
    
    return {"message": f"Successfully imported {len(transactions)} transactions"}