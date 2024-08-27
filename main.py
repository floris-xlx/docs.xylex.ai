import json

import asyncio
from automate.clear_cache import clear_cache
from automate.get_repo import clone_and_checkout
from automate.index_nav_groups import list_folders_in_cache_api, get_navigation_groups, update_navigation_groups
from automate.get_latest_commit import fetch_latest_commit
from automate.sync_nav_tags import sync_nav_tags
from automate.endpoint_router import find_and_extract_endpoints
from automate.content_framer import update_mdx_files_with_parameters

async def main():
    await clear_cache()
    await clone_and_checkout()
    await list_folders_in_cache_api()
    await get_navigation_groups()
    await update_navigation_groups()
    await fetch_latest_commit()
    sync_nav_tags()

    endpoints = find_and_extract_endpoints()
    print(json.dumps(endpoints, indent=4))

    await update_mdx_files_with_parameters(endpoints)

if __name__ == '__main__':
    asyncio.run(main())
