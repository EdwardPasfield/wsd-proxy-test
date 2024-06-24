import argparse
import asyncio
import aiohttp
import aiofiles
import random

SEM_LIMIT = 30  # Limit of 30 concurrent requests per proxy

def parse_args():
    parser = argparse.ArgumentParser(description="Concurrent Request CLI Application")
    parser.add_argument('input', type=str, help="Path to the input file containing strings")
    parser.add_argument('addresses', type=str, help="Path to the file containing proxy addresses")
    parser.add_argument('output', type=str, help="Path to the output file to store results")
    return parser.parse_args()

async def read_file(file_path):
    async with aiofiles.open(file_path, mode='r') as file:
        lines = await file.readlines()
    return [line.strip() for line in lines]

async def fetch(session, url, input_string, semaphore):
    async with semaphore:
        async with session.get(url, params={"input": input_string}) as response:
            if response.status == 200:
                data = await response.json()
                return input_string, data['information']
            elif response.status == 503:
                return None
            else:
                raise Exception(f"Unexpected status code {response.status} for input {input_string}")

async def write_result(output_path, result):
    async with aiofiles.open(output_path, mode='a') as file:
        await file.write(f"{result[0]} {result[1]}\n")

async def fetch_and_retry(session, url, input_string, semaphore, output_path):
    while True:
        result = await fetch(session, url, input_string, semaphore)
        if result:
            await write_result(output_path, result)
            break

async def process_requests(input_strings, proxy_addresses, output_path):
    tasks = []
    semaphores = {address: asyncio.Semaphore(SEM_LIMIT) for address in proxy_addresses}

    async with aiohttp.ClientSession() as session:
        for input_string in input_strings:
            proxy = random.choice(proxy_addresses)
            url = f"{proxy}/api/data"
            task = asyncio.create_task(fetch_and_retry(session, url, input_string, semaphores[proxy], output_path))
            tasks.append(task)
        
        await asyncio.gather(*tasks)

async def main():
    args = parse_args()
    input_strings = await read_file(args.input)
    proxy_addresses = await read_file(args.addresses)
    await process_requests(input_strings, proxy_addresses, args.output)

if __name__ == "__main__":
    asyncio.run(main())