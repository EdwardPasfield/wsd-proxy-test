import argparse
import asyncio
import time
import aiohttp
import aiofiles
import random
from typing import List, Tuple, Optional

SEM_LIMIT = 30  # Limit of 30 concurrent requests per proxy

def parse_args() -> argparse.Namespace:
    """Description: Uses argparse to handle 3 CLI inputs being (input.txt, addresses.txt and output.txt)"""
    parser = argparse.ArgumentParser(description="Concurrent Request CLI Application")
    parser.add_argument('input', type=str, help="Path to the input file containing strings")
    parser.add_argument('addresses', type=str, help="Path to the file containing proxy addresses")
    parser.add_argument('output', type=str, help="Path to the output file to store results")
    return parser.parse_args()

async def read_file(file_path: str) -> List[str]:
    """Description: uses aiofiles to aysnchronously read content and return list of lines"""
    async with aiofiles.open(file_path, mode='r') as file:
        lines = await file.readlines()
    return [line.strip() for line in lines]


async def fetch(session: aiohttp.ClientSession, url: str, input_string: str, semaphore: asyncio.Semaphore):
    """Description: Performs async HTTP Get request, ensures no more than 30 concurrent requests to proxy using semaphore
        Handles 200: success; 503: retries until response returns; all other status codes returns exception."""
    async with semaphore:
        async with session.get(url, params={"input": input_string}) as response:
            if response.status == 200:
                data = await response.json()
                return input_string, data['information']
            elif response.status == 503:
                return None
            else:
                raise Exception(f"Unexpected status code {response.status} for input {input_string}")

async def write_result(output_path: str, result: Tuple[str, str]) -> None:
    """Description: uses aiofiles to aysnchronously write content to output.txt"""
    async with aiofiles.open(output_path, mode='a') as file:
        await file.write(f"{result[0]} {result[1]}\n")

async def fetch_and_retry(session: aiohttp.ClientSession, url: str, input_string: str, semaphore: asyncio.Semaphore, output_path: str) -> None:
    """Description: continously attempts to fetch the data until a 200 response is recieved. uses await for this."""
    while True:
        result = await fetch(session, url, input_string, semaphore)
        if result:
            await write_result(output_path, result)
            break

async def process_requests(input_strings: List[str], proxy_addresses: List[str], output_path: str) -> None:
    tasks = []
    semaphores = {address: asyncio.Semaphore(SEM_LIMIT) for address in proxy_addresses}
    """Description: Manages overall process. Creates list of async tasks. gathers and runs all tasks concurrently"""
    async with aiohttp.ClientSession() as session:
        for input_string in input_strings:
            proxy = random.choice(proxy_addresses)
            url = f"{proxy}/api/data"
            task = asyncio.create_task(fetch_and_retry(session, url, input_string, semaphores[proxy], output_path))
            tasks.append(task)
            # Uccomment and run to see it appending to file after each concurrent task.
            #time.sleep(15)

            await asyncio.gather(*tasks)
    print("Request responses all concurrently uploaded!")


async def main() -> None:
    """Description: Parses CLI args. Reads input strings and proxies from files. Initiates request processing."""
    args = parse_args()
    input_strings = await read_file(args.input)
    proxy_addresses = await read_file(args.addresses)
    await process_requests(input_strings, proxy_addresses, args.output)

if __name__ == "__main__":
    asyncio.run(main())