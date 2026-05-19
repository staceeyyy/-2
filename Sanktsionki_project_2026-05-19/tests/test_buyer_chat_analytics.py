from __future__ import annotations

import json

from sanktsionki.services.buyer_chat_analytics import (
    build_buyer_chat_summary,
    extract_amount_mentions,
    load_telegram_export,
)


def test_buyer_chat_pipeline_extracts_core_metrics(tmp_path) -> None:
    export_path = tmp_path / "buyer_chat.json"
    export_path.write_text(
        json.dumps(
            {
                "messages": [
                    {
                        "id": 1,
                        "date": "2026-05-10T11:00:00",
                        "from": "buyer_admin",
                        "text": "Nike Air Force 1 из Китая: комиссия 1200 руб, доставка 1800 руб, под ключ 14500.",
                    },
                    {
                        "id": 2,
                        "date": "2026-05-11T10:40:00",
                        "from": "buyer_admin",
                        "text": "По Jordan комиссия 1800 руб, логистика 3200 руб, таможня 900 руб.",
                    },
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    messages = load_telegram_export(export_path)
    mentions = extract_amount_mentions(messages)
    summary = build_buyer_chat_summary(mentions)

    assert len(messages) == 2
    assert {"commission", "delivery", "total", "customs"} <= set(summary["metric"])
    assert mentions["country_name"].dropna().iloc[0] == "Китай"
    assert set(mentions["country_name"].dropna()) == {"Китай"}
