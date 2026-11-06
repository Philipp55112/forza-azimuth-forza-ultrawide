FM6 tools (how the FM6 data in Forza21x9_ops.json was made)
============================================================
xmem.py        LZX / XMemCompress decoder for Forza zip method 21 (FM6 UI.zip), verified on all 301 entries
zp.py          Forza zip reader (central directory, extra field 0x1123 = absolute data offset)
rootscan.py    lists the direct children of every scene's LayoutRoot
rules_v2.py    base rules (FullSceneWidth key, body grids centred +S, backgrounds full width, dialogs, HUD corners +90)
rules_v3.py    header + footer full 21:9 width, tab menus full width, 16:9 loading spinners inside the 16:9 area
rules_v6.py    pages declared 1920 wide -> full width (the game indents them by S otherwise), My Cars / player car pictures
               ScaleX = W/1920, Autovista panels left original
edges.py       elements that touch the left/right screen edge in 16:9 are moved to the 21:9 edge
build_v2.py    writes UI.zip (changed entries stored, method 0) + ZipManifest.xml for testing on the PC
fm6_templ.py   turns the finished 2580-wide files into width templates (@W@, @S@, @K@, @E:a:op:dec[:f]@) for the installer
edit_zip.py    small entry edits for the deflate zips of FH2 / F&F / FM5 (black-bar tests)

The scripts were run in this order on the decoded original files: v2 -> v3 -> (F040 / F000 fixes) -> v6 -> edges ->
manual fixes (F110 fillers, F908 end-of-race, F931 rewards 985/1595, F041 logo) -> fm6_templ.py.
A few fixes (player-car ScaleX in F213/F300/F311/F582/F676/F883, full-width gradients in F041/F042/F043/F062/F070/F312/F875)
came from a parallel session and were merged as files. Paths inside the scripts point to the working folders used then.
