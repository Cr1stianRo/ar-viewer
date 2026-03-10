# 🎯 AR Viewer - WebAR Application

Aplicación de Realidad Aumentada web usando **A-Frame** y **AR.js** con marcadores barcode.

## 🚀 Inicio Rápido

1. **Imprime el marcador:**
   - Abre `marcadores-ar-imprimir.pdf`
   - Imprime el marcador #4 (destacado)
   - Recorta por el borde negro

2. **Ejecuta la app:**
   - Abre `index.html` en Chrome móvil (HTTPS)
   - Da permiso a la cámara
   - Apunta al marcador #4 a 15-30cm

3. **¡Disfruta!**
   - El modelo 3D aparecerá sobre el marcador
   - Mueve la tarjeta y el modelo la sigue

---

## 📋 Configuración Actual

### Marcadores
- **Tipo:** `3x3_HAMMING63` (barcode con corrección de errores)
- **Marcador activo:** `#4`
- **Disponibles:** 0-6 (7 marcadores)
- **Ubicación:** `marcadores/*.png`

### Tecnologías
```
A-Frame: 1.4.2
AR.js: Master (raw.githack.com)
Marcador: 3x3_HAMMING63
Smoothing: Agresivo (15 frames)
```

---

## ⚙️ Cambiar Marcador Activo

**Archivo:** `index.html` línea 265

```html
<!-- Cambiar el número aquí (0-6) -->
<a-marker type="barcode" value="4" ...>
```

**Ejemplo para usar marcador #2:**
```html
<a-marker type="barcode" value="2" ...>
```

---

## 🎨 Modificar el Modelo 3D

**Ubicación:** `index.html` líneas 271-321

### Cambiar Colores
```html
<!-- Cubo verde -> rojo -->
<a-box color="#ff0000" ...>

<!-- Esfera blanca -> azul -->
<a-sphere color="#0000ff" ...>
```

### Cambiar Tamaño
```html
<!-- Cubo más grande -->
<a-box width="2" height="2" depth="2" ...>

<!-- Esfera más pequeña -->
<a-sphere radius="0.2" ...>
```

### Cargar Modelo 3D (.glb/.gltf)
```html
<!-- Reemplazar geometría por modelo externo -->
<a-marker type="barcode" value="4">
  <a-entity
    gltf-model="url(models/tu-modelo.glb)"
    scale="0.5 0.5 0.5"
    position="0 0 0"
  ></a-entity>
</a-marker>
```

---

## 🔧 Ajustar Estabilidad del Tracking

### Si el modelo tiembla mucho:

**Archivo:** `index.html` línea 265

```html
<!-- Aumentar suavizado -->
smoothCount="20"           <!-- 15 → 20 -->
smoothTolerance="0.005"    <!-- 0.01 → 0.005 -->
```

### Si hay lag/retraso:

```html
<!-- Reducir suavizado -->
smoothCount="10"           <!-- 15 → 10 -->
smoothTolerance="0.02"     <!-- 0.01 → 0.02 -->
```

---

## 📁 Archivos del Proyecto

```
ar-viewer/
├── index.html                      ⭐ App principal
├── marcadores-ar-imprimir.pdf      📄 Marcadores para imprimir
├── marcadores.html                 🖼️ Galería web de marcadores
├── comparacion-marcadores.html     🔍 Comparador de tipos
├── imprimir-marcadores.html        🖨️ Versión web para imprimir
├── marcadores/                     📁 Marcadores HAMMING63 (PNG)
│   └── 0.png - 6.png
├── marcadores-3x3-basico/          📁 Marcadores básicos (alternativa)
│   └── 0.png - 6.png
└── generar_pdf.py                  🐍 Script generador de PDF
```

---

## 🛠️ Solución de Problemas

### ❌ No detecta el marcador

**Causas:**
- Tipo de marcador incorrecto en el código
- Mala iluminación
- Marcador muy pequeño o borroso
- Cámara no tiene permiso

**Soluciones:**
1. Verificar que `matrixCodeType: 3x3_HAMMING63` (línea 250)
2. Mejorar iluminación del marcador
3. Imprimir en tamaño A4/Carta
4. Verificar permisos de cámara en navegador
5. Usar HTTPS (GitHub Pages, localhost con SSL)

### 🔄 El modelo desaparece al mover

**Causas:**
- Marcador pierde el borde negro del campo de visión
- Smoothing muy bajo

**Soluciones:**
1. Aumentar `smoothCount` a 20-25
2. Pegar marcador en cartón rígido
3. Mantener todo el marcador visible

### 📱 No funciona en móvil

**Causas:**
- No es HTTPS
- Navegador no soportado

**Soluciones:**
1. Subir a GitHub Pages (HTTPS automático)
2. Usar Chrome móvil (Safari puede fallar)
3. Verificar permisos de cámara en sistema operativo

---

## 🎯 Múltiples Marcadores

Para detectar varios marcadores simultáneamente:

```html
<!-- Marcador #4 con modelo 1 -->
<a-marker type="barcode" value="4">
  <a-box color="green" ...></a-box>
</a-marker>

<!-- Marcador #5 con modelo 2 -->
<a-marker type="barcode" value="5">
  <a-sphere color="red" ...></a-sphere>
</a-marker>

<!-- Marcador #6 con modelo 3 -->
<a-marker type="barcode" value="6">
  <a-torus color="blue" ...></a-torus>
</a-marker>
```

---

## 📚 Recursos

- [AR.js Documentation](https://ar-js-org.github.io/AR.js-Docs/)
- [A-Frame Documentation](https://aframe.io/docs/)
- [Marcadores oficiales](https://github.com/nicolocarpignoli/artoolkit-barcode-markers-collection)
- [Generador online](https://au.gmented.com/app/marker/marker.php)

---

## 📄 Licencia

Proyecto personal de demostración WebAR.

---

**Última actualización:** 2026-03-10
**Configuración:** 3x3_HAMMING63 | Marcador #4 | Smoothing agresivo