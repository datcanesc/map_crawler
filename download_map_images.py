import os
import json
import requests
import time

def create_folder(folder_path):
    """Creates a folder if it does not already exist."""
    try:
        os.makedirs(folder_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating folder {folder_path}: {e}")

def download_image(url, folder_name, filename, failed_downloads, x, y, z):
    """Downloads an image from a URL and saves it in the specified folder."""
    try:
        response = requests.get(url, timeout=10)  # Set a timeout to avoid hanging requests
        response.raise_for_status()

        base_folder = "/data/images"  # Store all images inside the 'images' folder
        full_folder_path = os.path.join(base_folder, folder_name)
        create_folder(full_folder_path)

        file_path = os.path.join(full_folder_path, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)

    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading {url}: {e}")
        failed_downloads.append({"url": url, "x": x, "y": y, "z": z, "folder_name": folder_name, "filename": filename})

def download_images_from_json(file_path):
    """Reads a JSON file and downloads images based on its contents."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error reading JSON file {file_path}: {e}")
        return

    failed_downloads = []
    for entry in data:
        url = entry.get("url", "").strip()
        x, y, z = entry.get("x", 0), entry.get("y", 0), entry.get("z", 0)

        if url:
            folder_name = str(z)  # Group images by zoom level
            filename = f"{x}-{y}.png"  # Save images as x-y.png
            download_image(url, folder_name, filename, failed_downloads, x, y, z)
    print(f"✅ Images are saved")
    # Retry failed downloads
    if failed_downloads:
        print("🔄 Retrying failed downloads...")
        retry_failed_downloads(failed_downloads)

def retry_failed_downloads(failed_downloads, max_retries=3):
    """Retries downloading failed images."""
    for attempt in range(1, max_retries + 1):
        if not failed_downloads:
            return
        print(f"🔁 Retry attempt {attempt}/{max_retries}")
        remaining_failures = []
        
        for item in failed_downloads:
            url, folder_name, filename = item["url"], item["folder_name"], item["filename"]
            x, y, z = item["x"], item["y"], item["z"]
            download_image(url, folder_name, filename, remaining_failures, x, y, z)
        
        failed_downloads = remaining_failures
        if failed_downloads:
            print("⏳ Waiting before next retry...")
            time.sleep(5)  # Wait before retrying
    
    if failed_downloads:
        print("❌ Some downloads failed after multiple attempts. Saving failed URLs.")
        with open("/data/failed_downloads.json", "w") as f:
            json.dump(failed_downloads, f, indent=4)

if __name__ == "__main__":
    json_file = "/data/urls.json"  # JSON file containing image details
    download_images_from_json(json_file)
