"""Código principal del programa."""
import datetime
import pytz
from fpdf import FPDF
import pandas as pd
import datetime
import pytz
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
  horaOrdenada = f"{Hora_Hour:02d}:{Hora_Minute:02d}"
  return horaOrdenada
def generar_folio(codigo_maq):
    fecha = Fecha_Actual.now(zona_mazatlan).strftime("%Y%m%d%H%M")
    return f"OT-{codigo_maq}-{fecha}"
class OT(FPDF):
  def header(self):
    self.image("https://raw.githubusercontent.com/jorzazul/mantenituchi/refs/heads/main/data/LOGO_TEC.png", 10, 8, 25)
    self.set_font("helvetica", style="B", size=15)
    self.cell(80)
    self.cell(30, 10, "DEPARTAMENTO DE MANTENIMIENTO", align="C")
    self.set_font(size=14)
    self.ln()
    self.cell(80)
    self.cell(30, 10, "FORMATO DE ORDEN DE TRABAJO", align="C")
    self.ln(20)
  def llenar_datos_equipos(self, nombre_maquina, codigo_input):
    self.set_font("helvetica", size=12)
    self.cell(0, 10, f"Número de folio: {folio_ot}")
    self.ln()
    self.cell(0, 10, f"Fecha de expedición: {fechaActual} {horaActual}")
    self.ln()
    self.cell(0, 10, f"Nombre del equipo: {nombre_maquina}.")
    self.ln()
    self.cell(0, 10, f"Código del equipo: {codigo_input}.")
    self.ln(10)
    self.cell(0, 10, "Actividades a realizar:")
    self.ln()
    self.cell(0, 40, f"Variable", border=1)
    self.ln()
    self.cell(0, 10, "Observaciones:")
    self.ln()
    self.cell(0, 40, "", border=1)
    self.ln(65)
    self.set_font("helvetica", size =11)
    ancho_util = self.w-2*(self.l_margin)
    ancho_firma = 70
    espacio =(ancho_util-(2*ancho_firma))/3
    self.set_x(self.l_margin + espacio)
    self.cell(ancho_firma,10,"",border="T", align="C")
    self.set_x(self.get_x() + espacio)
    self.cell(ancho_firma,10,"",border="T", align="C")
    self.ln(5)
    self.set_x(self.l_margin + espacio)
    self.cell(ancho_firma,10,"Nombre y firma del técnico", align="C")
    self.set_x(self.get_x() + espacio)
    self.cell(ancho_firma,10,"Nombre y Firma del solicitante", align="C")
    self.ln()
  def footer(self):
    self.set_y(-15)
    self.set_font("helvetica", style="I", size=8)
    self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")
# Declaración de variables
zona_mazatlan = pytz.timezone('America/Mazatlan')
Fecha_Actual = datetime.datetime.now(zona_mazatlan)
fechaActual = obtener_fecha_actual()
horaActual = obtener_hora_actual()
# Ingreso de datos
df_maqs = pd.read_csv("https://raw.githubusercontent.com/jorzazul/mantenituchi/refs/heads/main/data/maquinas.csv")
codigo_input = input("Ingresé el código de la máquina de interés: ").strip().upper()
print(f"Código ingresado: {codigo_input}")
tareas_maquina = df_maqs[df_maqs['codigo'] == codigo_input]
if tareas_maquina.empty:
  print(f"Error: El código que ha ingresado ({codigo_input}) no coincide con la base de datos.")
else:
  nombre_maquina = tareas_maquina['maquina'].iloc[0]
  print(f"\n--- Preparando PDF para: {nombre_maquina} ({codigo_input}) ---\n")
  folio_ot = generar_folio(codigo_input)
  pdf=OT(orientation="P", unit="mm", format="A4")
  pdf.add_page()
  pdf.llenar_datos_equipos(nombre_maquina, codigo_input)
  pdf.output(f"{folio_ot}.pdf")
  print("PDF generado exitosamente.")
