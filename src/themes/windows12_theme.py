#!/usr/bin/env python3
"""
Windows 12 Theme Module for Windows 12 UI Transformation
Version: 2.0.0 - Next Valley Edition

Implements the complete Windows 12 visual theme system.
"""

import json
import subprocess
import sys
import platform
from pathlib import Path
from typing import Dict, Any, Optional
import shutil

# Import winreg only on Windows
if platform.system() == 'Windows':
    import winreg
else:
    # Create a mock winreg module for non-Windows platforms
    import types
    
    class MockWinReg:
        HKEY_CURRENT_USER = 'HKEY_CURRENT_USER'
        HKEY_LOCAL_MACHINE = 'HKEY_LOCAL_MACHINE'
        KEY_WRITE = 0
        REG_DWORD = 0
        REG_SZ = 0
        
        @staticmethod
        def CreateKeyEx(*args, **kwargs):
            class MockKey:
                def __enter__(self):
                    return self
                def __exit__(self, *args):
                    pass
                def Close(self):
                    pass
            return MockKey()
        
        @staticmethod
        def SetValueEx(*args, **kwargs):
            pass
        
        @staticmethod
        def OpenKey(*args, **kwargs):
            class MockKey:
                def __enter__(self):
                    return self
                def __exit__(self, *args):
                    pass
                def Close(self):
                    pass
            return MockKey()
    
    winreg = MockWinReg()
    sys.modules['winreg'] = winreg
    sys.modules['winreg'] = winreg


