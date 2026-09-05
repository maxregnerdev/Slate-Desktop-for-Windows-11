#!/usr/bin/env python3
"""
Floating Taskbar Module for Windows 12 UI Transformation
Version: 2.0.0 - Next Valley Edition

Implements the floating taskbar feature inspired by macOS and Windows 12 concepts.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import winreg


class FloatingTaskbarModule:
    """
    Floating Taskbar Module
    
    Implements the Next Valley floating taskbar design with:
    - Floating taskbar with desktop background spill-over
    - Rounded corners
    - Transparency effects
    - macOS-inspired design
    """
    
    def __init__(self):
        self.name = "Floating Taskbar"
        self.description = "Next Valley floating taskbar with macOS-inspired design"
        self.version = "2.0.0"
        self.author = "Slate Desktop Team"
        self.dependencies = ['windhawk', 'explorerpatcher', 'translucenttb']
        
        # Configuration
        self.config = {
            'enabled': True,
            'floating': True,
            'position': 'bottom',
            'transparency': 0.8,
            'rounded_corners': True,
            'corner_radius': 16,
            'auto_hide': False,
            'icon_size': 'medium',
            'labels': False,
            'spacing': 8,
            'background_spill': True,
            'animation': True
        }
        
        # Registry paths
        self.registry_paths = {
            'taskbar_settings': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',
            'taskbar_metrics': r'HKCU\Control Panel\Desktop\WindowMetrics',
            'taskbar_style': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3'
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
            'winget install --id RamenSoftware.Windhawk',
            'winget install --id valinet.ExplorerPatcher',
            'winget install --id TranslucentTB.TranslucentTB'
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
        """Apply registry tweaks for floating taskbar"""
        print(f"Applying registry tweaks for {self.name}...")
        
        tweaks = [
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',
                'value': 'TaskbarSmallIcons',
                'data': 0,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',
                'value': 'TaskbarGlomLevel',
                'data': 2,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer',
                'value': 'TaskbarAutoHide',
                'data': 1 if self.config['auto_hide'] else 0,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Control Panel\Desktop\WindowMetrics',
                'value': 'BorderWidth',
                'data': -15,
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
    
    def configure_windhawk(self) -> bool:
        """Configure Windhawk for floating taskbar"""
        print(f"Configuring Windhawk for {self.name}...")
        
        # Windhawk configuration for floating taskbar
        windhawk_config = {
            "mods": {
                "taskbar_floating": {
                    "enabled": True,
                    "floating": True,
                    "position": self.config['position'],
                    "transparency": int(self.config['transparency'] * 255),
                    "rounded_corners": self.config['rounded_corners'],
                    "corner_radius": self.config['corner_radius'],
                    "background_spill": self.config['background_spill'],
                    "animation": self.config['animation']
                },
                "taskbar_styling": {
                    "enabled": True,
                    "icon_size": self.config['icon_size'],
                    "labels": self.config['labels'],
                    "spacing": self.config['spacing'],
                    "auto_hide": self.config['auto_hide']
                }
            }
        }
        
        try:
            # Save Windhawk configuration
            config_dir = Path.home() / '.windhawk'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'taskbar_floating.json'
            
            with open(config_file, 'w') as f:
                json.dump(windhawk_config, f, indent=4)
            
            print(f"[+] Windhawk configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error configuring Windhawk: {e}")
            return False
    
    def configure_translucenttb(self) -> bool:
        """Configure TranslucentTB for floating effect"""
        print(f"Configuring TranslucentTB for {self.name}...")
        
        # TranslucentTB configuration
        ttb_config = {
            "accentState": 3,  # Transparent
            "blurValue": 100,
            "opacity": int(self.config['transparency'] * 255),
            "noBorder": True,
            "smallTaskbar": False,
            "clearTaskbar": True
        }
        
        try:
            # Save TranslucentTB configuration
            config_dir = Path.home() / 'AppData' / 'Local' / 'TranslucentTB'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'config.json'
            
            with open(config_file, 'w') as f:
                json.dump(ttb_config, f, indent=4)
            
            print(f"[+] TranslucentTB configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error configuring TranslucentTB: {e}")
            return False
    
    def create_taskbar_script(self) -> bool:
        """Create PowerShell script for taskbar customization"""
        print(f"Creating taskbar customization script...")
        
        script_content = f'''
# Windows 12 Floating Taskbar Configuration Script
# Version: 2.0.0 - Next Valley Edition

param(
    [bool]$Floating = $True,
    [string]$Position = "{self.config['position']}",
    [int]$Transparency = {int(self.config['transparency'] * 255)},
    [bool]$RoundedCorners = $True,
    [int]$CornerRadius = {self.config['corner_radius']},
    [bool]$AutoHide = $False
)

# Apply taskbar settings via Windhawk CLI
if (Test-Path "$env:ProgramFiles\Windhawk\windhawk.exe") {{
    & "$env:ProgramFiles\Windhawk\windhawk.exe" --apply-mod "taskbar_floating"
    & "$env:ProgramFiles\Windhawk\windhawk.exe" --apply-mod "taskbar_styling"
}}

# Apply TranslucentTB settings
if (Test-Path "$env:LOCALAPPDATA\TranslucentTB\TranslucentTB.exe") {{
    Stop-Process -Name "TranslucentTB" -ErrorAction SilentlyContinue
    Start-Process -FilePath "$env:LOCALAPPDATA\TranslucentTB\TranslucentTB.exe"
}}

# Restart Windows Explorer to apply changes
Stop-Process -Name "explorer" -Force
Start-Process "explorer.exe"

Write-Host "Windows 12 Floating Taskbar configuration applied!" -ForegroundColor Green
'''
        
        try:
            scripts_dir = Path(__file__).parent.parent.parent / 'src' / 'scripts'
            scripts_dir.mkdir(parents=True, exist_ok=True)
            script_file = scripts_dir / 'configure_floating_taskbar.ps1'
            
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            print(f"[+] Taskbar script created: {script_file}")
            return True
        except Exception as e:
            print(f"[-] Error creating taskbar script: {e}")
            return False
    
    def install(self) -> bool:
        """Install the floating taskbar module"""
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
        
        # Step 3: Configure Windhawk
        if not self.configure_windhawk():
            print(f"[-] Failed to configure Windhawk")
            success = False
        
        # Step 4: Configure TranslucentTB
        if not self.configure_translucenttb():
            print(f"[-] Failed to configure TranslucentTB")
            success = False
        
        # Step 5: Create configuration script
        if not self.create_taskbar_script():
            print(f"[-] Failed to create configuration script")
            success = False
        
        if success:
            print(f"\n[+] {self.name} installed successfully!")
        else:
            print(f"\n[-] {self.name} installation completed with errors")
        
        return success
    
    def uninstall(self) -> bool:
        """Uninstall the floating taskbar module"""
        print(f"Uninstalling: {self.name}")
        
        try:
            # Remove Windhawk configuration
            config_file = Path.home() / '.windhawk' / 'taskbar_floating.json'
            if config_file.exists():
                config_file.unlink()
                print(f"[+] Removed Windhawk configuration")
            
            # Remove TranslucentTB configuration
            ttb_config = Path.home() / 'AppData' / 'Local' / 'TranslucentTB' / 'config.json'
            if ttb_config.exists():
                ttb_config.unlink()
                print(f"[+] Removed TranslucentTB configuration")
            
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
            # Remove custom taskbar settings
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'TaskbarGlomLevel')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'TaskbarSmallIcons')
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
            'windhawk_configured': False,
            'translucenttb_configured': False
        }
        
        # Check if configurations exist
        windhawk_config = Path.home() / '.windhawk' / 'taskbar_floating.json'
        ttb_config = Path.home() / 'AppData' / 'Local' / 'TranslucentTB' / 'config.json'
        
        status['windhawk_configured'] = windhawk_config.exists()
        status['translucenttb_configured'] = ttb_config.exists()
        
        return status


# Module interface
if __name__ == "__main__":
    module = FloatingTaskbarModule()
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        success = module.install()
        sys.exit(0 if success else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        success = module.uninstall()
        sys.exit(0 if success else 1)
    else:
        print(f"{module.get_name()} - {module.get_description()}")
        print("Usage: python taskbar.py [install|uninstall]")
