from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import nodriver as driver
from main import fetch_response
import asyncio
from contextlib import asynccontextmanager

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

# Global variables to store browser and tab
browser = None
tab = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global browser, tab
    print("Starting the browser.")
    browser = await driver.start(headless=False)
    tab = await browser.get("https://chatgpt.com")
    yield
    # Shutdown
    if browser:
        print("Closing the browser.")
        await browser.close()

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/complete/")
async def complete(prompt_request: PromptRequest):
    global browser, tab
    try:
        if not browser or not tab:
            print("Browser or tab not initialized. Attempting to reinitialize.")
            browser = await driver.start(headless=False)
            tab = await browser.get("https://chatgpt.com")
        
        response = await fetch_response(prompt_request.prompt, browser, tab)
        return {"response": response}
    except Exception as e:
        import traceback
        print(f"Error in /complete/: {str(e)}")
        print(traceback.format_exc())
        # Attempt to reinitialize the browser session
        try:
            if browser:
                await browser.close()
            browser = await driver.start(headless=False)
            tab = await browser.get("https://chatgpt.com")
            print("Browser session reinitialized after error.")
        except Exception as reinit_error:
            print(f"Failed to reinitialize browser: {str(reinit_error)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)