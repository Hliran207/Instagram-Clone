from fastapi import FastAPI


app = FastAPI(title="Instagram API", description="API for the Instagram project")


@app.get("/health")
def health_check():
    return {"status": "ok"}
