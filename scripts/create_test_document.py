from pathlib import Path

from reportlab.pdfgen import canvas


output_path = Path("data/raw/database_test.pdf")

pdf = canvas.Canvas(str(output_path))

pdf.drawString(
    72,
    750,
    "DATABASE TEST DOCUMENT"
)

pdf.drawString(
    72,
    720,
    "A relational database stores data in tables."
)

pdf.drawString(
    72,
    690,
    "Tables contain rows and columns."
)

pdf.drawString(
    72,
    660,
    "SQL is commonly used to query relational databases."
)

pdf.save()

print(f"Created: {output_path}")
