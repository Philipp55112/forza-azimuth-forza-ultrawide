# Changelog

All notable changes to the Forza 21:9 Ultrawide Patch are documented here.

## [1.3.0] - Forza Motorsport 6 Support

### Added

- **Forza Motorsport 6 support (1.0.0.44):** Added full 21:9 ultrawide UI support for Forza Motorsport 6.
- **Ultrawide menus:** Menu headers and controller button bars now span the full screen width, while menu content remains centred with full-width backgrounds.
- **HUD positioning:** HUD elements are repositioned towards the edges of ultrawide displays.
- **Adapted interface screens:** Loading screens, dialogs, tutorials and message boxes receive ultrawide adjustments.
- **Post-race rewards:** The rewards panel is repositioned towards the screen edge.
- **Vehicle image corrections:** Corrected squeezed vehicle images in My Cars, next race screens, Free Play, multiplayer lobbies and profiles.
- **16:9 screen handling:** Screens that remain in their original aspect ratio receive clean black side bars.
- **Full frame rate in menus:** Prevents FM6 from unnecessarily halving the configured frame rate in menus (e.g. 90 FPS instead of 45 FPS).
- **Restored start screen:** Fixed the missing "Press A" prompt by making FM6 wait until the intro video has finished playing.
- **Improved intro audio timing:** Menu music now starts after the logos and intro video have finished. When the intro is disabled in the game options, music starts immediately as usual.
- **FM6 desktop shortcut:** Added a dedicated desktop shortcut with the corresponding game logo.

### Changed

- **Azimuth 1.0.4 compatibility:** Added support for Azimuth 1.0.4 while retaining compatibility with Azimuth 1.0.2 and 1.0.3.
- **Installer:** Added Forza Motorsport 6 to the game selection and configuration options.
- **Patch updates:** Improved compatibility with previously installed versions of the patch's `dinput8.dll`, making updates from earlier releases easier.
- **FH2 and Fast & Furious loading backgrounds:** Loading and fast-travel backgrounds now fill the entire screen again. The additional black side bars previously added by the patch have been removed because Azimuth 1.0.4 now handles these backgrounds correctly.

### Fixed

- **Forza Motorsport 5 start screen:** The loading indicator on the original 16:9 start screen now stays within the 16:9 area.
- **Forza Motorsport 5 vehicle images:** Existing aspect-ratio corrections remain active in locations where the game still displays vehicle images too narrowly. Corrections are no longer applied to locations where Azimuth already displays them correctly.

---

## [1.2.1] - Forza Motorsport 5 Vehicle Image Fixes

### Fixed

- Fixed horizontally stretched vehicle images in the Car Dealer, My Cars, Marketplace and livery selection popup.
- Removed unnecessary width corrections in these locations because Azimuth 1.0 already displays the images with the correct aspect ratio.
- Retained width corrections in Free Play, multiplayer lobbies, player cards, lobby garage popups, Hopper selection and profiles, where vehicle images were still appearing too narrow.

No other changes compared to v1.2.0.

---

## [1.2.0] - Resolution-aware Forza Motorsport 5 UI

### Added

- Added support for Azimuth 1.0.3 while retaining compatibility with Azimuth 1.0.2.
- FM5 UI layouts are now calculated during installation for the selected display resolution instead of being fixed to 3440×1440.
- Added optional desktop shortcuts for configured games, allowing them to launch directly without opening the Azimuth launcher.
- Added English batch installers (`Install.bat` and `Uninstall.bat`) to the classic ZIP package.
- Added a folder picker for selecting the Azimuth installation directory.

### Changed

- FM5 garage and pre-race screens now run at the full configured frame rate instead of halving it.
- FM5 animated main menu header lines now extend to the right edge, with the dot pattern matching the original UI layout.
- Improved installation and per-game configuration handling.

### Improved

- Resolution-aware UI calculations now cover resolutions such as 2560×1080, 3440×1440 and 3840×1600.
- Added the option to disable the FM5 full-frame-rate correction through `azimuth_21x9.ini`.

---

## [1.1.0] - Forza Motorsport 5 Support

### Added

- Added support for Forza Motorsport 5 (1.0.0.20).
- Added per-game patch enable/disable functionality.
- Added support for Azimuth 1.0.2 and 1.0.3.
- Added a standalone EXE installer alongside the classic ZIP package.

### Improved

- Introduced runtime patching through a `dinput8.dll` proxy without modifying `azimuth.exe`.
- Improved UI scaling, aspect-ratio handling and clipping corrections.
- Improved FM5 UI layouts for ultrawide displays.

---

## [1.0.1] - Fast & Furious UI Fix

### Fixed

- Fixed the vehicle confirmation screen layout in Forza Horizon 2 Presents Fast & Furious after selecting a car.
- Repositioned manufacturer branding and vehicle statistics to improve alignment.

No changes to the Forza Horizon 2 patch or installer/uninstaller.

---

## [1.0.0] - Initial Release

### Added

- Initial 21:9 ultrawide UI support for Forza Horizon 2 (1.0.0.64).
- Initial 21:9 ultrawide UI support for Forza Horizon 2 Presents Fast & Furious (1.0.0.6).
- Repositioned HUD elements for ultrawide displays.
- Improved UI layouts while keeping supported menus and dialogs centred.
- Added black side bars for selected 16:9 loading content.
- Added an installer with file verification and automatic backups.
- Added an uninstaller to restore original files.
- Added optional compatibility adjustments for FH2 Extra Options 0.2.98.

### Compatibility

- Tested with Azimuth 0.9.10.
