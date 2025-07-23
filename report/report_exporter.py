from fpdf import FPDF
from PIL import Image

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, "Volvo Sales & Inventory Report", ln=True, align='C')
        self.ln(5)

    def section_title(self, title):
        self.set_font("Arial", 'B', 14)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def paragraph(self, text):
        self.set_font("Arial", '', 12)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 8, text)
        self.ln()

def export_report(kpis: dict, insight_text: str, chart_paths: list, output_path: str):
    pdf = PDFReport()
    pdf.add_page()

    # --- KPIs Summary ---
    pdf.section_title("Key Performance Indicators")

    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Total Sales: {int(kpis['total_sales']):,}", ln=True)
    pdf.cell(0, 8, f"Revenue (£): {round(kpis['total_revenue']):,}", ln=True)
    pdf.cell(0, 8, f"Gross Profit (£): {round(kpis['gross_profit']):,}", ln=True)
    pdf.cell(0, 8, f"Inventory Value (£): {round(kpis['inventory_value']):,}", ln=True)

    pdf.ln(5)

    # --- Insight Text ---
    pdf.section_title("Insight Summary")
    pdf.paragraph(insight_text)

    # --- Charts ---
    pdf.section_title("Visual Charts")
    for chart_path in chart_paths:
        try:
            pdf.image(chart_path, w=170)
            pdf.ln(5)
        except Exception as e:
            pdf.paragraph(f"[Error displaying chart: {chart_path}] {e}")

    # Save PDF
    pdf.output(output_path)
