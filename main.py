"""Código principal del programa."""
import datetime
import pytz
from fpdf import FPDF

nombre = input("Ingrese su maquina: ")

# Obtencion del tiempo actual
zona_mazatlan = pytz.timezone('America/Mazatlan')
Fecha_Actual = datetime.datetime.now(zona_mazatlan)

def obtener_fecha_actual():
  Fecha_Year = Fecha_Actual.year
  Fecha_Month = Fecha_Actual.month
  Fecha_Day = Fecha_Actual.day
  fechaOrdenada = f"{Fecha_Day}/{Fecha_Month}/{Fecha_Year}"

  return fechaOrdenada

def obtener_hora_actual():
  Hora_Second = Fecha_Actual.second
  Hora_Minute = Fecha_Actual.minute
  Hora_Hour = Fecha_Actual.hour
  horaOrdenada = f"{Hora_Hour}:{Hora_Minute}"

  return horaOrdenada

fechaActual = obtener_fecha_actual()
horaActual = obtener_hora_actual()

# Generación del formato de pdf
class OT(FPDF):
  def header(self):
    self.image("data/LOGO_TEC.png", 10, 8, 25)
    self.set_font("helvetica", style="B", size=15)
    self.cell(80)
    self.cell(30, 10, "DEPARTAMENTO DE MANTENIMIENTO", align="C")
    self.set_font(size=14)
    self.ln()
    self.cell(80)
    self.cell(30, 10, "FORMATO DE ORDEN DE TRABAJO", align="C")
    self.ln(20)
  def llenar_datos_equipos(self, nombre, codigo):
    self.set_font("helvetica", size=12)
    self.cell(30, 10, f"Fecha de expedición: {fechaActual} {horaActual}")
    self.ln()
    self.cell(0, 10, f"Nombre del equipo: {nombre}.")
    self.ln()
    self.cell(0, 10, f"Código del equipo: {codigo}.")
    self.ln(10)
    self.cell(0, 10, "Actividades a realizar:")
    self.ln()
    self.cell(0, 40, "", border=1)
    self.ln()
    self.cell(0, 10, "Observaciones:")
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
pdf.output(f"OT_{nombre}.pdf")