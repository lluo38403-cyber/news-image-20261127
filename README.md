# news-image-20261127

make.fun entry: sum up Friday 27 November 2026's world news in one image.

## The image

`entry.png` (1024×1024, PNG) is a one-page newspaper front page drawn by
`draw_news_image.py` (Pillow, deterministic, no network). Six stories,
all reported on 27 November 2026:

1. Explosions hit three tankers in the Strait of Hormuz (Middle East)
2. Russian strikes kill 5 in Ukraine and knock out power (Europe)
3. Thanksgiving storm cuts power to 724,000 on the US East Coast (US)
4. UK net migration falls to 77,000, a near 30-year low (UK)
5. Kim Jong Un orders North Korea's nuclear programme expanded (Asia)
6. All hostages freed after a 16-hour supermarket siege in Colombia (Latin America)

## How it runs

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`), so both
graded runs write identical bytes.

Regenerate the image with:

```sh
python3 draw_news_image.py
```

## License

MIT — see `LICENSE`.
