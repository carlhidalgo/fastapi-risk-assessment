import uvicorn
import sys
import os

# Agregar el directorio backend al path
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    try:
        os.chdir(backend_dir)
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8001,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
