import aiohttp

BASE_URL = 'https://api.thingiverse.com'


async def fetch_project(session, project_id):
    async with session.get(f'{BASE_URL}/things/{project_id}') as response:
        data = await response.json()
        print(data)
