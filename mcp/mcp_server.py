from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Mock MCP Server")

@app.post("/activate_card")
async def activate_card(request: Request):
    body = await request.json()
    card_number = body.get("card_number", "XXXX-XXXX-XXXX-0000")
    return JSONResponse({
        "status": "success",
        "message": f"Card {card_number} activated successfully."
    })

@app.post("/update_address")
async def update_address(request: Request):
    body = await request.json()
    account_id = body.get("account_id", "ACC12345")
    new_address = body.get("new_address", "N/A")
    return JSONResponse({
        "status": "success",
        "message": f"Address for account {account_id} updated to '{new_address}'."
    })

@app.post("/close_account")
async def close_account(request: Request):
    body = await request.json()
    account_id = body.get("account_id", "ACC12345")
    return JSONResponse({
        "status": "success",
        "message": f"Account {account_id} has been closed successfully."
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
