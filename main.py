# import automate.update_json_structure

# if __name__ == '__main__':
#     automate.update_json_structure.update_navigation()


import asyncio
from automate.clear_cache import clear_cache
from automate.get_repo import clone_and_checkout
from automate.index_nav_groups import list_folders_in_cache_api, get_navigation_groups, update_navigation_groups
from automate.get_latest_commit import fetch_latest_commit


async def main():
    await clear_cache()
    await clone_and_checkout()
    await list_folders_in_cache_api()
    await get_navigation_groups()
    await update_navigation_groups()
    await fetch_latest_commit()


if __name__ == '__main__':
    asyncio.run(main())
