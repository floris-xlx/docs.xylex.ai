# import automate.update_json_structure

# if __name__ == '__main__':
#     automate.update_json_structure.update_navigation()


import asyncio
from automate.clear_cache import clear_cache
from automate.get_repo import clone_and_checkout

async def main():
    await clear_cache()
    await clone_and_checkout()

if __name__ == '__main__':
    asyncio.run(main())

