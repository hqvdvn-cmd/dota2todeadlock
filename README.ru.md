[English](README.md) · **Русский**

# Dota 2 → Deadlock

[![GameBanana](assets/badge-gamebanana.svg)](https://gamebanana.com/mods/729017)
[![Deadlock Mod Manager](assets/badge-mod-manager.svg)](https://gamebanana.com/mods/729017#Files)

Иконки и эффекты Dota 2 для Deadlock. Соответствия выбраны по действию предметов: вампиризм, снижение брони, барьеры и другие механики. У составных предметов несколько Dota-иконок, у улучшений — золотые и красные варианты.

Из эффектов уже перенесены Counterspell, Refresher, Shiva’s Guard для Cold Front, Arctic Blast/Frostbite и барьеры Pavise. Появление, попадания и разрушение барьеров изменены также у способностей героев. Дальше планируется перенос других Dota-эффектов.

В V18 заменены 154 определения предметов, ещё 19 сохраняют родные иконки. В [таблице](docs/ITEMS.md) есть улучшения и режимные варианты. Скины героев и озвучка в комплект не входят.

## Скачать

[Архив V18](https://github.com/hqvdvn-cmd/dota2todeadlock/releases/tag/v18) · [ZIP полного репозитория](https://github.com/hqvdvn-cmd/dota2todeadlock/archive/refs/heads/main.zip) · [GameBanana](https://gamebanana.com/mods/729017#Files)

V18 доступна на GitHub. Обновление файла на GameBanana пока не опубликовано.

В разделе файлов GameBanana есть установка через **Deadlock Mod Manager**, **Grimoire Mod Manager** и **HELLCAT**. Отключи старую версию, установи новый архив и включи все пять компонентов.

## Установка вручную

1. Закрой Deadlock и менеджер. Сохрани копию `game/citadel/gameinfo.gi` и файлов предыдущей версии мода.
2. В Steam открой Deadlock → Свойства → Установленные файлы → Обзор, затем перейди в `game/citadel`.
3. Скопируй пять VPK в `game/citadel/addons`. В ZIP полного репозитория они лежат в `packages`, в архиве релиза V18 — в корне. Чужие моды не перезаписывай.
4. В `gameinfo.gi` найди `FileSystem` → `SearchPaths`. Поставь `Game citadel/addons` выше `Game citadel`. Сохрани остальные игровые и языковые пути и проверь наличие строк:

```text
Game  citadel/addons
Mod   citadel
Write citadel
Mod   core
Write core
```

При обновлении сначала убери файлы предыдущей версии этого пака. Для удаления убери только его пять VPK, сверив их с [SHA256SUMS.txt](SHA256SUMS.txt). Остальное содержимое `addons` сохрани.

### Необязательный Python-установщик

В GitHub ZIP есть скрипт, который проверяет штатный файл способностей и сохраняет копию конфигурации перед правкой. Нужен Python 3.10+. Замени путь к игре на свой:

```powershell
python scripts/manage.py install --game-dir "D:/SteamLibrary/steamapps/common/Deadlock/game/citadel" --enable-addons --apply
python scripts/manage.py launch --game-dir "D:/SteamLibrary/steamapps/common/Deadlock/game/citadel" --apply
```

Для удаления замени `install` на `uninstall` и убери `--enable-addons`. Выполняй из той же распакованной папки. Сохрани `.local/backups`.

## Демонстрация

![Иконки V18](assets/demo/icons-v18.png)

Видео и игровые скриншоты ниже сняты на более ранней версии. Скин героя с них в комплект не входит.

[Ролик — 27 секунд](assets/demo/showcase.mp4)

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

## Совместимость

База — игровые ресурсы от 21 октября. Патч Deadlock может сломать замену ресурсов или сбросить загрузку модов. Python-установщик проверяет штатный файл способностей; менеджеры и ручное копирование эту проверку не запускают. У новой ревизии иконок проверены файлы и пиксели; игровое подтверждение ещё нужно.

Для [Шуры](https://github.com/hqvdvn-cmd/sekiro-shura-deadlock) используй её D2D-патч привязки ульты. Две полные замены файла способностей требуют совместимой сборки.

Если найдёшь баг, напиши предмет/эффект, сборку игры и другие установленные моды. Приложи скриншот или короткий ролик.

Оригинальные ресурсы: Valve. [Авторы](CREDITS.md).
