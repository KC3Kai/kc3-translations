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

#### Special Case for JP
Since game data is already in Japanese, `ships.json` and `items.json` do not need to be translated, but will still need to have the files exist, just containing an empty JSON object `{}`.

#### Kanji ship names in quest descriptions
For quest descriptions like

`Have Tenryuu (\u5929\u9f8d) and Tatsuta (\u9f8d\u7530) in your main fleet.`

It is your choice if you want to still include kanji representations like `(\u5929\u9f8d)` in your own language

~~sample~~

## Notes & Rules for Specific Languages

For several languages, there are extra notes and rules:

* [Simplified Chinese (scn)](data/scn/README.md)
* [Traditional Chinese (tcn)](data/tcn/readme.md)
* [Japanese (jp)](data/jp/README.md)

Make sure to read them before contribution.
