#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de PDF con marcadores AR
Crea un PDF con los marcadores 0-6 en formato 3x3_HAMMING63
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import os

# Configuración
PDF_OUTPUT = "marcadores-ar-imprimir.pdf"
MARKERS_DIR = "marcadores"
PAGE_WIDTH, PAGE_HEIGHT = A4

# Crear el canvas del PDF
c = canvas.Canvas(PDF_OUTPUT, pagesize=A4)

# Título
c.setFont("Helvetica-Bold", 18)
c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 30*mm, "MARCADORES AR - 3x3 HAMMING63")

c.setFont("Helvetica", 10)
c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 40*mm, "Valores 0 a 6 | Listo para imprimir y recortar")

# Línea separadora
c.setLineWidth(2)
c.line(40*mm, PAGE_HEIGHT - 45*mm, PAGE_WIDTH - 40*mm, PAGE_HEIGHT - 45*mm)

# Configuración de la cuadrícula (3 columnas x 3 filas)
cols = 3
rows = 3
margin_x = 25*mm
margin_y = 50*mm
spacing_x = 10*mm
spacing_y = 12*mm

marker_size = 45*mm
available_width = PAGE_WIDTH - (2 * margin_x) - ((cols - 1) * spacing_x)
col_width = available_width / cols

start_y = PAGE_HEIGHT - margin_y - 50*mm

# Dibujar cada marcador
markers = [0, 1, 2, 3, 4, 5, 6]

for idx, marker_num in enumerate(markers):
    if idx >= cols * rows:
        break

    row = idx // cols
    col = idx % cols

    x = margin_x + (col * (col_width + spacing_x))
    y = start_y - (row * (marker_size + spacing_y))

    # Marco del marcador
    is_active = (marker_num == 4)

    if is_active:
        c.setLineWidth(3)
        c.setFillColorRGB(0.95, 0.95, 0.95)
        c.rect(x - 3*mm, y - 3*mm, col_width + 6*mm, marker_size + 10*mm, fill=1, stroke=1)
    else:
        c.setLineWidth(1.5)

    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(0, 0, 0)
    c.rect(x, y, col_width, marker_size + 7*mm, fill=1, stroke=1)

    # Número del marcador
    c.setFillColorRGB(0, 0, 0)
    if is_active:
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(x + col_width/2, y + marker_size + 3*mm, f"★ MARCADOR #{marker_num} ★")
    else:
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(x + col_width/2, y + marker_size + 3*mm, f"MARCADOR #{marker_num}")

    # Imagen del marcador
    marker_path = os.path.join(MARKERS_DIR, f"{marker_num}.png")
    if os.path.exists(marker_path):
        img = ImageReader(marker_path)
        img_size = 38*mm
        img_x = x + (col_width - img_size) / 2
        img_y = y + 2*mm

        # Fondo blanco para la imagen
        c.setFillColorRGB(1, 1, 1)
        c.rect(img_x - 2*mm, img_y - 2*mm, img_size + 4*mm, img_size + 4*mm, fill=1, stroke=0)

        # Imagen
        c.drawImage(img, img_x, img_y, img_size, img_size, preserveAspectRatio=True)

    # Info del marcador
    c.setFont("Helvetica", 7)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    if is_active:
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(x + col_width/2, y - 1*mm, "ACTIVO EN LA APP")
    else:
        c.drawCentredString(x + col_width/2, y - 1*mm, f"3x3_HAMMING63 | Value: {marker_num}")

# Instrucciones en la parte inferior
instructions_y = 30*mm
c.setFont("Helvetica-Bold", 9)
c.drawString(25*mm, instructions_y, "INSTRUCCIONES:")

c.setFont("Helvetica", 7)
instructions = [
    "1. Recorta cada marcador siguiendo el borde negro. Mantén el borde blanco intacto.",
    "2. Pega sobre cartón rígido para mayor durabilidad (opcional).",
    "3. Abre index.html en Chrome móvil. El marcador #4 está activo por defecto.",
    "4. Mantén el marcador a 15-30 cm de la cámara con buena iluminación.",
]

for i, instruction in enumerate(instructions):
    c.drawString(25*mm, instructions_y - ((i+1) * 3*mm), instruction)

# Guardar PDF
c.save()
print(f"PDF generado: {PDF_OUTPUT}")
