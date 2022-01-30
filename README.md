# MLTD JP server event fetcher and border-image generator

English | [繁體中文](README.zh-TW.md)

A Python based Rank fetcher and border-image generator
  
## Usage

```console
$ python main.py --help
usage: main.py [-h] [-O] [-S] [-T  [...]] [--dryrun | --checksum]

Generator that fetches hosting event information and border datasets then generates border image.

options:
  -h, --help            show this help message and exit
  -O , --output_path    Image generate ouput path, default is "./img-output"
  -S , --search_id      Search specific event with unique ID
  -T  [ ...], --type  [ ...]
                        Select fetches border type
  --dryrun              Don't generate border-image and output folder to disk
  --checksum            Don't generate any file or folder, test API response
```

## Option decription

`[-T [...]]` is border type, provides PT-rank("pt"), HighScore("hs"), LoungePoint("lp")  
it provide enter multiple border type, it can generate more than one type of border-image  

## License

Licensed under [MIT](LICENSE).

All the event information is provided by [api.matsurihi.me](https://api.matsurihi.me/docs/)  
The copyright of character in the image(includes .psd, .png) belongs to Bandai Namco Entertainment.  
Font in the image title is [ChiuKong Gothic](https://github.com/ChiuMing-Neko/ChiuKongGothic)  
Font in the image body is [jf open 粉圓](https://github.com/justfont/open-huninn-font)  
