## KC3改 Translations [![Build Status](https://travis-ci.org/KC3Kai/kc3-translations.svg?branch=master)](https://travis-ci.org/KC3Kai/kc3-translations)

![KC3改 Logo](http://puu.sh/h4Gbb.png)

If interested, you can translate KC3改 to your own language.

## Procedure
#### With GitHub (fork)
* Fork `KC3Kai/kc3-translations` repository
* Clone your repo to your local computer
* Make sure `KC3Kai/kc3-translations` is also added as secondary remote
* Go to the `data` directory where you can see language folders, copy one into a new language
* Go inside your new language folder, and edit the `json` files
* Commit your new language files, and push to your own GitHub repo
* Create a pull request to `KC3Kai/kc3-translations`

**Promotion to direct write-access**

You will first need your own translation fork (as indicated above), and has created a pull-request for the initial translation files for your language. If the language already has a directory, and you want to help existing translators, you will still need a fork, and a pull-request just to see a sample of your work before we can add you on the direct-write access team.

Once these requirements are fulfilled, you may request for promotion:
* Create a new issue on the [main `KC3Kai` repo](https://github.com/KC3Kai/KC3Kai/issues)
* Add `others` and `translation` as label
* Subject/Title: **Request translation repo access**

Then wait until reply, and an invitation to the KC3Kai organization, under the *Translation* team.


#### Without GitHub (manual)
* Download the ZIP file from the [project home](https://github.com/KC3Kai/kc3-translations)
* Extract the ZIP on your local computer
* Find the directory `\src\data\translations`
* Inside, you can see an `en` folder, copy it into a new language
* Go inside your new language folder, and edit the `json` files
* [Create an issue on the main repo](https://github.com/dragonjet/KC3Kai/issues/new), add a label "translation"
   * You can name the subject as: "*\[Translation: (lang_code)\] (what_was_translated)*"
   * For example: "*[Translation: JP] Settings Page*"
* Paste the translation files / links to its pastebin or puush or any preferred text transmission tool.

## Notes
The only required file is `terms.json`. If there are missing files from your translation directory, it will extend the English translations by default.
If there are missing keys in your translated JSON file, it will also extend the English ones by default.

By enabling the setting `Dev-Only Strategy Pages`, you can check the missing keys in your selected language via Strategy Room Dev-Only Translations page.

#### About `quests.json`
There are some keys used as meta attributes of quests, such as `code`, `unlock` and `tracking`.
They are not needed to be translated, and can be just omitted in the `quests.json` of your own language, as long as you do not intend to use different values from English's.

By the way, the values of `code` in English file are from the quest identifier system defined by [wikiwiki.jp/kancolle](https://wikiwiki.jp/kancolle/%E4%BB%BB%E5%8B%99), which also used by other English wikis.

#### About `en/ctype.json`
These Japanese ship class names are basically extracted from in-game ship library banner image. They are supposed to be automatically translated using the same mechanism of ship name translation. So just define your translations in your `ships.json` and `ship_affix.json`, and keep the `ctype.json` being empty (only containing `[]`) in your directory.

#### About `servers.json`
Similar with the `quests.json`, there are keys used as meta data which are not needed to be translated.
The only key required to be translated is `name`, omitting other keys in your language is fine.

To update the IP address of servers, suggested to execute the script in `tools` folder, instead of manual modification.

#### About `quotes.json`
It's a bit complicated about our subtitle mechanism, you might need to learn more from our source code, before another detailed document is ready.

#### Special case for JP
Since game data is already in Japanese, `ships.json` and `items.json` do not need to be translated, but will still need to have the files exist, just containing an empty JSON object `{}`. For more information, please read [this](data/jp/README.md).

#### Kanji or Unicode character in your JSON
Generally JSON files are recommended to be saved in Unicode `UTF-8` charset.

For Kanji or any non-ascii Unicode character, such as quest descriptions like

`Have Tenryuu (\u5929\u9f8d) and Tatsuta (\u9f8d\u7530) in your main fleet.`

It is your choice if you want to still include Kanji representations like `(\u5929\u9f8d)` in your own language.

But do remember to use escaped chars like `\uHHHH` instead of literal Kanji or non-ascii chars, if you are not sure how to save your JSON file in `UTF-8` charset.

## Notes & Rules for Specific Languages

For several languages, there are extra notes and rules:

* [Simplified Chinese (scn)](data/scn/README.md)
* [Traditional Chinese (tcn)](data/tcn/readme.md)
* [Japanese (jp)](data/jp/README.md)

Make sure to read them before contribution.
