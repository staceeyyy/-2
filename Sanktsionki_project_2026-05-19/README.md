# Sanktsionki.net

## Что это за проект
`Sanktsionki.net` — учебный data science проект про поиск выгодных предложений на популярные модели кроссовок ушедших брендов. Система собирает предложения с локального retail, marketplace и международного канала, сравнивает цены и показывает, где модель дешевле.

В текущей версии пользователь может:
- посмотреть сохраненный срез рынка по базовым моделям;
- запустить live-поиск по произвольной модели или артикулу;
- сравнить локальные и cross-border предложения;
- оценить комиссии и логистику байеров по Telegram-чатам;
- выгрузить результаты в Google Sheets.

## Что закрыто по требованиям продвинутой группы
- ООП-архитектура: модели данных, базовые классы парсеров, сервисный слой, CLI.
- Статический парсинг: `Lamoda`, `Sneakerhead`.
- Динамический парсинг через `Selenium`: `Avito`.
- Дашборды на `Dash`: интерактивный интерфейс с KPI, графиками, heatmap и live-поиском.

Дополнительно реализовано:
- `Google Sheets API` для выгрузки результатов;
- международный источник `CDEK.Shopping`;
- аналитика по экспортам Telegram-чатов байеров;
- история выгрузок в `offers_history.csv`.

Подробная карта соответствия критериям лежит в [docs/criteria_mapping.md](/C:/Users/vadim/Desktop/настя1/docs/criteria_mapping.md).

## Источники данных
- `Lamoda` — статическая выдача по поисковому запросу.
- `Sneakerhead` — статическая выдача по поисковому запросу.
- `Avito` — динамически отрендеренная выдача через `Selenium` и `Edge`.
- `CDEK.Shopping` — международные предложения через публичный search endpoint.
- `Telegram export` — JSON-выгрузки из buyer-чатов для оценки комиссий, доставки и total cost.

## Бизнес-идея
После ухода части международных fashion-брендов покупателю стало сложнее быстро понять:
- где купить оригинальную пару без сильной переплаты;
- когда выгоднее local retail, а когда cross-border канал;
- насколько итоговая цена вырастает из-за комиссии байера и доставки.

Проект отвечает на эти вопросы в формате исследовательской аналитической системы.

## Что реализовано в коде
- Единая модель `ProductOffer` для всех площадок.
- Пайплайн сбора данных `OfferPipeline`.
- Нормализация офферов и сбор итоговых CSV.
- Дашборд из трех частей:
  - сохраненный срез рынка;
  - live-поиск по текстовому запросу;
  - аналитика по buyer-чатам.
- CLI-скрипты для сбора, анализа чатов, экспорта в Google Sheets и запуска дашборда.

## Структура репозитория
```text
src/sanktsionki/
  config.py
  models.py
  utils.py
  cli.py
  scrapers/
    base.py
    avito.py
    cdek_shopping.py
    lamoda.py
    sneakerhead.py
  services/
    analytics.py
    buyer_chat_analytics.py
    google_sheets.py
    normalization.py
    pipeline.py
  dashboard/
    app.py
    assets/style.css
scripts/
  analyze_buyer_chats.py
  collect_offers.py
  export_google_sheets.py
  run_dashboard.py
data/
  input/
    buyer_chats/
      sample_buyer_chat.json
  raw/
  processed/
docs/
  criteria_mapping.md
  presentation_outline.md
  research_findings.md
tests/
```

## Как запустить
1. Установить зависимости:
```powershell
py -3 -m pip install -r requirements.txt
```

2. Собрать сохраненный срез рынка:
```powershell
$env:PYTHONPATH='src'
py -3 scripts/collect_offers.py --limit 4
```

3. При необходимости собрать ad hoc запрос:
```powershell
$env:PYTHONPATH='src'
py -3 scripts/collect_offers.py --limit 4 --text-query "Nike Air Force 1 07 white"
```

4. Построить аналитику по buyer-чатам:
```powershell
$env:PYTHONPATH='src'
py -3 scripts/analyze_buyer_chats.py
```

5. Запустить дашборд:
```powershell
$env:PYTHONPATH='src'
py -3 scripts/run_dashboard.py
```

6. При наличии сервисного аккаунта выгрузить результаты в Google Sheets:
```powershell
$env:PYTHONPATH='src'
$env:GOOGLE_SERVICE_ACCOUNT_FILE='C:\\path\\to\\service-account.json'
py -3 scripts/export_google_sheets.py --spreadsheet-id <SPREADSHEET_ID>
```

## Актуальные результаты в репозитории
После последнего прогона в [data/processed/offers.csv](/C:/Users/vadim/Desktop/настя1/data/processed/offers.csv) сохранено `55` офферов по `5` базовым запросам.

Лучшие минимальные цены по моделям:

| Модель | Лучшая площадка | Минимальная цена |
|---|---|---:|
| adidas samba | Lamoda | 5 999 ₽ |
| air force 1 | Avito | 7 490 ₽ |
| air max 90 | CDEK.Shopping | 10 479 ₽ |
| new balance 530 | CDEK.Shopping | 8 055 ₽ |
| new balance 574 | CDEK.Shopping | 6 452 ₽ |

Ключевой вывод: cross-border канал выигрывает по нескольким моделям даже с учетом типичной медианной логистики из buyer-чатов.

## Buyer-чаты
В репозитории лежит пример экспорта: [sample_buyer_chat.json](/C:/Users/vadim/Desktop/настя1/data/input/buyer_chats/sample_buyer_chat.json).

По sample-данным получаются такие медианы:
- комиссия байера — `1 350 ₽`;
- доставка — `2 400 ₽`;
- total под ключ — `18 900 ₽`;
- таможня — `1 300 ₽`.

Эти агрегаты используются как дополнительный аналитический слой для оценки реальной стоимости cross-border закупки.

## Ограничения
- Парсеры зависят от текущей верстки и структуры сайтов.
- `Avito` требует установленный `Microsoft Edge`.
- Buyer-чаты анализируются по текстовым эвристикам, поэтому это исследовательская, а не бухгалтерская оценка расходов.
- Цены актуальны только на момент конкретной выгрузки.

## Материалы для защиты
- [docs/research_findings.md](/C:/Users/vadim/Desktop/настя1/docs/research_findings.md)
- [docs/presentation_outline.md](/C:/Users/vadim/Desktop/настя1/docs/presentation_outline.md)
- [docs/criteria_mapping.md](/C:/Users/vadim/Desktop/настя1/docs/criteria_mapping.md)

## Референсы
- [Sanktsionki.net](https://github.com/chinchilla1337/Sanktsionki.net/tree/main)
- [GetCarz](https://github.com/SergoDobro/GetCarz/tree/avito)
- [project_hse](https://github.com/jetminded/project_hse/tree/main)

Код в этом репозитории написан под текущую тему и текущий набор источников. Открытые репозитории использовались только как ориентир по формату учебного проекта и структуре сдачи.
