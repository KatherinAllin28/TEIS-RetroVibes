from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO

class ReceiptGenerator:
    def generate(self, context):
        html = render_to_string("pdf/receipt_template.html", context)
        pdf_file = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)
        if pisa_status.err:
            return None
        pdf_file.seek(0)
        return pdf_file
