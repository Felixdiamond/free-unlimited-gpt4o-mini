from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import nodriver as driver
from main import fetch_response

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

# Global variables to store browser and tab
browser = None
tab = None

@app.on_event("startup")
async def startup_event():
    global browser, tab
    print("Starting the browser.")
    browser = await driver.start(headless=False)
    tab = await browser.get("https://chatgpt.com")

@app.on_event("shutdown")
async def shutdown_event():
    global browser
    if browser:
        print("Closing the browser.")
        await browser.close()

@app.post("/complete/")
async def complete(prompt_request: PromptRequest):
    global browser, tab
    try:
        if not browser or not tab:
            raise HTTPException(status_code=500, detail="Browser not initialized")
        
        response = await fetch_response(prompt_request.prompt, browser, tab)
        return {"response": response}
    except Exception as e:
        import traceback
        print(f"Error in /complete/: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)