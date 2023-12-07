from src.utils import seprate_admins
from decouple import config
from src.manual_reserve_handler import ManualReserveHandler
from src.db import DB
import asyncio


if __name__ == '__main__':
    manual_reserve_handler = ManualReserveHandler(
            token=config('TOKEN'),
            admin_ids=seprate_admins(config('ADMIN_ID')),
            log_level=config('LOG_LEVEL', default='INFO'),
            db=DB(
                host=config('DB_HOST', default='127.0.0.1'),
                port=config('DB_PORT', default='27017')
            ),
        )
    asyncio.run(manual_reserve_handler.handle_manual_reserve())