class Windows12ThemeModule:
    """
    Windows 12 Theme Module
    
    Implements the complete Windows 12 visual theme including:
    - pi11z Windows 12 Edition theme
    - Windows 12 icons
    - SecureUXTheme patching
    - Theme switching
    - Visual style customization
    """
    
    def __init__(self):
        self.name = "Windows 12 Theme"
        self.description = "Complete Windows 12 visual theme with floating taskbar support"
        self.version = "2.0.0"
        self.author = "Slate Desktop Team"
        self.dependencies = ['secureuxtheme', 'uxthemepatcher', '7tsp']
        
        # Configuration
        self.config = {
            'enabled': True,
            'theme_name': 'Windows 12 Next Valley',
            'theme_version': '2.0.0',
            'base_theme': 'pi11z',
            'theme_files': {
                'msstyle': 'pi11z-Windows12.msstyle',
                'theme': 'pi11z-Windows12.theme',
                'shellstyle': 'pi11z-Windows12-ShellStyle.dll'
            },
            'colors': {
                'primary': '#0078D4',
                'secondary': '#107C10',
                'accent': '#00B294',
                'background': '#000000',
                'surface': '#121212',
                'text_primary': '#FFFFFF',
                'text_secondary': '#B0B0B0'
            },
            'font': {
                'name': 'Segoe UI',
                'size': 9,
                'weight': 400
            },
            'window_metrics': {
                'border_width': -15,
                'caption_height': 24,
                'caption_font_height': 14,
                'small_caption_height': 20,
                'menu_height': 22,
                'scroll_width': 12,
                'scroll_height': 12
            },
            'transparency': {
                'enabled': True,
                'level': 0.7,
                'active_window': 0.9,
                'inactive_window': 0.7
            },
            'animations': {
                'enabled': True,
                'duration': 200,
                'easing': 'ease-out'
            }
        }
        
        # Theme paths - using raw strings for Windows paths
        self.theme_paths = {
            'resources': Path(__file__).parent.parent.parent.parent / 'sources' / 'downloads' / '04 - Themes',
            'themes_folder': Path(r'C:\Windows\Resources\Themes'),
            'system32': Path(r'C:\Windows\System32'),
            'syswow64': Path(r'C:\Windows\SysWOW64')
        }
    
    def get_name(self) -> str:
        """Get module name"""
        return self.name
    
    def get_description(self) -> str:
        """Get module description"""
        return self.description
    
    def get_version(self) -> str:
        """Get module version"""
        return self.version
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """Set configuration"""
        self.config.update(config)
    
    def check_dependencies(self) -> bool:
        """Check if all dependencies are installed"""
        missing_deps = []
        
        for dep in self.dependencies:
            try:
                result = subprocess.run(
                    ['where', dep],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    missing_deps.append(dep)
            except:
                missing_deps.append(dep)
        
        return len(missing_deps) == 0
    
    def install_dependencies(self) -> bool:
        """Install required dependencies"""
        print(f"Installing dependencies for {self.name}...")
        
        # Install via winget or direct download
        # Note: SecureUXTheme and UXThemePatcher may need to be downloaded manually
        winget_commands = [
            'winget install --id namazso.SecureUxTheme',
        ]
        
        success_count = 0
        for cmd in winget_commands:
            try:
                result = subprocess.run(
                    ['powershell', '-Command', cmd],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f"[+] Installed: {cmd}")
                    success_count += 1
                else:
                    print(f"[-] Failed to install: {cmd}")
            except Exception as e:
                print(f"[-] Error installing dependency: {e}")
        
        # Manual dependencies
        manual_deps = ['UXThemePatcher', '7TSP']
        for dep in manual_deps:
            print(f"[!] {dep} requires manual installation")
        
        return success_count == len(winget_commands)
    
    def apply_registry_tweaks(self) -> bool:
        """Apply registry tweaks for Windows 12 theme"""
        print(f"Applying registry tweaks for {self.name}...")
        
        tweaks = [
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes',
                'value': 'CurrentTheme',
                'data': self.config['theme_name'],
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes',
                'value': 'CurrentColorScheme',
                'data': 'Windows 12',
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes',
                'value': 'CurrentSize',
                'data': 'Normal',
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize',
                'value': 'WindowMetrics',
                'data': f'0,0,0,0,0,0,0,0,{abs(self.config["window_metrics"]["border_width"])},0,0,0,0,0,0',
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Control Panel\Desktop\WindowMetrics',
                'value': 'BorderWidth',
                'data': str(self.config['window_metrics']['border_width']),
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Control Panel\Desktop\WindowMetrics',
                'value': 'CaptionHeight',
                'data': str(self.config['window_metrics']['caption_height']),
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Control Panel\Desktop\WindowMetrics',
                'value': 'CaptionFontHeight',
                'data': str(self.config['window_metrics']['caption_font_height']),
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Control Panel\Desktop\WindowMetrics',
                'value': 'MenuHeight',
                'data': str(self.config['window_metrics']['menu_height']),
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Control Panel\Desktop\WindowMetrics',
                'value': 'ScrollWidth',
                'data': str(self.config['window_metrics']['scroll_width']),
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Control Panel\Desktop\WindowMetrics',
                'value': 'ScrollHeight',
                'data': str(self.config['window_metrics']['scroll_height']),
                'type': winreg.REG_SZ
            }
        ]
        
        applied = 0
        for tweak in tweaks:
            try:
                key_path = tweak['path'].split('\\')
                base_key = key_path[0]
                sub_key = '\\'.join(key_path[1:])
                
                key_map = {
                    'HKCU': winreg.HKEY_CURRENT_USER,
                    'HKLM': winreg.HKEY_LOCAL_MACHINE
                }
                
                if base_key in key_map:
                    with winreg.CreateKeyEx(key_map[base_key], sub_key, 0, winreg.KEY_WRITE) as key:
                        winreg.SetValueEx(key, tweak['value'], 0, tweak['type'], tweak['data'])
                        applied += 1
            except Exception as e:
                print(f"[-] Error applying registry tweak: {e}")
        
        print(f"[+] Applied {applied} registry tweaks")
        return applied > 0
    
    def patch_system_files(self) -> bool:
        """Patch system files for third-party themes"""
        print(f"Patching system files for {self.name}...")
        
        try:
            # Check if SecureUXTheme is running
            result = subprocess.run(
                ['powershell', '-Command', 'Get-Process -Name ThemeTool'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"[+] SecureUXTheme is running")
            else:
                print(f"[!] SecureUXTheme not running, attempting to start...")
                # Try to start SecureUXTheme
                secureux_path = Path(r'C:\Program Files\SecureUxTheme\ThemeTool.exe')
                if secureux_path.exists():
                    subprocess.Popen([str(secureux_path)])
                    print(f"[+] Started SecureUXTheme")
                else:
                    print(f"[-] SecureUXTheme not found")
                    return False
            
            # Apply theme using UXThemePatcher if needed
            uxtheme_path = Path(r'C:\Program Files\UXThemePatcher\UXThemePatcher.exe')
            if uxtheme_path.exists():
                result = subprocess.run(
                    [str(uxtheme_path), '/apply'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f"[+] Applied UXThemePatcher")
                else:
                    print(f"[-] UXThemePatcher failed")
                    return False
            
            print(f"[+] System files patched successfully")
            return True
            
        except Exception as e:
            print(f"[-] Error patching system files: {e}")
            return False
    
    def install_theme_files(self) -> bool:
        """Install Windows 12 theme files"""
        print(f"Installing theme files for {self.name}...")
        
        try:
            # Create themes directory if it doesn't exist
            themes_dir = self.theme_paths['themes_folder']
            themes_dir.mkdir(parents=True, exist_ok=True)
            
            # Check if theme files exist in sources
            source_themes_dir = self.theme_paths['resources'] / 'Step 1 - Windows 12 Theme'
            
            if source_themes_dir.exists():
                # Copy theme files to Windows Themes directory
                theme_files = [
                    'pi11z-Windows12.msstyle',
                    'pi11z-Windows12.theme',
                    'pi11z-Windows12-ShellStyle.dll'
                ]
                
                copied = 0
                for theme_file in theme_files:
                    source_file = source_themes_dir / theme_file
                    if source_file.exists():
                        dest_file = themes_dir / theme_file
                        shutil.copy2(source_file, dest_file)
                        print(f"[+] Copied: {theme_file}")
                        copied += 1
                
                if copied > 0:
                    print(f"[+] Copied {copied} theme files")
                    return True
                else:
                    print(f"[-] No theme files found in sources")
                    return False
            else:
                print(f"[-] Theme files not found in sources")
                return False
                
        except Exception as e:
            print(f"[-] Error installing theme files: {e}")
            return False
    
    def install_icons(self) -> bool:
        """Install Windows 12 icons"""
        print(f"Installing icons for {self.name}...")
        
        try:
            # Check if 7TSP is installed
            tsp_path = Path(r'C:\Program Files\7TSP\7tsp_gui.exe')
            if not tsp_path.exists():
                print(f"[!] 7TSP not found, icon installation may not work")
            
            # Check if icon files exist in sources
            source_icons_dir = self.theme_paths['resources'] / 'Step 2 - Windows 12 Icons'
            
            if source_icons_dir.exists():
                # Apply icons using 7TSP
                icon_files = list(source_icons_dir.glob('*.mun'))
                
                if icon_files:
                    print(f"[+] Found {len(icon_files)} icon files")
                    # This would be applied through 7TSP GUI or command line
                    print(f"[!] Icons need to be applied manually through 7TSP")
                    return True
                else:
                    print(f"[-] No icon files found")
                    return False
            else:
                print(f"[-] Icon files not found in sources")
                return False
                
        except Exception as e:
            print(f"[-] Error installing icons: {e}")
            return False
    
    def create_theme_config(self) -> bool:
        """Create theme configuration file"""
        print(f"Creating theme configuration for {self.name}...")
        
        theme_config = {
            "version": self.version,
            "name": self.config['theme_name'],
            "description": self.description,
            "base_theme": self.config['base_theme'],
            "theme_files": self.config['theme_files'],
            "colors": self.config['colors'],
            "font": self.config['font'],
            "window_metrics": self.config['window_metrics'],
            "transparency": self.config['transparency'],
            "animations": self.config['animations'],
            "dependencies": self.dependencies,
            "installation": {
                "themes_folder": str(self.theme_paths['themes_folder']),
                "system32": str(self.theme_paths['system32']),
                "syswow64": str(self.theme_paths['syswow64']),
                "patched": False,
                "active": False
            }
        }
        
        try:
            config_dir = Path(__file__).parent.parent.parent.parent / 'config' / 'Windows12'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'windows12_theme_config.json'
            
            with open(config_file, 'w') as f:
                json.dump(theme_config, f, indent=4)
            
            print(f"[+] Theme configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error creating theme configuration: {e}")
            return False
    
    def create_theme_script(self) -> bool:
        """Create PowerShell script for theme management"""
        print(f"Creating theme management script...")
        
        script_content = """# Windows 12 Theme Management Script
# Version: 2.0.0 - Next Valley Edition

param(
    [string]$ThemeName = "Windows 12 Next Valley",
    [string]$BaseTheme = "pi11z",
    [bool]$ApplyTheme = $True,
    [bool]$PatchSystem = $True
)

# Patch system for third-party themes
if ($PatchSystem) {
    # Check and start SecureUXTheme
    if (Test-Path "C:\\Program Files\\SecureUxTheme\\ThemeTool.exe") {
        $process = Get-Process -Name ThemeTool -ErrorAction SilentlyContinue
        if (-not $process) {
            Start-Process -FilePath "C:\\Program Files\\SecureUxTheme\\ThemeTool.exe"
            Start-Sleep -Seconds 2
        }
        Write-Host "SecureUXTheme is running" -ForegroundColor Green
    } else {
        Write-Host "SecureUXTheme not found" -ForegroundColor Yellow
    }
    
    # Apply UXThemePatcher
    if (Test-Path "C:\\Program Files\\UXThemePatcher\\UXThemePatcher.exe") {
        & "C:\\Program Files\\UXThemePatcher\\UXThemePatcher.exe" /apply
        Write-Host "UXThemePatcher applied" -ForegroundColor Green
    } else {
        Write-Host "UXThemePatcher not found" -ForegroundColor Yellow
    }
}

# Apply theme
if ($ApplyTheme) {
    # Set theme registry values
    $themeReg = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes"
    Set-ItemProperty -Path $themeReg -Name "CurrentTheme" -Value $ThemeName
    Set-ItemProperty -Path $themeReg -Name "CurrentColorScheme" -Value "Windows 12"
    Set-ItemProperty -Path $themeReg -Name "CurrentSize" -Value "Normal"
    
    # Set window metrics
    $metricsReg = "HKCU:\\Control Panel\\Desktop\\WindowMetrics"
    Set-ItemProperty -Path $metricsReg -Name "BorderWidth" -Value -15
    Set-ItemProperty -Path $metricsReg -Name "CaptionHeight" -Value 24
    
    # Restart Windows Explorer to apply theme
    Stop-Process -Name "explorer" -Force
    Start-Process "explorer.exe"
    
    Write-Host "Windows 12 Theme applied!" -ForegroundColor Green
}

# Apply icons using 7TSP
if (Test-Path "C:\\Program Files\\7TSP\\7tsp_gui.exe") {
    Write-Host "7TSP found - apply icons manually through GUI" -ForegroundColor Cyan
} else {
    Write-Host "7TSP not found - icons cannot be applied" -ForegroundColor Yellow
}
"""
        
        try:
            scripts_dir = Path(__file__).parent.parent.parent / 'src' / 'scripts'
            scripts_dir.mkdir(parents=True, exist_ok=True)
            script_file = scripts_dir / 'configure_windows12_theme.ps1'
            
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            print(f"[+] Theme script created: {script_file}")
            return True
        except Exception as e:
            print(f"[-] Error creating theme script: {e}")
            return False
    
    def install(self) -> bool:
        """Install the Windows 12 theme module"""
        print(f"\n{'='*60}")
        print(f"Installing: {self.name}")
        print(f"Version: {self.version}")
        print(f"{'='*60}\n")
        
        success = True
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            print(f"[!] Dependencies missing. Installing...")
            if not self.install_dependencies():
                print(f"[-] Failed to install dependencies")
                success = False
        
        # Step 2: Apply registry tweaks
        if not self.apply_registry_tweaks():
            print(f"[-] Failed to apply registry tweaks")
            success = False
        
        # Step 3: Patch system files
        if not self.patch_system_files():
            print(f"[-] Failed to patch system files")
            success = False
        
        # Step 4: Install theme files
        if not self.install_theme_files():
            print(f"[-] Failed to install theme files")
            success = False
        
        # Step 5: Install icons
        if not self.install_icons():
            print(f"[-] Failed to install icons")
            success = False
        
        # Step 6: Create theme configuration
        if not self.create_theme_config():
            print(f"[-] Failed to create theme configuration")
            success = False
        
        # Step 7: Create theme script
        if not self.create_theme_script():
            print(f"[-] Failed to create theme script")
            success = False
        
        if success:
            print(f"\n[+] {self.name} installed successfully!")
        else:
            print(f"\n[-] {self.name} installation completed with errors")
        
        return success
    
    def uninstall(self) -> bool:
        """Uninstall the Windows 12 theme module"""
        print(f"Uninstalling: {self.name}")
        
        try:
            # Remove theme files
            themes_dir = self.theme_paths['themes_folder']
            theme_files = [
                'pi11z-Windows12.msstyle',
                'pi11z-Windows12.theme',
                'pi11z-Windows12-ShellStyle.dll'
            ]
            
            removed = 0
            for theme_file in theme_files:
                theme_path = themes_dir / theme_file
                if theme_path.exists():
                    theme_path.unlink()
                    print(f"[+] Removed: {theme_file}")
                    removed += 1
            
            if removed > 0:
                print(f"[+] Removed {removed} theme files")
            
            # Remove theme configuration
            config_file = Path(__file__).parent.parent.parent.parent / 'config' / 'Windows12' / 'windows12_theme_config.json'
            if config_file.exists():
                config_file.unlink()
                print(f"[+] Removed theme configuration")
            
            # Remove theme script
            scripts_dir = Path(__file__).parent.parent.parent / 'src' / 'scripts'
            theme_script = scripts_dir / 'configure_windows12_theme.ps1'
            if theme_script.exists():
                theme_script.unlink()
                print(f"[+] Removed theme script")
            
            # Reset registry settings
            self.reset_registry()
            
            print(f"[+] {self.name} uninstalled successfully!")
            return True
        except Exception as e:
            print(f"[-] Error uninstalling: {e}")
            return False
    
    def reset_registry(self) -> bool:
        """Reset registry settings to defaults"""
        print(f"Resetting registry settings...")
        
        try:
            # Reset theme settings
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Software\Microsoft\Windows\CurrentVersion\Themes', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'CurrentTheme')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'CurrentColorScheme')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'CurrentSize')
                except:
                    pass
            
            # Reset WindowMetrics
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Control Panel\Desktop\WindowMetrics', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'BorderWidth')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'CaptionHeight')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'CaptionFontHeight')
                except:
                    pass
            
            print(f"[+] Registry settings reset")
            return True
        except Exception as e:
            print(f"[-] Error resetting registry: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the module"""
        status = {
            'installed': False,
            'enabled': self.config['enabled'],
            'dependencies_installed': self.check_dependencies(),
            'registry_applied': False,
            'theme_files_installed': False,
            'icons_installed': False,
            'system_patched': False
        }
        
        # Check if theme files exist
        themes_dir = self.theme_paths['themes_folder']
        theme_files = [
            'pi11z-Windows12.msstyle',
            'pi11z-Windows12.theme'
        ]
        
        for theme_file in theme_files:
            if (themes_dir / theme_file).exists():
                status['theme_files_installed'] = True
                break
        
        # Check if icons are configured
        # This would require checking 7TSP configuration
        
        return status


# Module interface
if __name__ == "__main__":
    module = Windows12ThemeModule()
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        success = module.install()
        sys.exit(0 if success else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        success = module.uninstall()
        sys.exit(0 if success else 1)
    else:
        print(f"{module.get_name()} - {module.get_description()}")
        print("Usage: python windows12_theme.py [install|uninstall]")
