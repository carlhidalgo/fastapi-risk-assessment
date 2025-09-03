#!/usr/bin/env python3
import os
import sys
import json

# Change to the backend directory  
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import main
from app.schemas.schemas import UserCreate
from app.core.database import get_db

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            if self.path == '/api/v1/auth/register':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                print(f"Received data: {data}")
                
                # Create user data
                user_data = UserCreate(**data)
                
                # Get database session
                db_gen = get_db()
                db = next(db_gen)
                
                try:
                    result = main.register(user_data, db)
                    response_data = {
                        "id": result.id,
                        "email": result.email,
                        "name": result.name,
                        "created_at": result.created_at.isoformat()
                    }
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(response_data).encode())
                    
                except Exception as e:
                    print(f"Error: {e}")
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"detail": str(e)}).encode())
                finally:
                    db.close()
            else:
                self.send_response(404)
                self.end_headers()
                
        except Exception as e:
            print(f"Handler error: {e}")
            import traceback
            traceback.print_exc()
            self.send_response(500)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8003), SimpleAPIHandler)
    print("Simple API server running on http://localhost:8003")
    print("Test with: POST http://localhost:8003/api/v1/auth/register")
    server.serve_forever()
