for f in "$@"; do python3 -c "import cairosvg,sys;cairosvg.svg2png(url=sys.argv[1],write_to=sys.argv[1][:-4]+'.png',output_width=1200)" $f 2>&1 | tail -1; done
