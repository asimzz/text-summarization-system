# Function to delete __pycache__ folders
cleanup() {
    find . -type d -name "__pycache__" -exec rm -r {} +
}

# Trap the EXIT signal to run the cleanup function when the script exits
trap cleanup EXIT

uvicorn app:app --reload --host 127.0.0.1 --port 8000

