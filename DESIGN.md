# Дизайн-документ  системы - TextMorph

## 1. Цели и предпосылки

### 1.1. Цель проекта
Создание системы, преобразующей повествовательные тексты (сказки, песни, рассказы) в анимированные визуализации с использованием машинного обучения и технологий StableDiffusion и Stable Video Diffusion.

### 1.2. Бизнес value
Современный контент-маркетинг требует визуализации текстового контента для лучшего взаимодействия с аудиторией. Решение позволит автоматизировать превращение текстов в анимации и видео, ускоряя создание контента и расширяя его возможности.

## 2. Метрики качества и технические требования

### 2.1. Метрики качества
1. Время генерации анимации (<10 минут для 20-секундного видео).
2. Анимации отражают основные идеи входного текста.
3. Валидации качества генерации видео.

## 3. Задачи проекта

1. Разбиение входного текста на смысловые блоки.
2. Генерация промптов для создания изображений.
3. Подбор и настройка моделей для генерации изображений и видео.
4. Создание набора изображений и их преобразование в анимации и видео.
5. Разработка интуитивно понятного UI для взаимодействия с системой.

## 4. Ограничения и масштабирование

### 4.1. Ограничения
1. Ограничение длины входного текста до 10 000 символов.
2. Не включает редактирование готовых анимаций.

### 4.2. Масштабирование
1. Горизонтальное масштабирование на нескольких серверах.
2. Использование мощных CPU и/или GPU для ускорения обработки запросов.

# 5. Реализация и тестирование

### 5.1 Тестирование модели

- Проведение ряда тестов для оценки качества и реализма генерируемых видео.
- Сравнение результатов с человеческими оценками и существующими стандартами в области видеопроизводства.

### 5.2 Пилотное внедрение

- Внедрение модели в контролируемые среды для демонстрации ее возможностей потенциальным пользователям и сбора обратной связи у ЦА.
- Внедрение формы ОС, для оценки генерации видеоряда.
- Визуальная валидация модератором некоторого количества сгенерированных видеорядов.

## 5. Архитектура и инфраструктура

### 5.1 Web Архитектура системы

### Компоненты Системы:
TBD - диаграмма 
1. Интерфейс пользователя (UI): Веб-приложение, позволяющее пользователям отправлять текстовые запросы и изображения, а также получать сгенерированные видео.

2. API сервер: Сервер, который обрабатывает запросы от UI, взаимодействует с моделями и возвращает результаты.

3. AI/ML Модуль Stable Video Diffusion: Центральный компонент, отвечающий за генерацию видео. Включает в себя другие подсистемы.

4. Система хранения данных: Включает в себя тексты, изображения и видео. В форматах JSON и NoSQL.

5. Облачная инфраструктура: Используется для масштабирования вычислительных и хранилищных ресурсов.



### 5.2. ML (AI) Архитектура, Пайплайн (TBD) - Никита О.
1. Модуль обработки текста.
2. Модуль генерации сценария с использованием LLM.
3. Модуль генерации анимации и видео с использованием StableDiffusion и Stable Video Diffusion.

### 5.2. Инфраструктура
1. Использование облачных платформ для доступа к вычислительным и хранилищным ресурсам.
2. Развертывание модели в высокопроизводительной инфраструктуре.
3. GPU - RTX3090ti with 24GB VRAM. 

### 5.3. Безопасность и соответствие законодательству
Принятие мер для защиты персональных данных и соблюдения нормативных требований.

## 6. Заключение
Этот проект объединяет передовые технологии в области машинного обучения для создания инновационных решений в сфере цифрового контента, открывая новые возможности для визуализации текстового контента.