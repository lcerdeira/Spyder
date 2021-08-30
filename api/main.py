from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import schemas

app = FastAPI()

collections_path = f"{os.getcwd().replace('api', 'pathogen')}/files/collections/"

@app.get("/collections/{organism}", response_model=schemas.Collections)
async def collections(organism: schemas.Organisms):
    organism_path = os.path.join(collections_path, organism)
    
    if os.path.exists(organism_path):
        path = []

        for dir in os.listdir(organism_path):
            for filename in os.listdir(f"{organism_path}/{dir}"):
                path.append({
                    "path": dir,
                    "filename": filename
                    })
        
        return {"organism": organism, "path": path}
    
    raise HTTPException(status_code=404, detail="Organism is not loaded yet")

@app.get("/collections/{organism}/{path}/{filename}")
async def downloadFile(organism: schemas.Organisms, path: str, filename: str):
    file = os.path.join(collections_path, organism, path, filename)

    if os.path.exists(file):
        return FileResponse(path=file, headers={f"Content-Disposition": "attachment; filename="+filename})

    raise HTTPException(status_code=404, detail="File doesn't exist")
