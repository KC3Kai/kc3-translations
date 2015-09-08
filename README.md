## KC3改 Translations

![KC3改 Logo](http://puu.sh/h4Gbb.png)

If interested, you can translate KC3改 to your own language.

## Procedure
#### With GitHub
* Fork KC3改 repository
* Clone your repo to your local computer (Article [[Setup development build]] may help)
* Make sure <code style="background:#eee;">dragonjet/KC3Kai</code> is also added as secondary remote
* Find the directory <code style="background:#eee;">\src\data\translations</code>
* Inside, you can see an <code style="background:#eee;">en</code> folder, copy it into a new language
* Go inside your new language folder, and edit the <code style="background:#eee;">json</code> files
* Commit your new language files, and push to your own GitHub repo
* Create a pull request to <code style="background:#eee;">dragonjet/KC3Kai</code>

#### Without GitHub (manual)
* Download the ZIP file from the [project home](https://github.com/dragonjet/KC3Kai)
* Extract the ZIP on your local computer
* Find the directory `\src\data\translations`
* Inside, you can see an `en` folder, copy it into a new language
* Go inside your new language folder, and edit the `json` files
* [Create an issue on the main repo](https://github.com/dragonjet/KC3Kai/issues/new), add a label "translation"
   * You can name the subject as: "*\[Translation: (lang_code)\] (what_was_translated)*"
   * For example: "*[Translation: JP] Settings Page*"
* Paste the translation files / links to its pastebin or puush or any preferred text transmission tool.

## Translation forks
* The only required file is `terms.json`. If there are missing files from your translation directory, it will extend the English translations by default.
* You do not need `developers.json` and `settings.json` on your localized directory anymore. The translatable words on those files are now moved into `terms.json`.
* `terms.json` is still an evolving file which will get updated very often, it is up to you to translate this every time or just wait for it to settle down and translate in one go.

#### Special Case for JP
Since game data is already in Japanese, some files do not need to be translated:
* `ships.json`
* `items.json`

However, they still need to have their own files, but just contains an empty JSON object `{}`.

#### Quests.json
##### Kanji ship names in quest descriptions
For quest descriptions like

`Have Tenryuu (\u5929\u9f8d) and Tatsuta (\u9f8d\u7530) in your main fleet.`

It is your choice if you want to still include kanji representations like `(\u5929\u9f8d)` in your own language

## Release / Publishing

#### Why shouldn't I make my own localized releases?
Making your own releases mean creating your own WebStore entry, which means we'll have multiple KC3改s in the WebStore, which is not good not because of competition, but for reasons indicated at the bottom of this section.

If you really really want your own release, you may only do so if
* It's not from the Chrome WebStore, and is only downloadable zip on your fork's releases section.
* Change the name in the `manifest.json` to add the language, for example: **KanColle Command Center 改 (Tagalog)** or **KC3改 (Tagalog)**, or **.....(PH)**.
* Retain the list of people in the credits list, but you may add yourself with the description *Translator (lang_code)*, for example **Translator (PH)** or a description in your local language, e.g. **Tagasalin (PH)**

The main reason why separate releases are not recommended since we cannot monitor the codes you use. Please do not make code changes that may put the player at risk. **We don't want a localized KC3改 release being tagged as something detectable and bannable, which will disgrace the KC3改 name**.

Here at KC3改, we uphold safety principles and will never risk our players.