#!/bin/bash

# ANCAP Screensaver v1.1 - Instalador Automático
# Screensaver Libertario con 192 frases optimizadas
# Máximo 18 palabras por frase para visualización perfecta

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ANCAP SCREENSAVER v1.1                   ║"
echo "║                  Instalador Libertario                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🟡 Características:"
echo "   • 192 frases libertarias optimizadas (máx. 18 palabras)"
echo "   • Efectos glitch ultra-violentos (0.2s)"
echo "   • Tipografía Space Grotesk profesional"
echo "   • Soporte bilingüe (Español/Inglés)"
echo "   • Controles manuales (Espacio/Flechas)"
echo "   • Autores: Mises, Hayek, Rothbard, Rand, Friedman, etc."
echo ""

# Verificar si es macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: Este screensaver solo funciona en macOS"
    exit 1
fi

# Verificar si el archivo existe
if [ ! -d "ANCAP.saver" ]; then
    echo "❌ Error: No se encuentra ANCAP.saver en el directorio actual"
    echo "   Asegúrate de ejecutar este script desde el directorio del screensaver"
    exit 1
fi

echo "🔧 Iniciando instalación..."

# Crear directorio de screensavers si no existe
SCREENSAVER_DIR="$HOME/Library/Screen Savers"
if [ ! -d "$SCREENSAVER_DIR" ]; then
    echo "   Creando directorio de screensavers..."
    mkdir -p "$SCREENSAVER_DIR"
fi

# Copiar screensaver
echo "   Copiando ANCAP.saver..."
cp -R "ANCAP.saver" "$SCREENSAVER_DIR/"

# Verificar instalación
if [ -d "$SCREENSAVER_DIR/ANCAP.saver" ]; then
    echo ""
    echo "✅ ¡Instalación completada exitosamente!"
    echo ""
    echo "📋 Instrucciones de activación:"
    echo "   1. Ve a Preferencias del Sistema > Escritorio y Salvapantallas"
    echo "   2. Selecciona la pestaña 'Salvapantallas'"
    echo "   3. Busca 'ANCAP' en la lista y selecciónalo"
    echo "   4. Configura el tiempo de espera según prefieras"
    echo ""
    echo "⌨️  Controles durante el screensaver:"
    echo "   • ESPACIO: Cambiar frase manualmente"
    echo "   • ← →: Navegar entre frases"
    echo "   • ESC: Salir del screensaver"
    echo ""
    echo "🎯 Frases incluidas:"
    echo "   • Ludwig von Mises (10 citas)"
    echo "   • Friedrich Hayek (10 citas)"
    echo "   • Murray Rothbard (10 citas)"
    echo "   • Ayn Rand (10 citas)"
    echo "   • Milton Friedman (10 citas)"
    echo "   • Adam Smith (10 citas)"
    echo "   • Hans-Hermann Hoppe (10 citas)"
    echo "   • Robert Nozick (5 citas)"
    echo "   • Ron Paul (10 citas)"
    echo "   • Frederic Bastiat (10 citas)"
    echo "   • Javier Milei (10 citas)"
    echo "   • Frases adicionales libertarias"
    echo ""
    echo "💛 ¡Disfruta tu screensaver libertario!"
    echo ""
    
    # Preguntar si quiere abrir las preferencias
    read -p "¿Quieres abrir las Preferencias del Sistema ahora? (s/N): " response
    if [[ "$response" =~ ^[Ss]$ ]]; then
        open "/System/Library/PreferencePanes/DesktopScreenEffectsPref.prefPane"
    fi
    
else
    echo "❌ Error durante la instalación"
    echo "   Verifica que tienes permisos de escritura en ~/Library/Screen Savers"
    exit 1
fi
