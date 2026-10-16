import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# 1. Define your API routes FIRST
@app.get("/api/status")
def get_status():
    return {"status": "Backend is running!"}

# 2. Path to your React Vite build directory
UI_DIR = os.path.join(os.path.dirname(__file__), "dist")

# 3. Mount the assets folder explicitly
# Vite puts bundled JS/CSS in the /assets directory by default
assets_path = os.path.join(UI_DIR, "assets")
if os.path.isdir(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

# 4. Catch-all route to serve the SPA
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """
    Serves static files if they exist (e.g., favicon.ico, robots.txt).
    Otherwise, falls back to index.html for React Router handling.
    """
    file_path = os.path.join(UI_DIR, full_path)
    
    # Serve the requested file if it actually exists
    if full_path and os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Fallback to index.html for SPA routing
    index_path = os.path.join(UI_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
        
    return {"error": "UI build not found. Did you run 'npm run build'?"}

if __name__ == "__main__":
    # Run the server using uvicorn programmatically
    port = int(os.environ.get("DATABRICKS_APP_PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)