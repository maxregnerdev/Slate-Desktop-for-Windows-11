#!/usr/bin/env python3
"""
Top Widgets Module for Windows 12 UI Transformation
Version: 2.0.0 - Next Valley Edition

Implements the top-mounted widgets and notification system for Windows 12 UI.
"""

import json
import subprocess
import sys
import platform
from pathlib import Path
from typing import Dict, Any, Optional

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


class TopWidgetsModule:
    """
    Top Widgets Module
    
    Implements Windows 12 top-mounted widgets and notification system with:
    - Top-mounted widget bar
    - Copilot 2.0 integration
    - Search widget
    - Notification center
    - Modular widget system
    """
    
    def __init__(self):
        self.name = "Top Widgets System"
        self.description = "Windows 12 top-mounted widgets and notification center"
        self.version = "2.0.0"
        self.author = "Slate Desktop Team"
        self.dependencies = ['rainmeter', 'windhawk']
        
        # Configuration
        self.config = {
            'enabled': True,
            'top_widgets': True,
            'position': 'top',
            'height': 48,
            'transparency': 0.9,
            'rounded_corners': True,
            'corner_radius': 12,
            'auto_hide': False,
            'widgets': {
                'copilot': {
                    'enabled': True,
                    'position': 'left',
                    'width': 300,
                    'features': ['search', 'suggestions', 'voice']
                },
                'search': {
                    'enabled': True,
                    'position': 'center',
                    'width': 500,
                    'provider': 'bing',
                    'ai_suggestions': True
                },
                'notifications': {
                    'enabled': True,
                    'position': 'right',
                    'width': 250,
                    'show_badges': True
                }
            },
            'animation': True,
            'blur_effect': True
        }
        
        # Widget definitions
        self.widget_definitions = {
            'copilot': {
                'name': 'Copilot 2.0',
                'description': 'Microsoft Copilot 2.0 AI assistant',
                'type': 'ai',
                'icon': '🤖',
                'features': ['natural_language', 'code_assistance', 'web_search']
            },
            'search': {
                'name': 'Smart Search',
                'description': 'AI-powered search with context awareness',
                'type': 'search',
                'icon': '🔍',
                'features': ['context_search', 'suggestions', 'voice_search']
            },
            'notifications': {
                'name': 'Notification Center',
                'description': 'Unified notification center',
                'type': 'notifications',
                'icon': '🔔',
                'features': ['app_notifications', 'system_alerts', 'quick_actions']
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
            'winget install --id Rainmeter.Rainmeter',
            'winget install --id RamenSoftware.Windhawk'
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
        """Apply registry tweaks for top widgets"""
        print(f"Applying registry tweaks for {self.name}...")
        
        tweaks = [
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',
                'value': 'ShowTaskViewButton',
                'data': 0,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',
                'value': 'ShowSearchButton',
                'data': 0,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer',
                'value': 'DisableLocalMachine',
                'data': 1,
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
    
    def configure_windhawk_widgets(self) -> bool:
        """Configure Windhawk for top widgets"""
        print(f"Configuring Windhawk for {self.name}...")
        
        # Windhawk configuration for top widgets
        windhawk_config = {
            "mods": {
                "top_widgets": {
                    "enabled": True,
                    "position": self.config['position'],
                    "height": self.config['height'],
                    "transparency": int(self.config['transparency'] * 255),
                    "rounded_corners": self.config['rounded_corners'],
                    "corner_radius": self.config['corner_radius'],
                    "auto_hide": self.config['auto_hide'],
                    "blur_effect": self.config['blur_effect'],
                    "animation": self.config['animation'],
                    "widgets": self.config['widgets']
                },
                "widget_styling": {
                    "enabled": True,
                    "theme": "dark",
                    "accent_color": "#0078D4",
                    "font": "Segoe UI",
                    "font_size": 12
                }
            }
        }
        
        try:
            # Save Windhawk configuration
            config_dir = Path.home() / '.windhawk'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'top_widgets.json'
            
            with open(config_file, 'w') as f:
                json.dump(windhawk_config, f, indent=4)
            
            print(f"[+] Windhawk widgets configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error configuring Windhawk widgets: {e}")
            return False
    
    def create_rainmeter_widgets(self) -> bool:
        """Create Rainmeter skins for top widgets"""
        print(f"Creating Rainmeter widgets for {self.name}...")
        
        # Create Rainmeter skins directory
        rainmeter_skins = Path.home() / 'Documents' / 'Rainmeter' / 'Skins' / 'Windows12Widgets'
        rainmeter_skins.mkdir(parents=True, exist_ok=True)
        
        # Create widget skins
        widgets = [
            {
                'name': 'CopilotWidget',
                'content': self.create_copilot_skin()
            },
            {
                'name': 'SearchWidget',
                'content': self.create_search_skin()
            },
            {
                'name': 'NotificationsWidget',
                'content': self.create_notifications_skin()
            }
        ]
        
        created = 0
        for widget in widgets:
            try:
                widget_dir = rainmeter_skins / widget['name']
                widget_dir.mkdir(exist_ok=True)
                
                # Create skin files
                (widget_dir / f"{widget['name']}.ini").write_text(widget['content'])
                created += 1
            except Exception as e:
                print(f"[-] Error creating {widget['name']}: {e}")
        
        print(f"[+] Created {created} Rainmeter widget skins")
        return created > 0
    
    def create_copilot_skin(self) -> str:
        """Create Copilot 2.0 Rainmeter skin"""
        return """[Rainmeter]
Update=1000
DynamicWindowSize=1
AccurateText=1

[Metadata]
Name=Copilot 2.0 Widget
Author=Slate Desktop Team
Version=2.0.0
License=MIT

[Variables]
Font=Segoe UI
FontSize=12
Color=255,255,255
Background=0,0,0,200
Width=300
Height=48

[Window]
X=0
Y=0
W=#Width#
H=#Height#

[Background]
Meter=Shape
Shape=Rectangle 0,0,#Width#,#Height#,12 | Fill Color #Background# | Stroke Color 0,0,0,0

[CopilotIcon]
Meter=Image
ImageName=🤖
X=12
Y=12
W=24
H=24

[CopilotText]
Meter=String
Text=Copilot 2.0
X=48
Y=16
FontFace=#Font#
FontSize=#FontSize#
FontColor=#Color#
StringAlign=Left

[CopilotStatus]
Meter=String
Text=Ready
X=48
Y=32
FontFace=#Font#
FontSize=10
FontColor=100,200,255
StringAlign=Left

[CopilotClick]
Meter=String
Text=
X=0
Y=0
W=#Width#
H=#Height#
LeftMouseUpAction=[!CommandMeasure "CopilotMeasure" "Execute"]

[CopilotMeasure]
Measure=Plugin
Plugin=RunCommand
Parameter=powershell -Command "Start-Process ms-copilot:"
State=Hide
"""
    
    def create_search_skin(self) -> str:
        """Create Search widget Rainmeter skin"""
        return """[Rainmeter]
Update=1000
DynamicWindowSize=1
AccurateText=1

[Metadata]
Name=Smart Search Widget
Author=Slate Desktop Team
Version=2.0.0
License=MIT

[Variables]
Font=Segoe UI
FontSize=12
Color=255,255,255
Background=0,0,0,200
Width=500
Height=48

[Window]
X=0
Y=0
W=#Width#
H=#Height#

[Background]
Meter=Shape
Shape=Rectangle 0,0,#Width#,#Height#,12 | Fill Color #Background# | Stroke Color 0,0,0,0

[SearchIcon]
Meter=Image
ImageName=🔍
X=12
Y=12
W=24
H=24

[SearchText]
Meter=String
Text=Search with AI...
X=48
Y=16
FontFace=#Font#
FontSize=#FontSize#
FontColor=#Color#
StringAlign=Left

[SearchInput]
Meter=String
Text=
X=48
Y=12
W=#Width#-60
H=24
FontFace=#Font#
FontSize=#FontSize#
FontColor=#Color#
StringAlign=Left

[SearchClick]
Meter=String
Text=
X=0
Y=0
W=#Width#
H=#Height#
LeftMouseUpAction=[!CommandMeasure "SearchMeasure" "Execute"]

[SearchMeasure]
Measure=Plugin
Plugin=RunCommand
Parameter=powershell -Command "Start-Process ms-search:"
State=Hide
"""
    
    def create_notifications_skin(self) -> str:
        """Create Notifications widget Rainmeter skin"""
        return """[Rainmeter]
Update=1000
DynamicWindowSize=1
AccurateText=1

[Metadata]
Name=Notifications Widget
Author=Slate Desktop Team
Version=2.0.0
License=MIT

[Variables]
Font=Segoe UI
FontSize=12
Color=255,255,255
Background=0,0,0,200
Width=250
Height=48

[Window]
X=0
Y=0
W=#Width#
H=#Height#

[Background]
Meter=Shape
Shape=Rectangle 0,0,#Width#,#Height#,12 | Fill Color #Background# | Stroke Color 0,0,0,0

[NotificationsIcon]
Meter=Image
ImageName=🔔
X=12
Y=12
W=24
H=24

[NotificationsText]
Meter=String
Text=Notifications
X=48
Y=16
FontFace=#Font#
FontSize=#FontSize#
FontColor=#Color#
StringAlign=Left

[NotificationsCount]
Meter=String
Text=0
X=#Width#-48
Y=12
FontFace=#Font#
FontSize=14
FontColor=255,100,100
StringAlign=Right

[NotificationsClick]
Meter=String
Text=
X=0
Y=0
W=#Width#
H=#Height#
LeftMouseUpAction=[!CommandMeasure "NotificationsMeasure" "Execute"]

[NotificationsMeasure]
Measure=Plugin
Plugin=RunCommand
Parameter=powershell -Command "Start-Process ms-actioncenter:"
State=Hide
"""
    
    def configure_rainmeter(self) -> bool:
        """Configure Rainmeter for top widgets"""
        print(f"Configuring Rainmeter for {self.name}...")
        
        # Rainmeter configuration
        rainmeter_config = {
            "skin_path": str(Path.home() / 'Documents' / 'Rainmeter' / 'Skins' / 'Windows12Widgets'),
            "layouts": {
                "Windows12TopWidgets": {
                    "skins": [
                        {
                            "name": "CopilotWidget",
                            "x": 10,
                            "y": 10,
                            "width": 300,
                            "height": 48
                        },
                        {
                            "name": "SearchWidget",
                            "x": 320,
                            "y": 10,
                            "width": 500,
                            "height": 48
                        },
                        {
                            "name": "NotificationsWidget",
                            "x": 830,
                            "y": 10,
                            "width": 250,
                            "height": 48
                        }
                    ]
                }
            }
        }
        
        try:
            # Save Rainmeter configuration
            config_dir = Path.home() / 'Documents' / 'Rainmeter'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'Windows12Widgets.json'
            
            with open(config_file, 'w') as f:
                json.dump(rainmeter_config, f, indent=4)
            
            print(f"[+] Rainmeter configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error configuring Rainmeter: {e}")
            return False
    
    def create_widget_script(self) -> bool:
        """Create PowerShell script for widget management"""
        print(f"Creating widget management script...")
        
        script_content = f'''
# Windows 12 Top Widgets Management Script
# Version: 2.0.0 - Next Valley Edition

param(
    [bool]$Enable = $True,
    [string]$Position = "{self.config['position']}",
    [int]$Height = {self.config['height']},
    [int]$Transparency = {int(self.config['transparency'] * 255)},
    [bool]$RoundedCorners = $True,
    [int]$CornerRadius = {self.config['corner_radius']}
)

# Apply Windhawk widget mod
if (Test-Path "$env:ProgramFiles\Windhawk\windhawk.exe") {{
    & "$env:ProgramFiles\Windhawk\windhawk.exe" --apply-mod "top_widgets"
    & "$env:ProgramFiles\Windhawk\windhawk.exe" --apply-mod "widget_styling"
}}

# Start Rainmeter with Windows 12 widgets
if (Test-Path "$env:ProgramFiles\Rainmeter\Rainmeter.exe") {{
    Stop-Process -Name "Rainmeter" -ErrorAction SilentlyContinue
    Start-Process -FilePath "$env:ProgramFiles\Rainmeter\Rainmeter.exe"
}}

# Apply widget positioning
$layoutPath = "$env:USERPROFILE\Documents\Rainmeter\Windows12Widgets.json"
if (Test-Path $layoutPath) {{
    # Load and apply layout
    $layout = Get-Content $layoutPath | ConvertFrom-Json
    # Apply layout logic here
}}

Write-Host "Windows 12 Top Widgets configuration applied!" -ForegroundColor Green
'''
        
        try:
            scripts_dir = Path(__file__).parent.parent.parent / Path('src') / Path('scripts')
            scripts_dir.mkdir(parents=True, exist_ok=True)
            script_file = scripts_dir / Path('configure_top_widgets.ps1')
            
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            print(f"[+] Widget script created: {script_file}")
            return True
        except Exception as e:
            print(f"[-] Error creating widget script: {e}")
            return False
    
    def install(self) -> bool:
        """Install the top widgets module"""
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
        if not self.configure_windhawk_widgets():
            print(f"[-] Failed to configure Windhawk")
            success = False
        
        # Step 4: Create Rainmeter widgets
        if not self.create_rainmeter_widgets():
            print(f"[-] Failed to create Rainmeter widgets")
            success = False
        
        # Step 5: Configure Rainmeter
        if not self.configure_rainmeter():
            print(f"[-] Failed to configure Rainmeter")
            success = False
        
        # Step 6: Create configuration script
        if not self.create_widget_script():
            print(f"[-] Failed to create configuration script")
            success = False
        
        if success:
            print(f"\n[+] {self.name} installed successfully!")
        else:
            print(f"\n[-] {self.name} installation completed with errors")
        
        return success
    
    def uninstall(self) -> bool:
        """Uninstall the top widgets module"""
        print(f"Uninstalling: {self.name}")
        
        try:
            # Remove Windhawk configuration
            config_file = Path.home() / '.windhawk' / 'top_widgets.json'
            if config_file.exists():
                config_file.unlink()
                print(f"[+] Removed Windhawk widgets configuration")
            
            # Remove Rainmeter skins
            rainmeter_skins = Path.home() / 'Documents' / 'Rainmeter' / 'Skins' / 'Windows12Widgets'
            if rainmeter_skins.exists():
                import shutil
                shutil.rmtree(rainmeter_skins)
                print(f"[+] Removed Rainmeter widgets")
            
            # Remove Rainmeter configuration
            rm_config = Path.home() / 'Documents' / 'Rainmeter' / 'Windows12Widgets.json'
            if rm_config.exists():
                rm_config.unlink()
                print(f"[+] Removed Rainmeter configuration")
            
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
            # Reset Explorer settings
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'ShowTaskViewButton')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'ShowSearchButton')
                except:
                    pass
            
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Software\Microsoft\Windows\CurrentVersion\Explorer', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'DisableLocalMachine')
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
            'rainmeter_configured': False
        }
        
        # Check if configurations exist
        windhawk_config = Path.home() / '.windhawk' / 'top_widgets.json'
        rainmeter_config = Path.home() / 'Documents' / 'Rainmeter' / 'Windows12Widgets.json'
        
        status['windhawk_configured'] = windhawk_config.exists()
        status['rainmeter_configured'] = rainmeter_config.exists()
        
        return status


# Module interface
if __name__ == "__main__":
    module = TopWidgetsModule()
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        success = module.install()
        sys.exit(0 if success else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        success = module.uninstall()
        sys.exit(0 if success else 1)
    else:
        print(f"{module.get_name()} - {module.get_description()}")
        print("Usage: python widgets.py [install|uninstall]")
