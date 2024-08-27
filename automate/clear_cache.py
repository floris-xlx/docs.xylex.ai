import os
import shutil


async def clear_cache():
    await clear_pages_cache()

    cache_dir = 'cache'
    if os.path.exists(cache_dir) and os.path.isdir(cache_dir):
        try:
            shutil.rmtree(cache_dir)
            os.makedirs(cache_dir)
            print(f"Cleared the contents of the '{cache_dir}' directory.")
        except PermissionError as e:
            print(
                f"PermissionError: {e}. Failed to clear the '{cache_dir}' directory."
            )
    else:
        print(f"The directory '{cache_dir}' does not exist.")


async def clear_pages_cache():
    pages_dir = 'pages'
    if os.path.exists(pages_dir) and os.path.isdir(pages_dir):
        try:
            shutil.rmtree(pages_dir)
            os.makedirs(pages_dir)
            print(f"Cleared the contents of the '{pages_dir}' directory.")
        except PermissionError as e:
            print(f"PermissionError: {e}. Failed to clear the '{pages_dir}' directory.")
    else:
        print(f"The directory '{pages_dir}' does not exist.")
