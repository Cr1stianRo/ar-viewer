# 🎲 Cubo Aumentado AR - Documentación Técnica

## 📋 Resumen
Sistema de realidad aumentada que superpone planos de colores digitales sobre un cubo físico usando MindAR image tracking. Cada cara del cubo físico se "pinta" con un color cuando la cámara la detecta.

---

## 🎨 Configuración de Caras

### Mapeo de Targets a Colores

| Target | Cara | Color | Hex | Descripción |
|--------|------|-------|-----|-------------|
| **0** | FRONTAL | 🔴 Rojo | `#ff3333` | Cara principal del cubo |
| **1** | TRASERA | 🔵 Azul | `#3333ff` | Cara opuesta a la frontal |
| **2** | DERECHA | 🟢 Verde | `#33ff33` | Cara lateral derecha |
| **3** | IZQUIERDA | 🟡 Amarillo | `#ffff33` | Cara lateral izquierda |
| **4** | SUPERIOR | 🟣 Magenta | `#ff33ff` | Cara de arriba |
| **5** | INFERIOR | 🔵 Cyan | `#33ffff` | Cara de abajo |

---

## 🔧 Parámetros Técnicos

### MindAR Image Tracking
```javascript
imageTargetSrc: marker/cubo.mind
autoStart: false
filterMinCF: 0.0001      // Filtro de confianza mínima
filterBeta: 1000         // Factor de suavizado (alto = más estable)
warmupTolerance: 2       // Frames de calentamiento
missTolerance: 100       // Frames antes de perder tracking (persistencia)
maxTrack: 6              // Máximo 6 caras simultáneas
```

### Planos AR (por cara)
```html
<a-plane
  width="1"              // Ancho = 1 unidad (tamaño del target)
  height="1"             // Alto = 1 unidad
  position="0 0 0.001"   // Ligeramente delante del target
  rotation="0 0 0"       // Sin rotación (alineado con target)
  material="
    color: #RRGGBB;      // Color único por cara
    opacity: 0.85;       // Semi-transparente (85%)
    side: double;        // Visible desde ambos lados
    transparent: true;   // Habilita transparencia
    shader: flat;        // Sin afectación por luz
  "
/>
```

### Bordes Blancos (marco)
```html
<a-plane
  width="1.02"           // 2% más grande
  height="1.02"
  position="0 0 0"       // Exactamente en el target
  material="
    color: #ffffff;
    opacity: 0.3;        // Muy transparente
    side: double;
    transparent: true;
    shader: flat;
  "
/>
```

---

## 📱 Configuración de Cámara

### Resolución y FPS
- **Resolución ideal**: 1920x1080 (Full HD)
- **Resolución mínima**: 1280x720 (HD)
- **FPS ideal**: 60 fps
- **FPS mínimo**: 30 fps

### Autofocus Continuo
```javascript
advanced: [
  { focusMode: 'continuous' },        // Autofocus permanente
  { exposureMode: 'continuous' },     // Exposición automática
  { whiteBalanceMode: 'continuous' }  // Balance de blancos auto
]
```

### Selección de Cámara
1. **Prioridad 1**: Cámara trasera principal (sin "wide", "ultra", "0.5")
2. **Prioridad 2**: Cualquier cámara con `facingMode: environment`

---

## 🎯 Sistema de Tracking

### Estados del Sistema
```javascript
state = {
  detectedFaces: Set(),     // Caras ya detectadas (0-5)
  currentFace: null,        // Cara actualmente visible (0-5 o null)
  trackingActive: false,    // Si hay tracking activo
  debugMode: false          // Modo debug (cambiar a true para logs)
}
```

### Eventos de Target
- **`targetFound`**: Se dispara cuando una cara es detectada
  - Actualiza UI (status dot, texto, contador)
  - Agrega cara al Set de detectadas
  - Muestra mensaje de progreso

- **`targetLost`**: Se dispara cuando se pierde la cara
  - Resetea estado de tracking
  - Muestra mensaje de "buscando cubo"
  - Mantiene registro de caras ya vistas

---

## 📊 UI/UX

