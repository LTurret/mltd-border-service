# MLTD日服榜線抓取以及圖片產生器

[English](README.md) | 繁體中文

基於Python開發的排行抓取以及圖片產生器
  
## 使用方法

```console
$ python main.py --help
usage: main.py [-h] [-O] [-S] [-T  [...]] [--dryrun | --checksum]

可以抓取當前活動資訊以及輸出排行圖片的產生器

options:
  -O , --output_path    圖片輸出路徑，預設為 "./image"
  -S , --search_id      使用獨立ID搜尋特定的活動
  -T  [ ...], --type  [ ...]
                        選擇欲抓取的活動類型
  --dryrun              不輸出排行圖片或輸出資料夾
  --checksum            不輸出任何檔案或資料夾，測試API
```

## 選項說明

`[-T [...]]` 是排行類型，提供了提供了PT榜("pt")、高分榜("hs")、廳榜("lp")  
可以同時輸入多種排行類型，輸出不只一張排行圖片  

## 授權

遵守 [MIT](LICENSE)授權條款。

所有的活動資訊皆由[api.matsurihi.me](https://api.matsurihi.me/docs/)提供  
出現在影像中的任何角色(包括.psd、.png)版權皆屬於萬代南夢宮娛樂所有  
字體使用於圖片標題為[秋空黑體](https://github.com/ChiuMing-Neko/ChiuKongGothic)  
字體使用於圖片內容為[jf open 粉圓](https://github.com/justfont/open-huninn-font)  
