import aiohttp
import asyncio
import aiofiles
import os
import html2text
from xml.sax.saxutils import unescape
from helpers.image_finder import get_image_url
from services.authenticate import get_project_folder_id, create_a_file, create_a_folder
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFileList
from apiclient.http import MediaFileUpload

BASE_URL = 'https://api.thingiverse.com'


async def fetch_project(session, project_id):
    async with session.get(f'{BASE_URL}/things/{project_id}') as response:
        data = await response.json()
        return data


async def fetch_images(session, project_data, drive_service, project_folder_id):
    image_folder_id = create_a_folder(
        drive_service, 'images', project_folder_id)["id"]
    async with session.get(project_data['images_url']) as response:
        images = await response.json()
        image_requests = []

        try:
            os.makedirs(f'./temp/{project_data["id"]}/images', )
        except:
            print('Could not create images folder.')

        for image in images:
            image_requests.append(download_image(
                session, image, project_data['id'], image_folder_id, drive_service))

        await asyncio.gather(*image_requests)


async def download_image(session, image, project_id, image_folder_id, drive_service):
    image_url = get_image_url(image)
    async with session.get(image_url) as imageResponse:
        file = await aiofiles.open(f'temp/{project_id}/images/{image["name"]}', mode='wb')

        await file.write(await imageResponse.read())
        await file.close()

        file_metadata = {'name': image["name"], 'parents': [image_folder_id]}
        media = MediaFileUpload(
            f'temp/{project_id}/images/{image["name"]}', mimetype=None)
        create_a_file(drive_service, file_metadata, media)


async def fetch_files(session, project_data, drive_service, project_folder_id):
    files_folder_id = create_a_folder(
        drive_service, 'files', project_folder_id)["id"]
    async with session.get(project_data['files_url']) as response:
        files = await response.json()
        file_requests = []

        try:
            os.makedirs(f'./temp/{project_data["id"]}/files')
        except:
            print('Could not create files folder.')

        for file in files:
            file_requests.append(download_file(
                session, file, project_data['id'], drive_service, files_folder_id))

        await asyncio.gather(*file_requests)


async def download_file(session, file2, project_id, drive_service, files_folder_id):
    async with session.get(file2['download_url']) as fileResponse:
        file = await aiofiles.open(f'temp/{project_id}/files/{file2["name"]}', mode='wb')

        await file.write(await fileResponse.read())
        await file.close()

        file_metadata = {'name': file2["name"], 'parents': [files_folder_id]}
        media = MediaFileUpload(
            f'temp/{project_id}/files/{file2["name"]}', mimetype=None)
        create_a_file(drive_service, file_metadata, media)


async def write_texts_to_files(project, drive_service, project_folder_id):
    description = await aiofiles.open(f'temp/{project["id"]}/description.md', mode="w")
    await description.write(html2text.html2text(unescape(project['details'])))
    await description.close()

    file_metadata = {'name': 'description.md', 'parents': [project_folder_id]}
    media = MediaFileUpload(
        f'temp/{project["id"]}/description.md', mimetype=None)
    create_a_file(drive_service, file_metadata, media)

    instructions = await aiofiles.open(f'temp/{project["id"]}/LICENSE.txt', mode="w")
    await instructions.write((project['license']))
    await instructions.close()

    file_metadata = {'name': 'LICENSE.txt', 'parents': [project_folder_id]}
    media = MediaFileUpload(f'temp/{project["id"]}/LICENSE.txt', mimetype=None)
    create_a_file(drive_service, file_metadata, media)
