#!/usr/bin/env python3
"""
Fluent Design 3.0 Module for Windows 12 UI Transformation
Version: 2.0.0 - Next Valley Edition

Implements Fluent Design 3.0 with rounded corners and modern UI elements.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import winreg


class FluentDesign3Module:
    """
    Fluent Design 3.0 Module
    
    Implements Windows 12 Fluent Design 3.0 features including:
    - Rounded corners for all UI elements
    - Mica and acrylic effects
    - Smooth animations
    - Modern color schemes
    - Consistent spacing and padding
    """
    
    def __init__(self):
        self.name = "Fluent Design 3.0"
        self.description = "Windows 12 Fluent Design 3.0 with rounded corners and modern UI"
        self.version = "2.0.0"
        self.author = "Slate Desktop Team"
        self.dependencies = ['explorerblurmica', 'dwmblurglass', 'micaforeveryone']
        
        # Configuration
        self.config = {
            'enabled': True,
            'fluent_design_version': '3.0',
            'rounded_corners': True,
            'corner_radius': 12,
            'mica_effect': True,
            'acrylic_effect': True,
            'animations': True,
            'theme': 'dark',
            'accent_color': '#0078D4',
            'transparency_level': 0.7,
            'blur_intensity': 100,
            'material': 'mica',  # mica, acrylic, or solid
            'elevation': True,
            'shadow_effects': True
        }
        
        # Design system values
        self.design_system = {
            'spacing': {
                'xxs': 2,
                'xs': 4,
                's': 8,
                'm': 12,
                'l': 16,
                'xl': 24,
                'xxl': 32
            },
            'colors': {
                'primary': '#0078D4',
                'secondary': '#107C10',
                'tertiary': '#00B294',
                'background': '#000000',
                'surface': '#121212',
                'text_primary': '#FFFFFF',
                'text_secondary': '#B0B0B0',
                'text_tertiary': '#808080',
                'accent': '#0078D4',
                'error': '#F1707B',
                'warning': '#FF8C00',
                'success': '#107C10'
            },
            'typography': {
                'font_family': 'Segoe UI',
                'base_size': 14,
                'caption': 12,
                'body': 14,
                'subheading': 16,
                'heading': 20,
                'title': 24,
                'large_title': 28
            }
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
        
        # Install via winget
        winget_commands = [
            'winget install --id Maplespe.ExplorerBlurMica',
            'winget install --id Maplespe.DWMBlurGlass',
            'winget install --id MicaForEveryone.MicaForEveryone'
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
        
        return success_count == len(winget_commands)
    
    def apply_registry_tweaks(self) -> bool:
        """Apply registry tweaks for Fluent Design 3.0"""
        print(f"Applying registry tweaks for {self.name}...")
        
        tweaks = [
            {
                'path': r'HKCU\Control Panel\Desktop\WindowMetrics',
                'value': 'BorderWidth',
                'data': f'-{self.config["corner_radius"]}',
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Control Panel\Desktop',
                'value': 'WindowMetrics',
                'data': f'0,0,0,0,0,0,0,0,-{self.config["corner_radius"]},0,0,0,0,0,0',
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\DWM',
                'value': 'ColorizationColor',
                'data': self.hex_to_dword(self.config['accent_color']),
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\DWM',
                'value': 'ColorizationAfterglow',
                'data': self.hex_to_dword(self.config['accent_color']),
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\DWM',
                'value': 'EnableAeroPeek',
                'data': 1,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\DWM',
                'value': 'AlwaysHibernateThumbnails',
                'data': 0,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize',
                'value': 'EnableTransparency',
                'data': 1,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize',
                'value': 'AppsUseLightTheme',
                'data': 0,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize',
                'value': 'SystemUsesLightTheme',
                'data': 0,
                'type': winreg.REG_DWORD
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
    
    def hex_to_dword(self, hex_color: str) -> int:
        """Convert hex color to DWORD value"""
        # Remove # if present
        hex_color = hex_color.lstrip('#')
        
        # Convert to BGR format (Windows uses BGR, not RGB)
        if len(hex_color) == 6:
            # RRGGBB -> BBRRGGBB
            bgr = hex_color[4:6] + hex_color[2:4] + hex_color[0:2]
            return int(bgr, 16)
        elif len(hex_color) == 8:
            # AARRGGBB -> AABBRRGGBB
            aarrggbb = hex_color[6:8] + hex_color[4:6] + hex_color[2:4] + hex_color[0:2]
            return int(aarrggbb, 16)
        
        return 0
    
    def configure_explorerblurmica(self) -> bool:
        """Configure ExplorerBlurMica for Fluent Design"""
        print(f"Configuring ExplorerBlurMica for {self.name}...")
        
        # ExplorerBlurMica configuration
        ebm_config = {
            "accentColor": self.config['accent_color'],
            "blurValue": self.config['blur_intensity'],
            "opacity": int(self.config['transparency_level'] * 255),
            "noBorder": True,
            "extendFrameIntoClientArea": True,
            "micaEffect": self.config['mica_effect'],
            "acrylicEffect": self.config['acrylic_effect'],
            "roundedCorners": self.config['rounded_corners'],
            "cornerRadius": self.config['corner_radius'],
            "animations": self.config['animations']
        }
        
        try:
            # Save ExplorerBlurMica configuration
            config_dir = Path.home() / 'AppData' / 'Local' / 'ExplorerBlurMica'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'config.json'
            
            with open(config_file, 'w') as f:
                json.dump(ebm_config, f, indent=4)
            
            print(f"[+] ExplorerBlurMica configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error configuring ExplorerBlurMica: {e}")
            return False
    
    def configure_dwmblurglass(self) -> bool:
        """Configure DWMBlurGlass for window effects"""
        print(f"Configuring DWMBlurGlass for {self.name}...")
        
        # DWMBlurGlass configuration
        dwm_config = {
            "blurValue": self.config['blur_intensity'],
            "opacity": int(self.config['transparency_level'] * 255),
            "roundedCorners": self.config['rounded_corners'],
            "cornerRadius": self.config['corner_radius'],
            "extendFrame": True,
            "noBorder": True,
            "animations": self.config['animations'],
            "color": self.config['accent_color']
        }
        
        try:
            # Save DWMBlurGlass configuration
            config_dir = Path.home() / 'AppData' / 'Local' / 'DWMBlurGlass'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'config.json'
            
            with open(config_file, 'w') as f:
                json.dump(dwm_config, f, indent=4)
            
            print(f"[+] DWMBlurGlass configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error configuring DWMBlurGlass: {e}")
            return False
    
    def configure_micaforeveryone(self) -> bool:
        """Configure MicaForEveryone for extended effects"""
        print(f"Configuring MicaForEveryone for {self.name}...")
        
        # MicaForEveryone configuration
        mfe_config = {
            "enabled": True,
            "effectType": self.config['material'],
            "darkMode": self.config['theme'] == 'dark',
            "lightMode": self.config['theme'] == 'light',
            "accentColor": self.config['accent_color'],
            "opacity": int(self.config['transparency_level'] * 255),
            "blurValue": self.config['blur_intensity'],
            "roundedCorners": self.config['rounded_corners'],
            "cornerRadius": self.config['corner_radius'],
            "animations": self.config['animations']
        }
        
        try:
            # Save MicaForEveryone configuration
            config_dir = Path.home() / 'AppData' / 'Local' / 'MicaForEveryone'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'config.json'
            
            with open(config_file, 'w') as f:
                json.dump(mfe_config, f, indent=4)
            
            print(f"[+] MicaForEveryone configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error configuring MicaForEveryone: {e}")
            return False
    
    def create_design_config(self) -> bool:
        """Create comprehensive design configuration file"""
        print(f"Creating design configuration for {self.name}...")
        
        design_config = {
            "fluent_design_version": self.config['fluent_design_version'],
            "theme": self.config['theme'],
            "colors": self.design_system['colors'],
            "spacing": self.design_system['spacing'],
            "typography": self.design_system['typography'],
            "effects": {
                "mica": self.config['mica_effect'],
                "acrylic": self.config['acrylic_effect'],
                "transparency": self.config['transparency_level'],
                "blur": self.config['blur_intensity'],
                "rounded_corners": self.config['rounded_corners'],
                "corner_radius": self.config['corner_radius'],
                "animations": self.config['animations'],
                "shadows": self.config['shadow_effects'],
                "elevation": self.config['elevation']
            },
            "components": {
                "windows": {
                    "rounded_corners": True,
                    "corner_radius": self.config['corner_radius'],
                    "transparency": self.config['transparency_level'],
                    "blur": self.config['blur_intensity']
                },
                "taskbar": {
                    "rounded_corners": True,
                    "corner_radius": self.config['corner_radius'],
                    "transparency": self.config['transparency_level'],
                    "material": self.config['material']
                },
                "start_menu": {
                    "rounded_corners": True,
                    "corner_radius": self.config['corner_radius'],
                    "transparency": self.config['transparency_level'],
                    "material": self.config['material']
                },
                "file_explorer": {
                    "rounded_corners": True,
                    "corner_radius": self.config['corner_radius'],
                    "transparency": self.config['transparency_level'],
                    "material": self.config['material']
                }
            }
        }
        
        try:
            config_dir = Path(__file__).parent.parent.parent.parent / 'config' / 'Windows12'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'fluent_design_config.json'
            
            with open(config_file, 'w') as f:
                json.dump(design_config, f, indent=4)
            
            print(f"[+] Design configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error creating design configuration: {e}")
            return False
    
    def create_design_script(self) -> bool:
        """Create PowerShell script for design configuration"""
        print(f"Creating design configuration script...")
        
        script_content = f'''
# Windows 12 Fluent Design 3.0 Configuration Script
# Version: 2.0.0 - Next Valley Edition

param(
    [string]$Theme = "{self.config['theme']}",
    [string]$AccentColor = "{self.config['accent_color']}",
    [int]$CornerRadius = {self.config['corner_radius']},
    [int]$Transparency = {int(self.config['transparency_level'] * 255)},
    [int]$BlurIntensity = {self.config['blur_intensity']},
    [bool]$MicaEffect = $True,
    [bool]$AcrylicEffect = $True,
    [bool]$RoundedCorners = $True,
    [bool]$Animations = $True
)

# Apply ExplorerBlurMica settings
if (Test-Path "$env:LOCALAPPDATA\\ExplorerBlurMica\\ExplorerBlurMica.exe") {{
    $ebmConfig = @{{
        accentColor = "$AccentColor"
        blurValue = $BlurIntensity
        opacity = $Transparency
        micaEffect = $MicaEffect
        acrylicEffect = $AcrylicEffect
        roundedCorners = $RoundedCorners
        cornerRadius = $CornerRadius
        animations = $Animations
    }}
    
    $ebmConfig | ConvertTo-Json | Out-File -FilePath "$env:LOCALAPPDATA\\ExplorerBlurMica\\config.json" -Encoding UTF8
}}

# Apply DWMBlurGlass settings
if (Test-Path "$env:LOCALAPPDATA\\DWMBlurGlass\\DWMBlurGlass.exe") {{
    $dwmConfig = @{{
        blurValue = $BlurIntensity
        opacity = $Transparency
        roundedCorners = $RoundedCorners
        cornerRadius = $CornerRadius
        animations = $Animations
        color = "$AccentColor"
    }}
    
    $dwmConfig | ConvertTo-Json | Out-File -FilePath "$env:LOCALAPPDATA\\DWMBlurGlass\\config.json" -Encoding UTF8
}}

# Apply MicaForEveryone settings
if (Test-Path "$env:LOCALAPPDATA\\MicaForEveryone\\MicaForEveryone.exe") {{
    $mfeConfig = @{{
        enabled = $True
        effectType = "mica"
        darkMode = ($Theme -eq "dark")
        accentColor = "$AccentColor"
        opacity = $Transparency
        blurValue = $BlurIntensity
        roundedCorners = $RoundedCorners
        cornerRadius = $CornerRadius
        animations = $Animations
    }}
    
    $mfeConfig | ConvertTo-Json | Out-File -FilePath "$env:LOCALAPPDATA\\MicaForEveryone\\config.json" -Encoding UTF8
}}

# Restart DWM to apply changes
Stop-Process -Name "dwm" -Force -ErrorAction SilentlyContinue

Write-Host "Windows 12 Fluent Design 3.0 configuration applied!" -ForegroundColor Green
'''
        
        try:
            scripts_dir = Path(__file__).parent.parent.parent / 'src' / 'scripts'
            scripts_dir.mkdir(parents=True, exist_ok=True)
            script_file = scripts_dir / 'configure_fluent_design.ps1'
            
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            print(f"[+] Design script created: {script_file}")
            return True
        except Exception as e:
            print(f"[-] Error creating design script: {e}")
            return False
    
    def install(self) -> bool:
        """Install the Fluent Design 3.0 module"""
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
        
        # Step 3: Configure ExplorerBlurMica
        if not self.configure_explorerblurmica():
            print(f"[-] Failed to configure ExplorerBlurMica")
            success = False
        
        # Step 4: Configure DWMBlurGlass
        if not self.configure_dwmblurglass():
            print(f"[-] Failed to configure DWMBlurGlass")
            success = False
        
        # Step 5: Configure MicaForEveryone
        if not self.configure_micaforeveryone():
            print(f"[-] Failed to configure MicaForEveryone")
            success = False
        
        # Step 6: Create design configuration
        if not self.create_design_config():
            print(f"[-] Failed to create design configuration")
            success = False
        
        # Step 7: Create configuration script
        if not self.create_design_script():
            print(f"[-] Failed to create configuration script")
            success = False
        
        if success:
            print(f"\n[+] {self.name} installed successfully!")
        else:
            print(f"\n[-] {self.name} installation completed with errors")
        
        return success
    
    def uninstall(self) -> bool:
        """Uninstall the Fluent Design 3.0 module"""
        print(f"Uninstalling: {self.name}")
        
        try:
            # Remove ExplorerBlurMica configuration
            ebm_config = Path.home() / 'AppData' / 'Local' / 'ExplorerBlurMica' / 'config.json'
            if ebm_config.exists():
                ebm_config.unlink()
                print(f"[+] Removed ExplorerBlurMica configuration")
            
            # Remove DWMBlurGlass configuration
            dwm_config = Path.home() / 'AppData' / 'Local' / 'DWMBlurGlass' / 'config.json'
            if dwm_config.exists():
                dwm_config.unlink()
                print(f"[+] Removed DWMBlurGlass configuration")
            
            # Remove MicaForEveryone configuration
            mfe_config = Path.home() / 'AppData' / 'Local' / 'MicaForEveryone' / 'config.json'
            if mfe_config.exists():
                mfe_config.unlink()
                print(f"[+] Removed MicaForEveryone configuration")
            
            # Remove design configuration
            design_config = Path(__file__).parent.parent.parent.parent / 'config' / 'Windows12' / 'fluent_design_config.json'
            if design_config.exists():
                design_config.unlink()
                print(f"[+] Removed design configuration")
            
            # Remove design script
            scripts_dir = Path(__file__).parent.parent.parent / 'src' / 'scripts'
            design_script = scripts_dir / 'configure_fluent_design.ps1'
            if design_script.exists():
                design_script.unlink()
                print(f"[+] Removed design script")
            
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
            # Reset WindowMetrics
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Control Panel\Desktop\WindowMetrics', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'BorderWidth')
                except:
                    pass
            
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Control Panel\Desktop', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'WindowMetrics')
                except:
                    pass
            
            # Reset DWM settings
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Software\Microsoft\Windows\DWM', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'ColorizationColor')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'ColorizationAfterglow')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'EnableAeroPeek')
                except:
                    pass
            
            # Reset theme settings
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'EnableTransparency')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'AppsUseLightTheme')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'SystemUsesLightTheme')
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
            'explorerblurmica_configured': False,
            'dwmblurglass_configured': False,
            'micaforeveryone_configured': False
        }
        
        # Check if configurations exist
        ebm_config = Path.home() / 'AppData' / 'Local' / 'ExplorerBlurMica' / 'config.json'
        dwm_config = Path.home() / 'AppData' / 'Local' / 'DWMBlurGlass' / 'config.json'
        mfe_config = Path.home() / 'AppData' / 'Local' / 'MicaForEveryone' / 'config.json'
        
        status['explorerblurmica_configured'] = ebm_config.exists()
        status['dwmblurglass_configured'] = dwm_config.exists()
        status['micaforeveryone_configured'] = mfe_config.exists()
        
        return status


# Module interface
if __name__ == "__main__":
    module = FluentDesign3Module()
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        success = module.install()
        sys.exit(0 if success else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        success = module.uninstall()
        sys.exit(0 if success else 1)
    else:
        print(f"{module.get_name()} - {module.get_description()}")
        print("Usage: python fluent_design.py [install|uninstall]")
