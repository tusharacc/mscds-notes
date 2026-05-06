"""Stage 5: Upload output files to Google Drive for NotebookLM ingestion."""

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


_SCOPES = ["https://www.googleapis.com/auth/drive.file"]

_MIME_TYPES = {
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".json": "application/json",
}


def _authenticate(credentials_file: Path, token_file: Path) -> Credentials:
    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), _SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_file), _SCOPES)
            creds = flow.run_local_server(port=0)
        token_file.write_text(creds.to_json())

    return creds


def _get_or_create_folder(service, name: str, parent_id: str | None = None) -> str:
    """Return folder ID, creating it if it doesn't exist."""
    query = f"mimeType='application/vnd.google-apps.folder' and name='{name}' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]

    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        metadata["parents"] = [parent_id]

    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def upload_to_drive(
    files: list[Path],
    course_name: str,
    lecture_slug: str,
    credentials_file: Path,
    token_file: Path,
    root_folder_name: str = "NotebookLM Sources",
) -> str:
    """Upload files to Google Drive under NotebookLM Sources / <course> / <lecture>.

    Args:
        files: List of file paths to upload.
        course_name: e.g. "MachineLearning"
        lecture_slug: e.g. "backprop_2026-04-05"
        credentials_file: Path to OAuth client secrets JSON.
        token_file: Path to cached token JSON (created on first run).
        root_folder_name: Top-level Drive folder name.

    Returns:
        URL of the lecture subfolder on Google Drive.
    """
    creds = _authenticate(credentials_file, token_file)
    service = build("drive", "v3", credentials=creds)

    # Ensure folder hierarchy exists
    root_id = _get_or_create_folder(service, root_folder_name)
    course_id = _get_or_create_folder(service, course_name, parent_id=root_id)
    lecture_id = _get_or_create_folder(service, lecture_slug, parent_id=course_id)

    for file_path in files:
        mime = _MIME_TYPES.get(file_path.suffix, "application/octet-stream")
        metadata = {"name": file_path.name, "parents": [lecture_id]}
        media = MediaFileUpload(str(file_path), mimetype=mime, resumable=True)

        # Overwrite if a file with the same name already exists in this folder
        existing = service.files().list(
            q=f"name='{file_path.name}' and '{lecture_id}' in parents and trashed=false",
            fields="files(id)",
        ).execute().get("files", [])

        if existing:
            service.files().update(
                fileId=existing[0]["id"],
                media_body=media,
            ).execute()
            print(f"  Updated: {file_path.name}")
        else:
            service.files().create(
                body=metadata,
                media_body=media,
                fields="id",
            ).execute()
            print(f"  Uploaded: {file_path.name}")

    folder_url = f"https://drive.google.com/drive/folders/{lecture_id}"
    print(f"  Drive folder: {folder_url}")
    return folder_url
