# database/__init__.py
from .db import get_db, init_db
from .queries import save_recommendation, update_market_prices, get_all_recommendations

__all__ = ['get_db', 'init_db', 'save_recommendation', 'update_market_prices', 'get_all_recommendations']