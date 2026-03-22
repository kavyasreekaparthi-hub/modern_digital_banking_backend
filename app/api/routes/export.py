from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.export_service import ExportService
from app.models.transaction import Transaction
from app.api.routes.auth import get_demo_user

router = APIRouter(prefix="/export", tags=["Data Export"])

@router.get("/transactions")
def export_transactions(format: str, db: Session = Depends(get_db)):
    user = get_demo_user(db)
    transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()

    if format.lower() == "csv":
        csv_data = ExportService.generate_transaction_csv(transactions)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=transactions.csv"}
        )
    
    elif format.lower() == "pdf":
        # Simplified insights for PDF demo
        insights = {"burn_rate": 45, "date": "2024-03-20"}
        pdf_buffer = ExportService.generate_summary_pdf(user.username, transactions, insights)
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=summary.pdf"}
        )