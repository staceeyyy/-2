from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from sanktsionki.utils import clean_whitespace, infer_brand, slugify_query


@dataclass(slots=True)
class SearchQuery:
    slug: str
    label: str
    brand: str
    category: str

    @classmethod
    def from_text(cls, raw_query: str, category: str = "sneakers") -> "SearchQuery":
        cleaned = clean_whitespace(raw_query)
        return cls(
            slug=slugify_query(cleaned),
            label=cleaned,
            brand=infer_brand(cleaned),
            category=category,
        )


@dataclass(slots=True)
class ProductOffer:
    query_slug: str
    query_label: str
    source_name: str
    source_type: str
    title: str
    brand: str
    category: str
    price_rub: int
    old_price_rub: int | None
    location: str | None
    seller: str | None
    listing_url: str
    image_url: str | None
    availability_note: str | None
    match_score: float
    collected_at: str
    raw_snippet: str | None = None
    country_name: str | None = None
    market_scope: str | None = None
    source_domain: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def timestamp(cls) -> str:
        return datetime.now(timezone.utc).isoformat()