### Elementos de Interfaz

1. **Topbar**
   - Logo: "🎲 CUBO AR"
   - Status dot: Rojo (buscando) / Verde (tracking)
   - Status text: Nombre de cara actual o "BUSCANDO CUBO..."

2. **Contador de Caras** (esquina superior derecha)
   - Muestra: "X/6" caras descubiertas
   - Se actualiza en tiempo real

3. **Instruction Card** (centro inferior)
   - Icono dinámico: 🎯 (inicial) / ✅ (detectado) / 🏆 (completo) / 🔍 (perdido)
   - Texto adaptativo según estado
   - Se oculta automáticamente después de 2.5 segundos (si no está completo)

4. **Botón Volver** (esquina superior izquierda)
   - Regresa al menú principal (index.html)

5. **Debug Panel** (opcional, inferior izquierda)
   - Activar con `state.debugMode = true`
   - Muestra: Target actual, Caras detectadas, FPS

---

## 🚀 Flujo de Ejecución

### 1. Inicio de Sistema
```
Usuario presiona "INICIAR EXPERIENCIA"
  ↓
startAR() se ejecuta
  ↓
Oculta pantalla de permisos
  ↓
Muestra escena AR + UI overlay
  ↓
Espera carga de A-Frame
  ↓
initMindAR() se ejecuta
```

### 2. Inicialización de MindAR
```
Inicia sistema MindAR
  ↓
Fuerza resize del renderer (fix canvas invisible)
  ↓
setupFaceTracking() configura eventos
  ↓
Sistema listo y buscando cubo
```

### 3. Detección de Cara
```
Cámara detecta cara del cubo (ej: Cara 0 - Roja)
  ↓
Evento 'targetFound' se dispara
  ↓
Plano rojo se hace visible sobre la cara física
  ↓
UI se actualiza: "CARA FRONTAL (Roja)" + "1/6"
  ↓
Usuario rota el cubo
  ↓
Se pierde Cara 0 → 'targetLost'
  ↓
Se detecta Cara 1 → 'targetFound' → Plano azul visible
  ↓
Continúa hasta descubrir las 6 caras
  ↓
Mensaje de victoria: "🏆 ¡CUBO COMPLETO!"
```

---

## 🎮 Experiencia del Usuario

### ¿Qué verá el usuario?

1. **Antes de apuntar al cubo**:
   - Pantalla con feed de cámara
   - UI mostrando "BUSCANDO CUBO..."
   - Instrucciones: "Apunta a cualquier cara del cubo"

2. **Al detectar primera cara (ej: Roja)**:
   - Plano rojo semi-transparente se superpone a la cara física
   - Borde blanco alrededor del plano para mejor definición
   - Status cambia a "CARA FRONTAL (Roja)"
   - Contador: "1/6"
   - Mensaje: "¡Cara Roja detectada! Faltan 5 caras por descubrir"

3. **Al rotar el cubo**:
   - Cara anterior desaparece (plano se oculta)
   - Nueva cara aparece con su color correspondiente
   - Contador se incrementa (2/6, 3/6, etc.)
   - Cada cara mantiene su color único

4. **Al completar las 6 caras**:
   - Mensaje especial: "🏆 ¡CUBO COMPLETO!"
   - Todas las caras ya fueron descubiertas
   - Usuario puede seguir explorando libremente

---

## 🔍 Verificación de Calidad

### ✅ Checklist de Funcionalidad

- [x] 6 targets definidos (targetIndex: 0-5)
- [x] 6 colores únicos y contrastantes
- [x] Planos perfectamente alineados con targets (position: 0 0 0.001)
- [x] Materiales con transparencia (opacity: 0.85)
- [x] Shader flat para no afectar por iluminación
- [x] Bordes blancos para mejor visualización
- [x] Side: double para visibilidad desde cualquier ángulo
- [x] Eventos targetFound y targetLost configurados
- [x] Contador de caras funcional (X/6)
- [x] UI adaptativa según estado
- [x] Interceptor de cámara para selección inteligente
- [x] Autofocus continuo habilitado
- [x] Parámetros MindAR optimizados (filterBeta: 1000, missTolerance: 100)
- [x] Manejo de errores completo
- [x] Renderer resize forzado (fix canvas invisible)
- [x] Debug mode disponible
- [x] Responsive design para móviles

