import csv
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from app.models.transaction import Transaction

class ExportService:
    @staticmethod
    def generate_transaction_csv(transactions):
        """Generates a CSV file in memory."""
        output = io.StringIO()
        writer = csv.writer(output)
        # Header
        writer.writerow(["ID", "Merchant", "Amount", "Category", "Date"])
        # Data
        for tx in transactions:
            writer.writerow([tx.id, tx.merchant, tx.amount, tx.category, tx.created_at])
        
        output.seek(0)
        return output.getvalue()

    @staticmethod
    def generate_summary_pdf(user_name, transactions, insights):
        """Generates a simple PDF summary."""
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("Helvetica-Bold", 16)
        
        p.drawString(100, 750, f"Financial Summary Report: {user_name}")
        p.setFont("Helvetica", 12)
        p.drawString(100, 730, f"Generated on: {insights.get('date')}")
        
        p.drawString(100, 700, "Insights Summary:")
        p.drawString(120, 680, f"- Burn Rate: {insights.get('burn_rate')}%")
        p.drawString(120, 660, f"- Total Transactions: {len(transactions)}")
        
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer