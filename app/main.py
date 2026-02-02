from fastapi import FastAPI

app = FastAPI(title="Loan Management System")


@app.get("/")
def read_root():
    return {"message": "Loan Management System API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
