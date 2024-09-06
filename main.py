import nodriver as driver
import asyncio

url = "https://chatgpt.com"

async def fetch_response(prompt: str, browser, tab) -> str:
    try:
        while True:
            try:
                # Check for limit reached
                limit_reached = await tab.find("Get smarter responses, upload files and images, and more.", timeout=2)
                if limit_reached:
                    print("Limit reached. Reloading the tab.")
                    await tab.reload()
                    continue
            except Exception:
                pass  # Limit not reached, continue with the prompt

            try:
                logged_out_link = await tab.find("text=Stay logged out", timeout=2)
                print("'Stay logged out' link found. Clicking it.")
                await logged_out_link.click()
            except Exception:
                print("'Stay logged out' link not found.")

            print("Locating the textarea for input.")
            textarea = await tab.select("#prompt-textarea")
            print("Inputting the prompt text.")
            await textarea.clear_input()
            await textarea.send_keys(prompt)

            print("Locating and clicking the submit button.")
            button = await tab.select("button.mb-1")
            await button.click()

            print("Waiting for the response.")
            max_retries = 10
            for attempt in range(max_retries):
                try:
                    await asyncio.sleep(5)
                    elements = await tab.query_selector_all('div.markdown.prose')
                    
                    if elements:
                        last_element = elements[-1]
                        response_text = last_element.text
                        print(f"Response found.")
                        print(f"Response received: {response_text}")
                        return response_text
                    
                    print(f"Response not found, attempt {attempt + 1}/{max_retries}")
                    await asyncio.sleep(2)
                except Exception as e:
                    print(f"Error in attempt {attempt + 1}: {e}")
                    await asyncio.sleep(2)

            print("Failed to capture response after multiple attempts.")
            return "Failed to capture response."

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

async def main():
    print("Starting the browser.")
    browser = await driver.start(headless=False)
    tab = await browser.get(url)

    while True:
        prompt = input("Enter your prompt (or 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break
        
        response = await fetch_response(prompt, browser, tab)
        print(f"Final response: {response}")

    print("Closing the browser.")
    await browser.close()

if __name__ == "__main__":
    driver.loop().run_until_complete(main())