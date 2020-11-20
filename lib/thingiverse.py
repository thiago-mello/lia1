import aiohttp
import asyncio
import aiofiles
import os
import html2text
from helpers.image_finder import get_image_url

BASE_URL = 'https://api.thingiverse.com'


async def fetch_project(session, project_id):
    async with session.get(f'{BASE_URL}/things/{project_id}') as response:
        data = await response.json()
        return data


async def fetch_images(session, project_data):
    async with session.get(project_data['images_url']) as response:
        images = await response.json()
        image_requests = []

        try:
            os.makedirs(f'./temp/{project_data["id"]}/images', )
        except:
            print('Could not create images folder.')

        for image in images:
            image_requests.append(download_image(
                session, image, project_data['id']))

        await asyncio.gather(*image_requests)


async def download_image(session, image, project_id):
    image_url = get_image_url(image)
    async with session.get(image_url) as imageResponse:
        file = await aiofiles.open(f'temp/{project_id}/images/{image["name"]}', mode='wb')

        await file.write(await imageResponse.read())
        await file.close()


async def fetch_files(session, project_data):
    async with session.get(project_data['files_url']) as response:
        files = await response.json()
        file_requests = []

        try:
            os.makedirs(f'./temp/{project_data["id"]}/files')
        except:
            print('Could not create files folder.')

        for file in files:
            file_requests.append(download_file(
                session, file, project_data['id']))

        await asyncio.gather(*file_requests)


async def download_file(session, file, project_id):
    async with session.get(file['download_url']) as fileResponse:
        file = await aiofiles.open(f'temp/{project_id}/files/{file["name"]}', mode='wb')

        await file.write(await fileResponse.read())
        await file.close()


async def write_texts_to_files(project):
    description = await aiofiles.open(f'temp/{project["id"]}/description.md', mode="w")
    await description.write(html2text.html2text(project['details']))
    await description.close()

    instructions = await aiofiles.open(f'temp/{project["id"]}/LICENSE.txt', mode="w")
    await instructions.write((project['license']))
    await instructions.close()
