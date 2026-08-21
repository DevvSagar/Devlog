from fastapi import FastAPI

app = FastAPI(title="Devlog-Blog")


@app.get("/")
def root():
    return {"Message" : "Your API is Running !!!"}


