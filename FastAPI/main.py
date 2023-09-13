from fastapi import FastAPI

app = FastAPI()
user = {1:{"name":"ATUL","language":"python"}}
@app.get("/{id}")
def root(id: int):
    data = user[id]
    print(data)
    return data

@app.post("/{id}")
def root(id: int, data: dict):
    user[id]=data
    print(user)
    return data


@app.put("/{id}")
def root(id: int, data: dict):
    user[id]=data
    print(user)
    return data
