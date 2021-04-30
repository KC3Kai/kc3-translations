## 参与简体中文KC3改翻译须知

欢迎参与KC3改的简体中文翻译！希望在贡献翻译时尽量依据以下规则：

* 版面宽松的情况下尽量使用全角标点符号
* 装备中的括号使用半角
* 使用Tab缩进
* 以下情况可以直接push至repo：
    * 翻译缺失项目（包括将现存英文条目翻译中文）
    * 修正笔误 / 调整缩进
* 修改已有翻译超过三条请尽量发Pull Request 并 @ 其他scn翻译者 （目前主要活跃的翻译者为： @Javran @Diablohu ）
* 其他情况下自行判断

## 编辑中文字幕

请勿直接编辑 `quotes.json` 中以舰娘id为索引的数据。这一部分是不定期从[舰娘百科](http://zh.kcwiki.moe/wiki/%E8%88%B0%E5%A8%98%E7%99%BE%E7%A7%91)数据库中获取的，故对此部分的修订请通过编辑舰娘百科中相应条目的方法完成。

附中文字幕更新方法:

- 需要 [kantour](https://github.com/Javran/kantour)
- `kcwikizh-subtitle-merge.py` 与 `remodelGroups.json` 在`tools`目录下，以下不再说明。

```bash
# 获取台词并生成kcwiki.json
<dir to kantour>./stack build && stack exec -- quotesfetch
# 对于限定台词，需要额外参数，如
<dir to kantour>./stack build && stack exec -- quotesfetch 季节性/2017年女儿节
# 完整列表见 https://zh.kcwiki.moe/wiki/%E5%AD%A3%E8%8A%82%E6%80%A7
./kcwikizh-subtitle-merge.py kcwiki.json ../data/scn/quotes.json quotes2.json
# 删除冗余台词
./quotes-minify.py remodelGroups.json quotes2.json ../data/scn/quotes.json
# overwrite old file
# cleanup
rm kcwiki.json quotes2.json
```

## 声明

* 部分翻译来自 [@Diablohu](http://diablohu.com)
* 部分翻译（任务翻译以及中文简体字幕）来自 [舰娘百科](http://zh.kcwiki.moe)，有少许修改。
* 部分台词翻译参考自[萌娘百科](https://zh.moegirl.org)
    - NPC 台词参照来源： [舰队Collection:明石](https://zh.moegirl.org/%E8%88%B0%E9%98%9FCollection:%E6%98%8E%E7%9F%B3) [舰队Collection:大淀](https://zh.moegirl.org/%E8%88%B0%E9%98%9FCollection:%E5%A4%A7%E6%B7%80)
