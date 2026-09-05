# Windows 12 UI Transformation - Installation Guide

## Version: 2.0.0 - Next Valley Edition

This guide provides step-by-step instructions for transforming your Windows 11 25H2 system into a complete Windows 12 UI experience.

## Prerequisites

- **Windows 11 25H2 or later** (Build 26100+ recommended)
- **Administrator privileges**
- **Internet connection** for downloading components
- **Minimum 8GB RAM** and **50GB free disk space**

## Installation Steps

### Step 1: System Preparation

1. **Backup your system** - Create a full system backup before proceeding
2. **Run as Administrator** - Right-click install.bat and select "Run as Administrator"
3. **Check system requirements** - The installer will verify your system meets the requirements

### Step 2: Core Components Installation

The installer will automatically download and install the following core components:

1. **Windhawk Customization Engine** - Enables floating taskbar and UI modifications
2. **ExplorerPatcher Next Valley** - Modified explorer with Windows 12 features
3. **Registry Tweaks** - System-wide UI modifications for Windows 12 look

### Step 3: Visual Effects Configuration

1. **ExplorerBlurMica Enhanced** - Advanced blur and mica effects
2. **DWMBlurGlass Enhanced** - Custom window effects and rounded corners
3. **TranslucentTB Enhanced** - Transparent floating taskbar
4. **MicaForEveryone Enhanced** - Extended mica effects for all applications

### Step 4: AI Integration Setup

1. **PowerToys Copilot Edition** - AI-powered productivity tools
2. **Windows Copilot 2.0** - Microsoft's AI assistant with Windows 12 integration

### Step 5: Theme Application

1. **Windows 12 Theme** - Complete visual theme with floating taskbar support
2. **Windows 12 Icons** - Matching icon set for the new UI

### Step 6: Widgets and Notifications

1. **Rainmeter Widget Engine** - Custom widgets for top-mounted display
2. **Floating Taskbar Mod** - Windhawk mod for floating taskbar
3. **Top Widgets Mod** - Windhawk mod for top-mounted widgets

### Step 7: Hybrid Optimization

1. **MacType Enhanced** - Improved font rendering for Windows 12
2. **Windows 12 MacType Profile** - Optimized font rendering settings

## Post-Installation Configuration

### Taskbar Configuration

Edit `config/Windows12/taskbar_config.json` to customize:
- Floating behavior and position
- Transparency level
- Rounded corners radius
- Icon size and spacing
- Auto-hide settings

### Widgets Configuration

Edit `config/Windows12/widgets_config.json` to customize:
- Top widgets visibility
- Widget positions (left, center, right)
- Auto-hide behavior
- Transparency settings

### AI Integration Configuration

Edit `config/Windows12/ai_config.json` to customize:
- Copilot 2.0 features
- AI-powered suggestions
- Integration points
- Voice control settings

### Design Configuration

Edit `config/Windows12/design_config.json` to customize:
- Fluent Design 3.0 settings
- Rounded corners radius
- Mica and acrylic effects
- Theme colors
- Animation settings

## Troubleshooting

### Common Issues

1. **Floating taskbar not working**
   - Ensure Windhawk and ExplorerPatcher are running
   - Check that the floating taskbar mod is properly installed
   - Restart Windows Explorer (Ctrl+Shift+Esc > File > Run new task > explorer.exe)

2. **Widgets not appearing**
   - Verify Rainmeter is running
   - Check widget configurations in the config files
   - Ensure the top widgets mod is active in Windhawk

3. **Visual effects not applying**
   - Make sure all visual effect tools are installed
   - Check that DWM is running (Windows key + R > services.msc)
   - Verify that transparency effects are enabled in system settings

### System Restore

If you need to revert to the original Windows 11 UI:

1. **Uninstall all components** via Control Panel or Settings > Apps
2. **Restore registry** using the backup created during installation
3. **Reset Windows Explorer** settings
4. **Reboot** your system

## Support

For additional support and updates, visit:
- GitHub: https://github.com/QuiteAFancyEmerald/Slate-Desktop-for-Windows-11
- Issues: Report any problems in the GitHub issues section

## Credits

This Windows 12 UI transformation is made possible by:
- Windhawk Team - Customization engine
- ExplorerPatcher Team - Explorer modifications
- Microsoft - Windows 12 design concepts and Copilot 2.0
- Various open-source contributors

---

*Last updated: 2026-09-05*
*Version: 2.0.0 - Next Valley Edition*
