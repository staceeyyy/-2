# Соответствие критериям

## Проверка по документу курса
Источник требований: [Проект2026 (1).docx](</C:/Users/vadim/Downloads/Telegram Desktop/Проект2026 (1).docx>).

## Базовые требования
| Требование | Как закрыто |
|---|---|
| 2-3 разных открытых источника | Используются `Lamoda`, `Sneakerhead`, `Avito`, `CDEK.Shopping`, `Telegram export` |
| Хотя бы один статический парсинг | `Lamoda` и `Sneakerhead` |
| Выводы по своей части + графики | Дашборд в [src/sanktsionki/dashboard/app.py](/C:/Users/vadim/Desktop/настя1/src/sanktsionki/dashboard/app.py), выводы в [docs/research_findings.md](/C:/Users/vadim/Desktop/настя1/docs/research_findings.md) |
| Итоговые материалы для презентации | [docs/presentation_outline.md](/C:/Users/vadim/Desktop/настя1/docs/presentation_outline.md) |

## Обязательные требования продвинутой группы
| Требование | Как закрыто |
|---|---|
| ООП | [models.py](/C:/Users/vadim/Desktop/настя1/src/sanktsionki/models.py), [scrapers/base.py](/C:/Users/vadim/Desktop/настя1/src/sanktsionki/scrapers/base.py), [pipeline.py](/C:/Users/vadim/Desktop/настя1/src/sanktsionki/services/pipeline.py) |
| Selenium / Playwright | [avito.py](/C:/Users/vadim/Desktop/настя1/src/sanktsionki/scrapers/avito.py) использует `Selenium` и `Edge` |
| Dash | [app.py](/C:/Users/vadim/Desktop/настя1/src/sanktsionki/dashboard/app.py) |

## Дополнительные темы курса
| Тема | Как закрыто |
|---|---|
| Google Sheets API | [google_sheets.py](/C:/Users/vadim/Desktop/настя1/src/sanktsionki/services/google_sheets.py), [export_google_sheets.py](/C:/Users/vadim/Desktop/настя1/scripts/export_google_sheets.py) |
| Аналитика логистики / total cost | [buyer_chat_analytics.py](/C:/Users/vadim/Desktop/настя1/src/sanktsionki/services/buyer_chat_analytics.py) |
| История данных | [offers_history.csv](/C:/Users/vadim/Desktop/настя1/data/processed/offers_history.csv) |

## Где смотреть результат
- Основной CSV со всеми офферами: [offers.csv](/C:/Users/vadim/Desktop/настя1/data/processed/offers.csv)
- Сводка по площадкам: [market_summary.csv](/C:/Users/vadim/Desktop/настя1/data/processed/market_summary.csv)
- Лучшие офферы: [best_offers.csv](/C:/Users/vadim/Desktop/настя1/data/processed/best_offers.csv)
- Buyer-чаты: [buyer_chat_summary.csv](/C:/Users/vadim/Desktop/настя1/data/processed/buyer_chat_summary.csv)

## Что можно сказать на защите
- В проекте есть и статический, и динамический парсинг.
- Код разделен на модели, парсеры, сервисы и интерфейс.
- Дашборд показывает не только сохраненный срез, но и live-поиск по произвольной модели.
- Международный канал и buyer-чаты добавляют бизнес-смысл, а не просто еще один CSV.
