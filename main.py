"""Código principal del programa."""
from fpdf import FPDF

nombre = input("Ingrese su maquina: ")

# Código del formato de OT's
class OT(FPDF):
  def header(self):
    self.image("LOGO_TEC_PNG_OK-2534661981.png", 10, 8, 33)
    self.set_font("helvetica", style="B", size=15)
    self.cell(80)
    self.cell(30, 10, "ORDEN DE TRABAJO DE MANTENIMIENTO", 1, align="C")
    self.ln(30)
  def llenar_datos_equipos(self, nombre, codigo):
    self.set_font("helvetica", size=12)
    self.cell(0, 10, f"Nombre del equipo: {nombre}.")
    self.ln()
    self.cell(0, 10, f"Código del equipo: {codigo}.")
    self.ln(10)
    self.cell(0, 10, "Actividades a realizar:")
    self.ln()
    self.cell(0, 40, "", border=1)
    self.ln()
  def footer(self):
    self.set_y(-15)
    self.set_font("helvetica", style="I", size=8)
    self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")

pdf=OT(orientation="P", unit="mm", format="A4")
pdf.add_page()
pdf.llenar_datos_equipos(nombre="Torre de enfriamiento", codigo="SER-02")
pdf.output("data/OT.pdf")
