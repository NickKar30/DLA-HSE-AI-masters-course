# Домашнее задание 4: Fine-tuning MusicGen

В этом домашнем задании вам предстоит провести **fine-tuning** модели MusicGen из репозитория [AudioCraft](https://github.com/facebookresearch/audiocraft).

**Максимальный балл:** 100 баллов
*   **50 баллов:** Реализация пайплайна (код, сбор данных, модификация AudioCraft, запуск обучения).
*   **50 баллов:** Качество генерации и следование промптам (оценивается по 5 тестовым заданиям).

---

## Часть 1. Реализация пайплайна (50 баллов)

В этой части вам предстоит написать код для подготовки данных и настройки обучения. Результатом должен быть рабочий репозиторий и запущенный процесс файнтюнинга.

### 1. Сбор данных MusicCaps (10 баллов)
Датасет [MusicCaps](https://huggingface.co/datasets/google/MusicCaps) содержит ссылки на YouTube и текстовые описания.
*   Напишите скрипт для скачивания аудио.
*   **Важно:** Не скачивайте видео целиком! Используйте связку `yt-dlp` (для получения прямой ссылки на аудиопоток) и `ffmpeg` (для скачивания конкретного 10-секундного фрагмента напрямую в `.wav` формате.

### 2. Обогащение метаданных с помощью LLM (15 баллов)
Оригинальные описания в MusicCaps — это просто сплошной текст. MusicGen лучше обучается на структурированных данных.
*   Используйте любую LLM (OpenAI, Gemini, Claude, локальную Llama 3), чтобы перевести сырые текстовые описания (`caption`) в строгий JSON-формат.
*   **Обязательная схема JSON для каждого трека:**
    ```json
    {
      "description": "string",
      "general_mood": "string",
      "genre_tags": ["string"],
      "lead_instrument": "string",
      "accompaniment": "string",
      "tempo_and_rhythm": "string",
      "vocal_presence": "string",
      "production_quality": "string"
    }
    ```
*   Сохраните результаты в виде `.json` файлов рядом с каждым `.wav` файлом (или соберите в один большой JSON и напишите скрипт-импортер).

### 3. Модификация AudioCraft (15 баллов)
По умолчанию [AudioCraft](https://github.com/facebookresearch/audiocraft) не знает про ваши новые поля.

*   Сделайте форк/клон репозитория AudioCraft.
*   Найдите датакласс `MusicInfo` (обычно в `audiocraft/data/music_dataset.py`) и добавьте туда новые поля из вашей JSON-схемы.
*   Обновите логику чтения метаданных, чтобы при загрузке датасета эти поля корректно парсились и передавались в текстовый энкодер.

### 4. Настройка конфигов и запуск обучения (10 баллов)
*   Создайте манифесты (`.jsonl.gz`) для train и valid выборок.
*   Настройте конфигурацию Hydra.
*   **Важно:** Убедитесь, что параметры `merge_text_p` и `drop_desc_p` (или `drop_other_p`) настроены так, чтобы модель обращала внимание на ваши новые структурированные поля, но при этом сохраняла способность к Classifier-Free Guidance.
*   Запустите файнтюнинг модели `musicgen-small` или `musicgen-medium` на собранном датасете.

---

## Часть 2. Оценка качества генерации (50 баллов)

После того как ваша модель обучится, вам нужно сгенерировать 5 треков (длительностью 10-15 секунд) по заранее заданным структурированным промптам. 

Каждый сгенерированный трек оценивается в **10 баллов** (5 баллов за качество звука/отсутствие артефактов + 5 баллов за точное следование всем полям промпта).

### Тестовые промпты для инференса:

**Промпт 1:**
```json
{
  "description": "An epic and triumphant orchestral soundtrack featuring powerful brass and a sweeping string ensemble, driven by a fast march-like rhythm and an epic background choir, recorded with massive stadium reverb.",
  "general_mood": "Epic, heroic, triumphant, building tension",
  "genre_tags": ["Cinematic", "Orchestral", "Soundtrack"],
  "lead_instrument": "Powerful brass section (horns, trombones)",
  "accompaniment": "Sweeping string ensemble, heavy cinematic percussion, timpani",
  "tempo_and_rhythm": "Fast, driving, march-like rhythm",
  "vocal_presence": "Epic choir in the background (wordless chanting)",
  "production_quality": "High fidelity, wide stereo image, massive stadium reverb"
}
```
**Промпт 2:**
```json
{
  "description": "A relaxing lo-fi hip-hop instrumental with a muffled electric piano playing jazz chords over a dusty vinyl crackle, deep sub-bass, and a slow boom-bap drum loop.",
  "general_mood": "Relaxing, nostalgic, chill, melancholic",
  "genre_tags": ["Lo-Fi Hip Hop", "Chillhop", "Instrumental"],
  "lead_instrument": "Muffled electric piano (Rhodes) playing jazz chords",
  "accompaniment": "Dusty vinyl crackle, deep sub-bass, soft boom-bap drum loop",
  "tempo_and_rhythm": "Slow, laid-back, swinging groove",
  "vocal_presence": "None",
  "production_quality": "Lo-Fi, vintage, warm tape saturation, slightly muffled high frequencies"
}
```

**Промпт 3:**
```json
{
  "description": "An energetic progressive house dance track with a bright detuned synthesizer lead, pumping sidechain bass, and chopped vocal samples over a fast four-on-the-floor beat.",
  "general_mood": "Energetic, uplifting, party vibe, euphoric",
  "genre_tags": ["EDM", "Progressive House", "Dance"],
  "lead_instrument": "Bright, detuned synthesizer lead",
  "accompaniment": "Pumping sidechain bass, risers, crash cymbals",
  "tempo_and_rhythm": "Fast, driving, strict four-on-the-floor beat",
  "vocal_presence": "Chopped vocal samples used as a rhythmic instrument",
  "production_quality": "Modern, extremely loud, punchy, club-ready mix"
}
```

**Промпт 4:**
```json
{
  "description": "An intimate acoustic folk instrumental featuring a fingerpicked acoustic guitar, light tambourine, and subtle upright bass, played in a gentle waltz-like rhythm.",
  "general_mood": "Intimate, warm, acoustic, peaceful",
  "genre_tags": ["Folk", "Acoustic", "Indie"],
  "lead_instrument": "Fingerpicked acoustic guitar",
  "accompaniment": "Light tambourine, subtle upright bass, distant ambient room sound",
  "tempo_and_rhythm": "Mid-tempo, gentle, waltz-like triple meter",
  "vocal_presence": "None",
  "production_quality": "Raw, organic, close-mic recording, natural room acoustics"
}
```

**Промпт 5:**
```json
{
  "description": "A dark cyberpunk synthwave instrumental driven by an aggressive distorted analog bass synthesizer, arpeggiated synth plucks, and a retro 80s drum machine.",
  "general_mood": "Dark, futuristic, gritty, mysterious",
  "genre_tags": ["Synthwave", "Cyberpunk", "Darkwave"],
  "lead_instrument": "Aggressive, distorted analog bass synthesizer",
  "accompaniment": "Arpeggiated synth plucks, retro 80s drum machine (gated snare)",
  "tempo_and_rhythm": "Driving, mid-tempo, robotic precision",
  "vocal_presence": "None",
  "production_quality": "Retro-futuristic, heavy compression, synthetic, 80s aesthetic"
}
```

---

## Формат сдачи
1. Ссылка на GitHub-репозиторий с вашим кодом (скрипты парсинга, модифицированный AudioCraft, скрипты инференса).
2. Ссылка на веса обученной модели (HuggingFace / Google Drive).
3. Папка с 5 сгенерированными `.wav` файлами, названными `prompt_1.wav` ... `prompt_5.wav`.
4. Краткий отчет (Markdown/PDF) с описанием:
   * С какими трудностями столкнулись?
   * Какую LLM использовали для парсинга и какой системный промпт сработал лучше всего?
   * Какие гиперпараметры обучения (learning rate, batch size, steps) вы использовали?
   * Приложите логи обучения (ссылку на WandB/CometML), чтобы можно было оценить процесс обучения.

**Важно:**
Как и в Дз2 и Дз3, мы обращаем внимание на читаемость кода и наличие понятной документации. Если код невозможно читать или `README` непонятен, оценка за работу может быть снижена.
Ваш `README` в репозитории должен четко объяснять:
1. Как собрать и подготовить датасет.
2. Как запустить процесс обучения.
3. Как запустить инференс.
