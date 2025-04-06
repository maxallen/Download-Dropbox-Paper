import os
import dropbox
from dropbox.files import FolderMetadata, FileMetadata
from dotenv import load_dotenv

# Get access token from .env file
load_dotenv()
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

if not DROPBOX_ACCESS_TOKEN:
    raise ValueError("DROPBOX_ACCESS_TOKEN not found in environment variables. Please check your .env file.")

def export_paper_docs(dbx, dropbox_path, local_root):
    """
    Recursively export files from the Dropbox folder `dropbox_path` to `local_root`
    """
    try:
        result = dbx.files_list_folder(dropbox_path, recursive=False)

        # print(f"Got result: {result}")
        # print("\n\n")
        print(f"Got {len(result.entries)} result entries")

        for entry in result.entries:
            rel_path = entry.path_display[len("/Migrated Paper Docs/"):]  # Get relative path from root
            local_path = os.path.join(local_root, rel_path.lstrip("/"))

            if isinstance(entry, FolderMetadata):
                print(f"Making directory: {local_path}")
                os.makedirs(local_path, exist_ok=True)
                export_paper_docs(dbx, entry.path_lower, local_root)

            elif isinstance(entry, FileMetadata):
                # Remove .paper suffix from the file path if it exists
                local_path = local_path.rstrip('.paper')

                print(f"Writing file: {local_path}")
                os.makedirs(os.path.dirname(local_path), exist_ok=True)


                try:
                    export_result, response = dbx.files_export(entry.path_lower, export_format="markdown")
                    with open(local_path, "wb") as f:
                        f.write(response.content)
                    # export_result = dbx.files_export(entry.path_lower)
                    # print(f"File export result: {export_result}")
                    # with open(local_path, "wb") as f:
                    #     f.write(export_result.file_binary)
                    print(f"Exported: {entry.path_display} → {local_path}")
                except dropbox.exceptions.ApiError as e:
                    print(f"Failed to export {entry.path_display}: {e}")

    except Exception as e:
        print(f"Error accessing {dropbox_path}: {e}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Export Dropbox 'Migrated Paper Docs' using files_export.")
    parser.add_argument("output_dir", help="Local directory to save exported files")
    args = parser.parse_args()

    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

    try:
        current_account = dbx.users_get_current_account()
        print(f"Authenticated as: {current_account.name.display_name}")
    except Exception as e:
        print("Failed to authenticate with Dropbox:", e)
        return

    # Start recursive export
    export_paper_docs(dbx, "/Migrated Paper Docs/", args.output_dir)


if __name__ == "__main__":
    main()
