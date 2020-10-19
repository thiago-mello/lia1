from services.parse_project import parse_project
from services.requests import fetch_project
import aiohttp
import asyncio
import sys
sys.path.append('.')

API_TOKEN = '56edfc79ecf25922b98202dd79a291aa'


async def main():
    try:
        project_string = sys.argv[1]
        project_id = parse_project(project_string)
        async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {API_TOKEN}'}) as session:
            project = await fetch_project(session, project_id)
            print(project)
    except IndexError:
        print('ERROR: The Thingiverse project is missing.')


if __name__ == '__main__':
    asyncio.run(main())
