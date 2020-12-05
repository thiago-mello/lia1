from services.parse_project import parse_project
from lib.thingiverse import fetch_project, fetch_images, fetch_files, write_texts_to_files
import aiohttp
import aiofiles
import asyncio
import os
import sys
sys.path.append('.')

API_TOKEN = '2cf5af8ad1db62516b66b0262b590432'


async def fetch_project_data(project_id):
    async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {API_TOKEN}'}) as session:
        project = await fetch_project(session, project_id)

        try:
            os.makedirs(f'./temp/{project["id"]}')
        except:
            print('Could not create project folder.')

        await asyncio.gather(fetch_images(session, project), fetch_files(session, project), write_texts_to_files(project))


async def main():
    try:
        project_strings = sys.argv[1:]
        project_tasks = []

        for project_string in project_strings:

            project_id = parse_project(project_string)
            project_tasks.append(fetch_project_data(project_id))

        await asyncio.gather(*project_tasks)

    except IndexError:
        print('ERROR: The Thingiverse project is missing.')


if __name__ == '__main__':
    asyncio.run(main())
