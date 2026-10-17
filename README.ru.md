[English](README.md) · **Русский**

# Dota 2 → Deadlock

Иконки предметов и эффекты Dota 2 в Deadlock.

- **86 иконок предметов**, включая красные и золотые варианты для улучшений.
- Щит **Counterspell** Антимага и зелёная спираль **Refresher**.
- **Shiva’s Guard** для Cold Front, красная волна Arctic Blast и Frostbite.
- Барьеры **Pavise** голубого, золотого и красного цвета.

[Скачать ZIP](https://github.com/hqvdvn-cmd/dota2todeadlock/archive/refs/heads/main.zip) · [Список предметов](docs/ITEMS.md)

## Демонстрация

[![Демонстрация мода](assets/demo/poster.jpg)](assets/demo/showcase.mp4)

**[Смотреть ролик — 27 секунд](assets/demo/showcase.mp4)** · [Скачать видео](https://github.com/hqvdvn-cmd/dota2todeadlock/raw/refs/heads/main/assets/demo/showcase.mp4)

Скин героя на записи установлен отдельно и в комплект не входит.

<details>
<summary>Скриншоты: предметы и эффекты</summary>

**Иконки предметов — нажми на изображение для полного размера.**

<a href="assets/demo/items-800-1600.png"><img src="assets/demo/items-800-1600.png" width="32%" alt="Иконки предметов за 800 и 1600 душ"></a>
<a href="assets/demo/items-3200.png"><img src="assets/demo/items-3200.png" width="32%" alt="Иконки предметов за 3200 душ"></a>
<a href="assets/demo/items-6400.png"><img src="assets/demo/items-6400.png" width="32%" alt="Иконки предметов за 6400 душ"></a>

**Pavise: голубой, золотой и красный варианты.**

<a href="assets/demo/pavise-cyan.png"><img src="assets/demo/pavise-cyan.png" width="32%" alt="Голубой барьер Pavise"></a>
<a href="assets/demo/pavise-gold.png"><img src="assets/demo/pavise-gold.png" width="32%" alt="Золотой барьер Pavise"></a>
<a href="assets/demo/pavise-red.png"><img src="assets/demo/pavise-red.png" width="32%" alt="Красный барьер Pavise на герое и союзнике"></a>

**Cold Front / Shiva.**

![Волна Shiva в Deadlock](assets/demo/cold-front.png)

</details>

## Что нужно

- Deadlock, установленный через Steam на Windows.
- [Python 3.10 или новее](https://www.python.org/downloads/windows/) для установщика.

## Установка

1. [Скачай ZIP](https://github.com/hqvdvn-cmd/dota2todeadlock/archive/refs/heads/main.zip) и распакуй вне папки игры.
2. Закрой Deadlock и мод-менеджер, включая его значок в трее.
3. В Steam открой **Deadlock → Свойства → Установленные файлы → Обзор**. Перейди в `game\citadel` и скопируй путь этой папки.
4. Открой PowerShell в распакованной папке мода и выполни команду ниже. **Замени пример пути к игре на свой.**

```powershell
python scripts/manage.py install --game-dir "D:\SteamLibrary\steamapps\common\Deadlock\game\citadel" --enable-addons --apply
```

Установщик настроит загрузку модов и сохранит доступ к штатной конфигурации игры. Перед изменением он сделает резервную копию. Копии находятся в `.local\backups` внутри распакованной папки мода. Сохрани эту папку.

Если установщик сообщает о занятом или изменённом файле, остановись и проверь другие моды. Не перезаписывай конфликтующий файл.

## Запуск с модом

Дождись завершения обновления Deadlock в Steam. Закрой игру и мод-менеджер, затем выполни команду из папки мода, заменив путь на свой:

```powershell
python scripts/manage.py launch --game-dir "D:\SteamLibrary\steamapps\common\Deadlock\game\citadel" --apply
```

Команда восстановит загрузку модов, если `gameinfo.gi` сбросился, сохранит копию перед изменением конфигурации и передаст запуск Steam. Проверку целостности файлов Steam она не вызывает. Для игры с модом пользуйся этой командой каждый раз; отдельный мод-менеджер необязателен. VPK остаются на месте. Если файлы этого дистрибутива отсутствуют или изменены, команда откажется запускать игру.

Если после команды Steam начал обновление, дождись его завершения, закрой игру, если она открылась, и повтори команду. Восстановление загрузки не обеспечивает совместимость устаревшего мода с новым патчем.

### Обновление мода

Перед заменой папки закрой игру и удали мод командой ниже из **старой копии** дистрибутива. Распакуй новый ZIP в отдельную папку и установи мод оттуда. Сохрани резервные копии. Новая версия установщика откажется перезаписывать пакеты предыдущего выпуска.

### Игра выдаёт «Unable to read default keybinding configuration»

Обнови мод по инструкции выше и используй команду запуска. Она также исправляет конфигурацию, когда файлы текущей версии уже установлены. Сбрасывать клавиши или удалять сохранения не нужно.

## Удаление

Закрой игру и мод-менеджер. Из той же папки мода выполни:

```powershell
python scripts/manage.py uninstall --game-dir "D:\SteamLibrary\steamapps\common\Deadlock\game\citadel" --apply
```

Будут удалены пакеты этого мода. Остальные моды останутся на месте. Перезапусти игру, чтобы вернуть обычные иконки и эффекты предметов.

<details>
<summary>Установка вручную</summary>

Сохрани копию `game\citadel\gameinfo.gi`. Скопируй пять файлов из `packages` в `game\citadel\addons`, не заменяя чужие моды. В `gameinfo.gi`, внутри `FileSystem → SearchPaths`, размести `Game citadel/addons` выше `Game citadel`. В этом же блоке должны быть четыре строки:

```text
Mod   citadel
Write citadel
Mod   core
Write core
```

Сохрани существующие строки `Game citadel`, `Game core`, языковые и остальные настройки. Одной строки addons недостаточно: явные `Mod` и `Write` сохраняют доступ к стандартной конфигурации клавиш.

Для ручного удаления убери только `pak06_dir.vpk` — `pak10_dir.vpk` этого мода, сверив их с [SHA256SUMS.txt](SHA256SUMS.txt). Остальное содержимое `addons` сохрани.

</details>

## Совместимость

Мод подготовлен для версии игры от **17 октября 2026**. Обновления Deadlock могут нарушить его работу. Если после обновления появились проблемы, удали мод до выхода совместимой версии. Мод-менеджер также может заменить установленные вручную файлы при синхронизации.

Неофициальный фанатский мод с ресурсами Dota 2 и Deadlock от Valve. [Авторы и ресурсы](CREDITS.md).
