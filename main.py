"""Código principal del programa."""
import os
import datetime
import pytz
from fpdf import FPDF
import pandas as pd
from pathlib import Path
def obtener_fecha_actual():
  Fecha_Year = Fecha_Actual.year
  Fecha_Month = Fecha_Actual.month
  Fecha_Day = Fecha_Actual.day
  fechaOrdenada = f"{Fecha_Year}-{Fecha_Month}-{Fecha_Day}"
  return fechaOrdenada
def obtener_hora_actual():
  Hora_Second = Fecha_Actual.second
  Hora_Minute = Fecha_Actual.minute
  Hora_Hour = Fecha_Actual.hour
  horaOrdenada = f"{Hora_Hour:02d}:{Hora_Minute:02d}"
  return horaOrdenada

#incompleto
def gen_estructura_carpetas():
  print("\n--- Creando carpetas con respecto a la base de datos... ---\n")
  carpeta_base = Path('ordenes_trabajo')
  for nombre_maquina in df_maqs["maquina"].intertuples().unique:
    nombre_maquina = f"{nombre_maquina.codigo}_{nombre_maquina.maquina}"
    ruta_carpeta = carpeta_base / nombre_maquina
    ruta_carpeta.mkdir(parents=True, exist_ok=True)

def generar_folio():
  archivo_historial = "historial_ots.csv"
  if not os.path.exists(archivo_historial) or os.stat(archivo_historial).st_size == 0:
    return 1
  else:
    df_historial = pd.read_csv(archivo_historial)
    if df_historial.empty:
      return 1
    ultimo_folio = df_historial["folio"].max()
    nuevo_folio = ultimo_folio + 1
    return nuevo_folio
      
class OT(FPDF):
  def header(self):
    self.image("data/logo.png", 10, 8, 25)
    self.set_font("helvetica", style="B", size=15)
    self.cell(80)
    self.cell(30, 10, "DEPARTAMENTO DE MANTENIMIENTO", align="C")
    self.set_font(size=14)
    self.ln()
    self.cell(80)
    self.cell(30, 10, "FORMATO DE ORDEN DE TRABAJO", align="C")
    self.ln(20)
  def llenar_datos_equipos(self, nombre_maquina, codigo_input):
    ancho_util = self.w-2*(self.l_margin)
    ancho_firma = 70
    espacio =(ancho_util-(2*ancho_firma))/3
    self.set_font("helvetica", size=12)
    self.cell(0, 10, f"Número de folio: {folio_pdf}")
    self.ln()
    self.cell(0, 10, f"Fecha de expedición: {fechaActual}  {horaActual}")
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
    self.ln(45)

    self.set_x(self.l_margin + espacio)
    self.cell(ancho_firma,10,"Verificado por:", align="C")
    self.set_x(self.get_x() + espacio)
    self.cell(ancho_firma,10,"Solicitado por:", align="C")
    self.ln(20)
    self.set_font("helvetica", size =11)
    self.set_x(self.l_margin + espacio)
    self.cell(ancho_firma,10,"",border="T", align="C")
    self.set_x(self.get_x() + espacio)
    self.cell(ancho_firma,10,"",border="T", align="C")
    self.ln(5)

    self.set_x(self.l_margin + espacio)
    self.cell(ancho_firma,10,"Nombre y firma del técnico", align="C")
    self.set_x(self.get_x() + espacio)
    self.cell(ancho_firma,10,"Nombre y Firma del(a)", align="C")
    self.ln(7)
    self.set_x(self.l_margin + espacio + ancho_firma + espacio)
    self.cell(ancho_firma,10,"Jefe(a) del Área solicitante", align="C")
    self.ln(10)
    self.set_x(self.l_margin + espacio)
    self.cell(ancho_firma,10,"Aprobado por:", align="C")
    self.ln(20)
    self.set_x(self.get_x() + espacio)
    self.cell(ancho_firma,10,"",border="T", align="C")
    self.ln(5)
    self.set_x(self.get_x() + espacio)
    self.cell(ancho_firma,10,"Nombre y Firma del supervisor", align="C")
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
df_maqs = pd.read_csv("data/maquinas.csv")
codigo_input = input("Ingresé el código de la máquina de interés: ").strip().upper()
print(f"Código ingresado: {codigo_input}")
tareas_maquina = df_maqs[df_maqs['codigo'] == codigo_input]
if tareas_maquina.empty:
  print(f"Error: El código que ha ingresado ({codigo_input}) no coincide con la base de datos.")
else:
  nombre_maquina = tareas_maquina['maquina'].iloc[0]
  n_folio = generar_folio()
  folio_pdf = f"{n_folio:04d}"
  print(f"\n--- Preparando PDF para: {nombre_maquina} ({codigo_input}) ---\n")
  pdf=OT(orientation="P", unit="mm", format="A4")
  pdf.add_page()
  pdf.llenar_datos_equipos(nombre_maquina, codigo_input)
  ruta_ot = f"data/ordenes_trabajo/{folio_pdf}.pdf"
  pdf.output(ruta_ot)
  nueva_orden = pd.DataFrame([{
    'folio' : f"{folio_pdf}",
    'codigo_maquina' : codigo_input,
    'fecha_generacion' : fechaActual,
    'estado' : 'Generada',
    'ruta' : f"{ruta_ot}"
  }])
  nueva_orden.to_csv('historial_ots.csv', mode='a', header=not os.path.exists('historial_ots.csv'), index=False, encoding='utf-8')
  print("PDF generado exitosamente.")
