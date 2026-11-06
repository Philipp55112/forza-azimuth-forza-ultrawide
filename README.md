# Forza 21:9 Ultrawide Patch

**True 21:9 ultrawide UI support for Xbox One Forza games running on PC through Azimuth.**

The Forza 21:9 Ultrawide Patch adapts the games' user interfaces for ultrawide displays, repositioning HUD elements, adjusting menu layouts, and correcting aspect ratios to provide a more natural experience on 21:9 monitors.

The patch currently supports **Forza Horizon 2**, **Forza Horizon 2 Presents Fast & Furious**, **Forza Motorsport 5**, and **Forza Motorsport 6**.

Compatible with **Azimuth 1.0.2, 1.0.3 and 1.0.4**.

See [CHANGELOG.md](CHANGELOG.md) for the complete version history.

---

## Supported Games

| Game | Version | Status |
| --- | --- | --- |
| **Forza Horizon 2** | `1.0.0.64` | Supported |
| **Forza Horizon 2 Presents Fast & Furious** | `1.0.0.6` | Supported |
| **Forza Motorsport 5** | `1.0.0.20` | Supported |
| **Forza Motorsport 6** | `1.0.0.44` | Supported |
| Forza Horizon 3 | — | Planned |

## Features

- **True ultrawide UI:** Adapts HUD elements and supported interface layouts for ultrawide displays.
- **Resolution-aware layouts:** Calculates the appropriate UI dimensions for the selected display resolution.
- **Improved menu layouts:** Keeps supported menu content properly positioned while extending backgrounds and interface elements across the screen.
- **Aspect ratio corrections:** Prevents vehicle images and other UI elements from appearing stretched or squeezed.
- **Full frame rate:** Prevents supported menus and screens from unnecessarily halving the configured frame rate.
- **Per-game configuration:** Enables or disables the patch individually for each supported title.
- **Optional desktop shortcuts:** Launches individual games directly without opening the Azimuth launcher.
- **Automatic backups:** Verifies original files using SHA-256 and backs them up before modifications.
- **Safe restoration:** Includes an uninstaller to restore the original files.

## What's New in v1.3.0

### Forza Motorsport 6 support

Version 1.3.0 introduces full ultrawide UI support for **Forza Motorsport 6 (1.0.0.44)**.

The new FM6 implementation includes:

- **Ultrawide menus:** Menu headers and controller button bars extend across the full screen, while menu content remains properly centred.
- **HUD positioning:** HUD elements are repositioned towards the edges of the ultrawide display.
- **Adapted interface screens:** Loading screens, dialogs, tutorials and message boxes receive ultrawide adjustments.
- **Post-race rewards:** The rewards panel is repositioned towards the screen edge.
- **Vehicle image corrections:** Fixes squeezed vehicle images in My Cars, next race screens, Free Play, multiplayer lobbies and profiles.
- **16:9 screen handling:** Screens that remain in their original aspect ratio receive clean black side bars.
- **Full frame rate in menus:** Prevents FM6 from halving the configured frame rate in menus. For example, 90 FPS instead of 45 FPS.
- **Restored start screen:** Fixes the missing "Press A" prompt by ensuring the game waits until the intro video has finished.
- **Correct intro audio timing:** Menu music starts after the logos and intro video have finished. When the intro is disabled in the game options, the music starts immediately as usual.

### Improvements for existing games

**Forza Horizon 2 & Fast & Furious**
- Loading and fast-travel backgrounds now fill the entire screen again.
- The additional black side bars previously added by the patch have been removed, as Azimuth 1.0.4 now handles these backgrounds correctly.

**Forza Motorsport 5**
- The loading indicator on the 16:9 start screen now stays within the original 16:9 area.
- Existing vehicle image aspect-ratio corrections remain in place where the game still displays images too narrowly.

**Installer**
- Added Forza Motorsport 6 to the supported game selection.
- Added a dedicated FM6 desktop shortcut with its own game icon.
- Improved compatibility with previous versions of the patch's `dinput8.dll`, making updates from earlier releases easier.

---

## Game-specific Features

| Game | Ultrawide adjustments |
| --- | --- |
| **Forza Horizon 2** | HUD positioned at 21:9 screen edges, centred menus, full-width menu elements and adapted loading backgrounds |
| **FH2 Presents Fast & Furious** | Same ultrawide UI adjustments as FH2 |
| **Forza Motorsport 5** | Ultrawide menus, races and HUD, corrected vehicle images, full frame rate in garage and pre-race screens |
| **Forza Motorsport 6** | Full-width menu headers, edge-positioned HUD, adapted dialogs and loading screens, corrected vehicle images, full menu frame rate and improved intro handling |

Some pre-rendered videos, intro sequences and selected loading screens remain in their original 16:9 format.

## Requirements

- Windows PC
- Compatible installation of a supported Forza game
- Azimuth **1.0.2, 1.0.3 or 1.0.4**
- Ultrawide display for the intended 21:9 experience
- Sufficient free disk space for backups and modified UI files

## Installation

