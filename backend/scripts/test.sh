# Function to delete __pycache__ folders
cleanup() {
    find . -type d -name "__pycache__" -exec rm -r {} +
    find . -type d -name ".pytest_cache" -exec rm -r {} +
}

# Trap the EXIT signal to run the cleanup function when the script exits
trap cleanup EXIT

pytest --disable-warnings tests/