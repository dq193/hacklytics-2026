from fastapi import FastAPI

app = FastAPI(title="Hacklytics 2026 API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Welcome to Hacklytics 2026 API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import hypercorn
    import asyncio
    from hypercorn.config import Config
    from hypercorn.asyncio import serve
    
    config = Config()
    config.bind = ["0.0.0.0:3000"]
    asyncio.run(serve(app, config))
