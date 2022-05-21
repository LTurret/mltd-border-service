# MLTD JP server event fetcher and border-image generator

English | [繁體中文](README.zh-TW.md)

A Python based Rank fetcher and border-image generator
  
## Usage

```console
$ ./AnnaBorder --help
usage: AnnaBorder.exe [-h] [-O] [-S] -T  [...] [--dryrun | --checksum]

Generator that fetches hosting event information and border datasets then generates border image.

options:
  -h, --help            show this help message and exit
  -O , --output_path    Image generate ouput path, default is "./image"
  -S , --search_id      Search specific event with unique ID
  -T  [ ...], --type  [ ...]
                        Select fetches border type
  --dryrun              Don't generate border-image and output folder to disk
  --checksum            Don't generate any file or folder, test API response
  --static              Don't fetch any thing from internet, test image generate with existing JSON file
```

## Option decription

`[-T [...]]` is border type, using `*args` format, provides PT-rank("pt"), HighScore("hs"), LoungePoint("lp")  
it can enter multiple border types, generates more than one border-image  

## Customization

.psd file in the `./components` folder makes everyone change border-background to their own style  

## Configuration

`config.json` is **event informations data**, **border data**, **fonts**, **background** file location, with customization, convenient the file organization

## Build

For program library:

```console
aiohttp
argparse
asyncio
PIL
```

For production library:

```console
pyinstaller
```

Build args example:

```console
pyinstaller -F "main.py" -i "icon.ico"
```

## License

Licensed under [MIT](LICENSE).

The copyright of any characters in the image(includes .psd, .png) belongs to [Bandai Namco Entertainment](https://www.bandainamcoent.co.jp/).  
All the event information is provided by [api.matsurihi.me](https://api.matsurihi.me/docs/)  
Font used in the image title is [ChiuKong Gothic](https://github.com/ChiuMing-Neko/ChiuKongGothic)  
Font used in the image body is [jf open 粉圓](https://github.com/justfont/open-huninn-font)  
