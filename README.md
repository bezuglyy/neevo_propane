# Neevo Propane (Home Assistant, HACS)

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
![HA Version](https://img.shields.io/badge/HA-2024.6%2B-25A162)
![IoT Class](https://img.shields.io/badge/IoT%20class-cloud__polling-795548)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

Кастом-интеграция для Home Assistant, читающая данные **OtoData Neevo** (уровень пропана и температура) через облачное API. Настраивается через **Config Flow** (UI), поддерживает установку через **HACS**.

---

## Возможности
- 🧪 **Датчики**:  
  - `Level` — уровень пропана, %  
  - `Temperature` — температура, °C (если доступна у устройства)
- ⚙️ **Настройки в UI**: интервал опроса (по умолчанию **180 секунд**)
- 🧩 **Несколько устройств**: добавляйте интеграцию повторно для разных баков (каждый entry — один бак)
- 🛡️ **Только чтение**: интеграция делает GET к официальному Neevo API
- 🌐 **iot_class**: `cloud_polling`

---

## Требования
- Home Assistant **2024.6+**
- Аккаунт/токен для **OtoData Neevo** (значение из заголовка `Authorization: Basic <base64>`).  
  **Важно:** вводите **только** сам base64 (без слова `Basic`).

---

## Установка

### Вариант A — через HACS (Custom Repository)
1. Открой **HACS → Integrations → меню (⋮) → Custom repositories**.  
2. Добавь ссылку на этот репозиторий как **Integration**.  
3. Установи **Neevo Propane** и перезапусти Home Assistant.  
4. **Settings → Devices & Services → Add Integration → Neevo Propane**.  
5. Введите **Base64 токен** (без `Basic`) → дождитесь списка устройств → выберите нужный бак.  
6. (Опционально) В **Options** задайте интервал опроса (секунды).

### Вариант B — вручную
1. Скопируй папку `custom_components/neevo_propane` в `/config/custom_components/`.  
2. Перезапусти HA.  
3. Добавь интеграцию в **Settings → Devices & Services** как выше.

---

## Откуда взять токен?
Если в запросах к API у вас есть заголовок:
