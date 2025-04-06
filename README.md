# Download DropboxxPaper

## Instructions
1. Clone this repository
2. Head over to [Dropbox's API explorer](https://dropbox.github.io/dropbox-api-v2-explorer/#files_export) and generate an API token by clicking "Get Token". Create a `.env` file in this repository, which should look like this:
```
DROPBOX_ACCESS_TOKEN=<YOUR_DROPBOX_TOKEN_HERE>
```
3. Ensure your Dropbox Paper files are in your [Dropbox home](https://www.dropbox.com/home) under a top-level folder called `Migrated Paper Docs`. If they aren't you'll need to update the script to point it at the correct directory.
4. Setup and run the script like so:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python download_paper.py ./output
```

The script will download all Dropbox Paper files from your `Migrated Paper Docs` folder and save them as markdown files in the specified output directory.