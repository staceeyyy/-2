from __future__ import annotations

from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from sanktsionki import config
from sanktsionki.models import ProductOffer, SearchQuery
from sanktsionki.scrapers.base import SeleniumEdgeScraper
from sanktsionki.utils import absolute_url, parse_price


class AvitoScraper(SeleniumEdgeScraper):
    source_name = "Avito"
    source_type = "dynamic"

    def search(self, query: SearchQuery, limit: int = 10) -> list[ProductOffer]:
        url = f"{config.AVITO_BASE_URL}/all/odezhda_obuv_aksessuary?q={quote_plus(query.label)}"
        soup = BeautifulSoup(self._render_html(url), "html.parser")
        offers: list[ProductOffer] = []

        for item in soup.select('[data-marker="item"]'):
            title_link = item.select_one('[data-marker="item-title"]')
            price_value = item.select_one('[data-marker="item-price-value"]') or item.select_one('[data-marker="item-price"]')
            photo_link = item.select_one('[data-marker="item-photo-sliderLink"]')
            image = item.select_one('img[itemprop="image"]')
            location = item.select_one('[data-marker="item-location"]')
            seller = item.select_one('[data-marker="seller-info/summary"]')
            note = item.select_one('[data-marker="badge-title-2359"]')
            description = item.select_one('meta[itemprop="description"]')

            title = title_link.get_text(" ", strip=True) if title_link else ""
            price_rub = parse_price(price_value.get_text(" ", strip=True) if price_value else "")
            raw_snippet = item.get_text(" ", strip=True)
            score = self._is_relevant(
                query,
                title,
                description.get("content") if description else "",
                raw_snippet,
            )

            if not title or price_rub is None or score < 0.5:
                continue

            offers.append(
                self._offer(
                    query,
                    title=title,
                    price_rub=price_rub,
                    location=location.get_text(" ", strip=True) if location else None,
                    seller=seller.get_text(" ", strip=True) if seller else None,
                    listing_url=absolute_url(
                        config.AVITO_BASE_URL,
                        photo_link.get("href") if photo_link else None,
                    ),
                    image_url=image.get("src") if image else None,
                    availability_note=note.get_text(" ", strip=True) if note else None,
                    raw_snippet=description.get("content") if description else raw_snippet,
                    match_override=score,
                    market_scope="marketplace",
                    source_domain="avito.ru",
                )
            )
            if len(offers) >= limit:
                break

        return offers