Two installation packages are available in the [Releases](https://github.com/Philipp55112/fh2-ultrawide-ui/releases) section.

### Option 1: Standalone EXE installer

Download and run:

`Forza21x9_Setup_v1.3.0.exe`

The installer allows you to:

- Select your Azimuth installation folder.
- Select your target display resolution.
- Enable or disable the patch individually for each supported game.
- Create optional desktop shortcuts for configured games.
- Install or update the patch.
- Uninstall the patch and restore original files.

The installer verifies the expected original files using SHA-256 and creates backups before applying modifications.

### Option 2: Classic ZIP package

Download:

`Forza21x9_Ultrawide_v1.3.0.zip`

The classic package contains the English batch installer and uninstaller, along with the required scripts and supporting files.

1. Extract the ZIP package.
2. Run `Install.bat`.
3. Select your Azimuth installation folder using the folder picker.
4. Select your target resolution.
5. Choose which games should receive the patch.
6. Follow the instructions displayed by the installer.

To remove the patch, run `Uninstall.bat`.

The installer preserves backups so that the original files can be restored. Keep the backup folder until you have verified that the original installation has been restored successfully.

### Source Code

The source code is also available:

`Forza21x9_Source_v1.3.0.zip`

---

## Optional Desktop Shortcuts

The installer can create individual desktop shortcuts for each configured game, using the corresponding game logo as its icon.

These shortcuts launch the selected game directly without opening the Azimuth launcher.

The shortcuts use Azimuth's game selection and launcher-skipping arguments.

Examples:

- Forza Horizon 2: `azimuth.exe --game=fh2 --skip-launcher`
- Forza Horizon 2 Presents Fast & Furious: `azimuth.exe --game=fh2-ff --skip-launcher`
- Forza Motorsport 5: `azimuth.exe --game=fm5 --skip-launcher`
- Forza Motorsport 6: `azimuth.exe --game=fm6 --skip-launcher`

The shortcuts are optional and are removed by the uninstaller.

---

## Configuration

The patch uses `azimuth_21x9.ini` for additional settings.

### Per-game configuration

The installer allows you to enable or disable the patch for each supported title individually.

Disabled games retain their original UI files.

### Optional FM5 and FM6 features

Some additional corrections can be disabled individually through the configuration file.

```ini
[fm5]
full_rate=0

[fm6]
full_rate=0
start_screen=0
quiet_intro=0
```

| Setting | Description |
| --- | --- |
| `[fm5] full_rate` | Disables the full-frame-rate correction in FM5 |
| `[fm6] full_rate` | Disables the full-frame-rate correction in FM6 menus |
| `[fm6] start_screen` | Disables the FM6 start screen correction |
| `[fm6] quiet_intro` | Disables the adjusted FM6 intro music timing |

Set an option to `0` to disable the corresponding correction. The default configuration supplied with the installed version determines which features are enabled.

Use the configuration file and section names supplied with your installed version.

---

## How It Works

### In-memory Azimuth patching

The patch leaves `azimuth.exe` unchanged.

A `dinput8.dll` proxy is placed alongside `azimuth.exe`. Since Azimuth imports `DINPUT8.dll`, the proxy can load automatically, forward `DirectInput8Create` to the original Windows system DLL, and apply the necessary modifications in memory.

The patch identifies the active game and enables the appropriate modifications for that title.

This approach avoids directly modifying the Azimuth executable and preserves compatibility with FH2 Extra Options.

### UI layout modifications

The patch modifies the games' XAML-based UI layouts inside:

`Mount\media\UI.zip`

Modified archives are rebuilt from the original UI files using predefined operations that verify expected original data before replacing it.

Forza uses a custom ZIP structure with an additional central-directory field (`0x1123`) containing absolute data offsets. The patch preserves this structure and updates the relevant `zipmanifest.xml` directory information.

The patch does not include any original game files or Azimuth files.

### Runtime corrections

In addition to UI archive modifications, certain fixes are applied at runtime through the `dinput8.dll` proxy.

These include frame-rate corrections, menu behavior adjustments, intro handling and other game-specific fixes.

The runtime modifications are only activated for the corresponding game when its patch is enabled.

---

## Backups and Uninstallation

The installer backs up original files to:

`<Azimuth folder>\Forza21x9_backup\`

Original files are verified using SHA-256 before modifications are applied.

The backup contains the files required to restore the original installation.

Use the included uninstaller to remove the patch and restore the backed-up files. The uninstaller also removes the optional desktop shortcuts created by the installer.

Do not delete the backup folder until you have confirmed that the original installation has been restored successfully.

The patch should be configured separately for each Azimuth installation you use.

---

## Known Issues and Limitations

### Resolution testing

- **3440×1440 (21:9)** is the primary development and tested resolution.
- Other ultrawide resolutions are calculated during installation but have not all been tested.
- 2560×1080 and 3840×1600 are supported by the layout calculations.
- 32:9 is theoretically supported but has not been confirmed through testing.

### Original 16:9 content

Some pre-rendered videos, intro sequences and selected loading screens remain in their original 16:9 format.

### General

- Compatibility depends on the supported game version and Azimuth installation.
- Modified UI archives must preserve the game's custom ZIP structure. Repacking them with ordinary ZIP tools may break the game.
- Always keep your original backups before making manual changes.

---

## Roadmap

The project will continue expanding to cover more Forza titles.

**Planned:**
- Forza Horizon 3 support.
- Further resolution compatibility testing.
- Additional game-specific UI improvements.
- More compatibility testing and refinements.

---

## Credits

- **Azimuth Project** — For making it possible to run these Xbox One Forza games on PC.
- **Claude (Anthropic)** — Assistance with research, development and implementation.
- **The community** — For feedback, testing, suggestions and continued interest in preserving these games.

---

## Disclaimer

This is an unofficial community project. It is not affiliated with or endorsed by Microsoft, Xbox, Playground Games or Turn 10 Studios.

Use the patch at your own risk. Always keep backups of your original files.

---

## Project and Downloads

**GitHub Repository:**  
https://github.com/Philipp55112/fh2-ultrawide-ui

**Latest Release:**  
https://github.com/Philipp55112/fh2-ultrawide-ui/releases/latest

See [CHANGELOG.md](CHANGELOG.md) for the complete version history.
