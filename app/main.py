from fastapi import FastAPI

app = FastAPI(
    title="AI Research Agent",
    description="An AI-powered document intelligence and research system",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Research Agent is running!"
    }