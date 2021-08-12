from maid_manga_id import MaidManga
import asyncio

if __name__ == '__main__':
    maid = MaidManga()

    async def main():
        manga = await maid.info('kanojo mo kanojo')
        print(manga)

    asyncio.get_event_loop().run_until_complete(main())