# Function to delete __pycache__ folders
cleanup() {
    find . -type d -name "__pycache__" -exec rm -r {} +
}

# Trap the EXIT signal to run the cleanup function when the script exits
trap cleanup EXIT

# Activate the virtual environment if needed
source .venv/bin/activate

# Run the Python script to populate the database
python populate.py