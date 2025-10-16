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

# Neevo Propane – карточка уровня в виде баллона (Home Assistant)

Кастомный виджет на базе **button-card**, отображающий уровень пропана в стилизованном виде **газового баллона** с плавной заливкой, цветовой индикацией уровня и лёгкой «инерцией» текста процента.

---

## Визуальный стиль в виде баллона

- **Форма баллона** реализована через SVG-маску (`mask` / `-webkit-mask`), поэтому заливка остаётся чёткой на любом размере.
- **Плавная заливка**: градиент «снизу вверх» изменяет высоту в зависимости от процента.
- **Цветовая шкала**:
  - `< 15%` — красный (критично)
  - `< 35%` — оранжевый (низкий)
  - `≥ 35%` — голубой (норма)
- **Инерция текста**: при обновлении значения процент «подпрыгивает» (fade + translate), создавая ощущение живости.
- Поддерживает тёмную/светлую темы благодаря полупрозрачным цветам и мягкой внутренней тени.

> Карточка не требует дополнительных фронтенд-аддонов, кроме установленного **custom:button-card**.

---

## Требования

- Home Assistant с установленной **button-card**.
- Сенсор уровня: `sensor.neevo_propane_<id>_level`  
  (из интеграции «Neevo Propane» или любой другой источник уровня в %).

> В примере ниже стоит временная сущность `sensor.neevo_propane_none_level`. Замените её на вашу **реальную**.

---

## Установка

1. Убедитесь, что **button-card** установлен (через HACS → Frontend).
2. Скопируйте YAML ниже в вашу Lovelace-дашборд-карточку (Raw configuration editor или UI-карточку «button-card»).
3. Замените `entity` на ваш фактический сенсор уровня.

---

## Конфигурация (пример)

```yaml
type: custom:button-card
entity: sensor.neevo_propane_none_level   # ← замените на реальный entity_id
name: Пропан
show_icon: false
show_state: true
tap_action:
  action: more-info
triggers_update:
  - sensor.neevo_propane_none_level
state_display: |
  [[[
    const v = Number(entity?.state);
    if (isNaN(v)) return '—';
    return `${Math.max(0, Math.min(100, v)).toFixed(0)}%`;
  ]]]
styles:
  grid:
    - grid-template-areas: "\"n\" \"s\""
    - grid-template-rows: 1fr auto
    - grid-template-columns: 1fr
  name:
    - justify-self: center
    - padding-top: 6px
    - font-weight: 700
    - font-size: 1.8rem
  state:
    - justify-self: center
    - padding-bottom: 10px
    - font-weight: 800
    - font-size: 3.8rem
    - transition: transform 300ms ease, opacity 300ms ease
    - transform: translateY(0)
    - opacity: 1
  card:
    - height: 140px
    - width: 202px
    - padding: 0
    - border-radius: 20px
    - box-shadow: inset 0 0 0 2px rgba(255,255,255,0.15)
    - transition: background 1.2s cubic-bezier(0.22, 1, 0.36, 1)
    - will-change: background
    - background: |
        [[[
          const raw = Number(entity?.state);
          const pct = isNaN(raw) ? 0 : Math.max(0, Math.min(100, raw));
          const color = pct < 15 
            ? 'rgba(239,68,68,0.92)'      // красный
            : (pct < 35 
              ? 'rgba(245,158,11,0.92)'   // оранжевый
              : 'rgba(56,189,248,0.92)'); // голубой
          // Мягкий «подлёт» текста при смене числа
          const el = this?.shadowRoot?.querySelector('.state');
          if (el) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(6px)';
            setTimeout(() => {
              el.style.opacity = '1';
              el.style.transform = 'translateY(0)';
            }, 0);
          }
          return `linear-gradient(to top, ${color} ${pct}%, rgba(255,255,255,0.06) ${pct}%)`;
        ]]]
    - "-webkit-mask": >
        url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg'
        viewBox='0 0 120 240'> <g fill='%23000'>
          <rect x='25' y='46' width='70' height='140' rx='18' ry='18'/>
          <ellipse cx='60' cy='46' rx='35' ry='12'/>
          <ellipse cx='60' cy='186' rx='35' ry='12'/>
          <rect x='40' y='20' width='40' height='28' rx='6'/>
          <rect x='50' y='8'  width='20' height='12' rx='3'/>
        </g> </svg>") no-repeat center / contain
    - mask: >
        url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg'
        viewBox='0 0 120 240'> <g fill='%23000'>
          <rect x='25' y='46' width='70' height='140' rx='18' ry='18'/>
          <ellipse cx='60' cy='46' rx='35' ry='12'/>
          <ellipse cx='60' cy='186' rx='35' ry='12'/>
          <rect x='40' y='20' width='40' height='28' rx='6'/>
          <rect x='50' y='8'  width='20' height='12' rx='3'/>
        </g> </svg>") no-repeat center / contain

