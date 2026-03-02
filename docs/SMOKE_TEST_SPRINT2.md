# Smoke test — SeafarerApp после Sprint 2

Дата: 2026-02-25.  
Проверка: запуск backend/frontend, UI /jobs, фильтры, Load more, /jobs/[id], ошибки.

---

## 1. Что проверено

### 1.1 Backend запускается

- **Результат:** OK  
- **Как проверяли:** В среде выполнения запущен uvicorn из корня проекта:
  ```powershell
  Set-Location backend; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```
- **Вывод:** `Uvicorn running on http://0.0.0.0:8000`, `Application startup complete`.
- **Примечание:** На Windows в части окружений `make` недоступен — запускать backend напрямую (см. выше).

### 1.2 Frontend запускается

- **Результат:** Не проверено в автоматическом режиме  
- **Причина:** В среде выполнения не найден `npm`/`npx` (Node.js не в PATH).  
- **Рекомендация:** Запуск вручную на своей машине:
  ```powershell
  cd frontend
  npm run dev
  ```
  Либо через Make (если установлен): `make frontend`.

### 1.3 Сборка и линт фронтенда

- **Результат:** Линт — без замечаний  
- **Проверенные файлы:**  
  `frontend/src/app/jobs/page.tsx`, `frontend/src/app/jobs/[id]/page.tsx`,  
  `frontend/src/lib/api.ts`, `frontend/src/components/JobCard.tsx`  
- **Сборка (next build):** Не выполнялась (нет Node в PATH в среде теста).

### 1.4 Код страницы деталей и API

- **Результат:** Код проверен, линт чист  
- **Детали:**
  - Тип `JobDetail` и `getJobById()` в `api.ts` — без изменений, используются на странице.
  - Страница `/jobs/[id]`: `useParams()`, загрузка через `getJobById(id, initData)`, разметка с Card/Badge/Button, все поля через `displayText`/`formatDate`/`formatSalary` с защитой от null/undefined.
  - Обработка ошибок: 401 → Unauthorized, 404 → Job not found, 429 → Too many requests, 500+ → Server error.

---

## 2. Что не проверено (нужна ручная проверка)

- Фактическая загрузка списка на `/jobs` в браузере.
- Работа фильтров (search, rank, vessel_type) и изменение URL.
- Кнопка «Load more».
- Переход по карточке на `/jobs/[id]` и отображение деталей.
- Поведение при пустых полях вакансии (не падает ли страница).
- Отображение ошибок 401/404/429 в UI (при возможности воспроизведения).
- Отсутствие ошибок в консоли браузера и в логах Next.js.

---

## 3. Что сломано

- В среде выполнения агента: **ничего не сломано** в коде.  
- Backend успешно стартует.  
- Frontend и полный UI-сценарий не проверялись из-за отсутствия Node/npm в PATH.

---

## 4. Как воспроизвести проверку у себя

### 4.1 Backend

```powershell
cd c:\0_ROOT\10_ACTIVE\01_Main_Project\SeafarerApp\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Открыть: `http://localhost:8000/health` — ожидается JSON с `status: ok`.

### 4.2 Frontend

```powershell
cd c:\0_ROOT\10_ACTIVE\01_Main_Project\SeafarerApp\frontend
npm run dev
```

- В `frontend/.env.local` задать (для локального dev):
  - `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`
  - `NEXT_PUBLIC_DEV_TG_INIT_DATA=<валидная initData строка для теста>`

### 4.3 Сценарии в браузере

1. **Список вакансий**  
   Открыть `http://localhost:3000/jobs` — список должен загрузиться (при валидном initData).

2. **Фильтры и URL**  
   Ввести поиск, выбрать rank и vessel_type — в адресной строке должны появиться/обновиться query-параметры (`?search=...&rank=...&vessel_type=...`).

3. **Load more**  
   Если есть следующая страница — нажать «Load more», должны подгрузиться ещё вакансии.

4. **Деталь вакансии**  
   Клик по карточке → переход на `http://localhost:3000/jobs/<id>`. Должны отображаться заголовок, описание, условия, блок «Vessel & company», кнопка «← Back to jobs».

5. **Пустые поля**  
   Вакансия с минимальным набором полей (или пустые description, salary и т.д.) — страница не должна падать, должны быть подписи вроде «Not specified» / «No description provided.»

6. **Ошибки**  
   - **401:** убрать/очистить `NEXT_PUBLIC_DEV_TG_INIT_DATA`, перезагрузить `/jobs` или `/jobs/[id]` — ожидается сообщение про открытие в Telegram или настройку dev initData.  
   - **404:** открыть `http://localhost:3000/jobs/non-existent-id` — ожидается «Job not found.»  
   - **429:** при возможности вызвать rate limit на API — ожидается «Too many requests. Please try again later.»

7. **Консоль**  
   В DevTools (Console) не должно быть красных ошибок при обычном сценарии (список → фильтры → деталь).

---

## 5. Минимальные правки (если понадобятся)

- **Код:** по результатам smoke-теста правки не требуются.  
- **Окружение:**  
  - Если на Windows нет `make`, использовать прямые команды выше для backend и `npm run dev` для frontend.  
  - Для стабильного локального теста задать `NEXT_PUBLIC_DEV_TG_INIT_DATA` в `frontend/.env.local`.

---

## 6. Краткий чеклист для ручного прогона

| # | Проверка | Ожидание |
|---|----------|----------|
| 1 | Backend запускается | `uvicorn` слушает 8000, `/health` → `status: ok` |
| 2 | Frontend запускается | `npm run dev`, приложение на 3000 |
| 3 | /jobs загружает список | Карточки вакансий, без ошибок в консоли |
| 4 | Фильтры меняют URL | `?search=...&rank=...&vessel_type=...` в адресе |
| 5 | Load more работает | Подгружаются следующие элементы |
| 6 | Переход на /jobs/[id] | Детальная страница с данными вакансии |
| 7 | Пустые поля не ломают страницу | «Not specified» / «No description provided.» |
| 8 | 401/404/429 отображаются | Сообщения об ошибках в UI |
| 9 | Нет ошибок сборки/рантайма | Чистая консоль браузера и терминал Next |
