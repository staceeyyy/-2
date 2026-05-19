from __future__ import annotations

import pandas as pd


def build_market_summary(offers: pd.DataFrame) -> pd.DataFrame:
    if offers.empty:
        return pd.DataFrame()

    summary = (
        offers.groupby(["query_slug", "query_label", "source_name", "source_type"], as_index=False)
        .agg(
            offer_count=("title", "count"),
            min_price_rub=("price_rub", "min"),
            median_price_rub=("price_rub", "median"),
            mean_price_rub=("price_rub", "mean"),
            max_price_rub=("price_rub", "max"),
            avg_match_score=("match_score", "mean"),
            discount_share=("has_discount", "mean"),
        )
        .sort_values(["query_label", "min_price_rub", "source_name"])
    )
    summary["price_spread_rub"] = summary["max_price_rub"] - summary["min_price_rub"]
    summary["discount_share"] = (summary["discount_share"] * 100).round(1)
    summary["mean_price_rub"] = summary["mean_price_rub"].round(1)
    summary["median_price_rub"] = summary["median_price_rub"].round(1)
    summary["avg_match_score"] = summary["avg_match_score"].round(3)
    summary["query_best_source"] = (
        summary.groupby("query_slug")["min_price_rub"].transform("min") == summary["min_price_rub"]
    )
    return summary.reset_index(drop=True)


def build_best_offers(offers: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    if offers.empty:
        return pd.DataFrame()

    ranked = offers.sort_values(["query_label", "price_rub", "match_score"], ascending=[True, True, False]).copy()
    ranked["rank_inside_query"] = ranked.groupby("query_slug").cumcount() + 1
    return ranked[ranked["rank_inside_query"] <= top_n].reset_index(drop=True)
