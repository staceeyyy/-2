from __future__ import annotations

import pandas as pd

from sanktsionki.utils import offer_link_markdown


def offers_to_frame(records: list[dict[str, object]]) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()

    frame = pd.DataFrame(records)
    defaults: dict[str, object] = {
        "old_price_rub": None,
        "location": None,
        "seller": None,
        "image_url": None,
        "availability_note": None,
        "raw_snippet": None,
        "country_name": None,
        "market_scope": "local",
        "source_domain": None,
    }
    for column_name, default_value in defaults.items():
        if column_name not in frame:
            frame[column_name] = default_value

    frame = frame.drop_duplicates(
        subset=["query_slug", "source_name", "title", "price_rub", "listing_url"],
        keep="first",
    )
    frame["discount_rub"] = (
        frame["old_price_rub"].fillna(frame["price_rub"]) - frame["price_rub"]
    ).clip(lower=0)
    frame["has_discount"] = frame["discount_rub"] > 0
    frame["offer_link"] = frame["listing_url"].apply(offer_link_markdown)
    frame = frame.sort_values(
        ["query_label", "source_name", "price_rub", "match_score"],
        ascending=[True, True, True, False],
    )
    frame.reset_index(drop=True, inplace=True)
    return frame
