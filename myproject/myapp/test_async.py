import asyncio

from myapp.views import get_product_info

class MockRequest:
    def __init__(self, search):
        self.GET = {'search': search}

request = MockRequest(search_query='emaple_search')

async def main():
    product_list = await get_product_info(request)
    print(product_list)

asyncio.run(main())