---

## 🐛 Solución de Problemas

### Problema: "No detecta ninguna cara"
**Posibles causas**:
- Archivo `cubo.mind` corrupto o no existe
- Iluminación insuficiente
- Cubo físico muy pequeño o muy lejos
- Cámara no tiene autofocus

**Soluciones**:
1. Verificar que `marker/cubo.mind` existe (3.0 MB)
2. Mejorar iluminación del entorno
3. Mantener cubo a 20-40cm de la cámara
4. Activar debug mode: `state.debugMode = true`
5. Revisar consola del navegador (F12)

### Problema: "Planos no se superponen bien al cubo"
**Posibles causas**:
- Tamaño del plano no coincide con target
- Posición Z incorrecta
- Cubo físico deformado

**Soluciones**:
1. Ajustar `width` y `height` del plano (actualmente 1x1)
2. Ajustar `position="0 0 Z"` (probar 0.001, 0.01, 0.1)
3. Verificar que el cubo físico sea perfectamente cuadrado

### Problema: "Tracking muy inestable (tiembla mucho)"
**Posibles causas**:
- Parámetros MindAR muy agresivos
- Iluminación variable
- Cubo con bordes borrosos

**Soluciones**:
1. Aumentar `filterBeta` (más suavizado): 2000, 3000
2. Aumentar `warmupTolerance`: 5, 10
3. Mejorar contraste de las imágenes del cubo
4. Estabilizar iluminación del entorno

### Problema: "Colores se ven muy opacos o muy transparentes"
**Solución**:
- Ajustar `opacity` en material (actualmente 0.85)
- Rango recomendado: 0.5 (muy transparente) - 1.0 (opaco)

---

## 📝 Notas Técnicas

### Diferencias con otros modos AR del proyecto

| Característica | Cubo AR | MindAR Simple | Marker Barcode |
|----------------|---------|---------------|----------------|
| Tecnología | MindAR Image | MindAR Image | AR.js Barcode |
| Targets | 6 simultáneos | 1 único | 1 único |
| Contenido | Planos de color | Cubo 3D | Gallina 3D |
| Propósito | Superposición perfecta | Demo IA | Demo clásica |
| Complejidad | Media | Baja | Baja |

### Archivo cubo.mind
- **Tamaño**: ~3.0 MB
- **Formato**: Binario compilado por MindAR
- **Contenido**: 6 descriptores de imagen (features)
- **Generación**: MindAR compiler tool
- **Ubicación**: `marker/cubo.mind`

### Performance
- **FPS esperado**: 30-60 fps (según dispositivo)
- **Latencia**: <100ms (detección → renderizado)
- **Tracking persistence**: 100 frames sin detección antes de perder target
- **Smooth tracking**: filterBeta=1000 aplica suavizado agresivo

---

## 🎓 Conceptos Clave

### Image Tracking vs Barcode Tracking
- **Barcode**: Detecta patrones binarios (blanco/negro), rápido pero limitado
- **Image Tracking**: Detecta features naturales, más flexible y robusto

### ¿Por qué semi-transparencia?
- Permite ver el cubo físico debajo
- Crea efecto de "pintura digital"
- Facilita alineación visual

### ¿Por qué shader: flat?
- Desactiva iluminación 3D
- Colores se ven constantes independiente de luz ambiente
- Mejor visibilidad en cualquier condición

### ¿Por qué side: double?
- El plano se ve desde ambos lados
- Útil si el target se voltea accidentalmente
- Más robusto ante rotaciones inesperadas

---

## 📚 Recursos

- **A-Frame**: https://aframe.io/docs/
- **MindAR**: https://hiukim.github.io/mind-ar-js-doc/
- **AR.js**: https://ar-js-org.github.io/AR.js-Docs/

---

**Última actualización**: 2026-03-11
**Versión**: 1.0
**Archivo**: index-cube.html
**Líneas de código**: 772
