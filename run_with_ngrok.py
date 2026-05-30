"""
Script simplificado para iniciar Flask con ngrok
Versión mejorada que no requiere requests
"""
import subprocess
import time
import sys
import os
import webbrowser

def start_with_ngrok():
    """Inicia Flask con túnel ngrok"""
    
    # Ruta de ngrok
    ngrok_path = r"C:\Program Files\WindowsApps\ngrok.ngrok_3.24.0.0_x64__1g87z0zv29zzc\ngrok.exe"
    
    if not os.path.exists(ngrok_path):
        print("\n❌ No se encontró ngrok.exe")
        print(f"   Buscado en: {ngrok_path}")
        print("\n💡 Verifica la ruta de instalación")
        input("\nPresiona Enter para salir...")
        sys.exit(1)
    
    # Configurar puerto
    port = 5000
    
    print("="*70)
    print("🚀 Iniciando EquaHome con acceso remoto")
    print("="*70)
    print(f"\n📍 Servidor local: http://localhost:{port}")
    print(f"🏠 Red local: http://192.168.88.14:{port}")
    
    # Iniciar ngrok en segundo plano
    print(f"\n🌍 Iniciando túnel ngrok...")
    
    try:
        # Iniciar ngrok sin el authtoken en la línea de comando (ya está configurado)
        ngrok_process = subprocess.Popen(
            [ngrok_path, "http", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        
        # Esperar a que ngrok se conecte
        print("⏳ Esperando conexión (5 segundos)...")
        time.sleep(5)
        
        print("\n" + "="*70)
        print("✅ ngrok iniciado correctamente")
        print("="*70)
        print("\n📱 Dashboard de ngrok: http://localhost:4040")
        print("   Abre esta URL en tu navegador para ver tu enlace público\n")
        print("="*70)
        
        # Abrir dashboard automáticamente
        try:
            webbrowser.open('http://localhost:4040')
            print("🌐 Abriendo dashboard de ngrok en tu navegador...")
        except:
            pass
        
        print("\n▶️  Iniciando servidor Flask...\n")
        
        # Importar y ejecutar la app Flask
        from app import create_app
        app = create_app()
        
        # Ejecutar Flask
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo servidor...")
        ngrok_process.terminate()
        print("✅ Servidor detenido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if 'ngrok_process' in locals():
            ngrok_process.terminate()
        sys.exit(1)

if __name__ == '__main__':
    start_with_ngrok()
