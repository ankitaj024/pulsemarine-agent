import asyncio
import httpx
import time

async def main():
    async with httpx.AsyncClient(timeout=60.0) as client:
        start = time.time()
        print("Sending request for companies...")
        response = await client.post("http://127.0.0.1:8000/ai/ask", json={"query": "Give me all companies and charterers"})
        end = time.time()
        print(f"Status: {response.status_code}")
        print(f"Time taken: {end - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
