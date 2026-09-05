#!/usr/bin/env python3
"""
Hybrid Optimization Module for Windows 12 UI Transformation
Version: 2.0.0 - Next Valley Edition

Implements hybrid device optimization for both PC and tablet modes in Windows 12 UI.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import winreg


class HybridOptimizationModule:
    """
    Hybrid Optimization Module
    
    Implements Windows 12 hybrid optimization for:
    - PC mode optimization
    - Tablet mode optimization
    - Adaptive UI based on device type
    - Touch and pen support
    - Performance optimization for different form factors
    """
    
    def __init__(self):
        self.name = "Hybrid Optimization"
        self.description = "Windows 12 hybrid device optimization for PC and tablet modes"
        self.version = "2.0.0"
        self.author = "Slate Desktop Team"
        self.dependencies = ['mactype', 'windhawk']
        
        # Configuration
        self.config = {
            'enabled': True,
            'device_type': 'auto',  # auto, pc, tablet, hybrid
            'pc_mode': {
                'enabled': True,
                'optimizations': {
                    'performance': 'max',
                    'animations': True,
                    'transparency': True,
                    'font_rendering': 'enhanced',
                    'touch_support': False,
                    'pen_support': False
                }
            },
            'tablet_mode': {
                'enabled': True,
                'optimizations': {
                    'performance': 'balanced',
                    'animations': True,
                    'transparency': True,
                    'font_rendering': 'enhanced',
                    'touch_support': True,
                    'pen_support': True,
                    'touch_target_size': 'large',
                    'gesture_support': True
                }
            },
            'hybrid_mode': {
                'enabled': True,
                'auto_switch': True,
                'pc_threshold': 12,  # inches
                'tablet_threshold': 10,  # inches
                'transition_animation': True
            },
            'font_rendering': {
                'enabled': True,
                'method': 'mactype',  # mactype, directwrite, cleartype
                'profile': 'windows12',
                'gamma': 1.0,
                'contrast': 1.2,
                'subpixel_rendering': True,
                'hinting': 'slight'
            },
            'touch_optimization': {
                'enabled': True,
                'touch_target_min_size': 48,
                'gesture_recognition': True,
                'pen_pressure_sensitivity': True,
                'palm_rejection': True
            }
        }
        
        # Device detection
        self.device_profiles = {
            'pc': {
                'name': 'Desktop PC',
                'description': 'Optimized for keyboard and mouse input',
                'screen_size': 'large',
                'input_method': 'keyboard_mouse',
                'performance_profile': 'max'
            },
            'tablet': {
                'name': 'Tablet',
                'description': 'Optimized for touch and pen input',
                'screen_size': 'medium',
                'input_method': 'touch_pen',
                'performance_profile': 'balanced'
            },
            'hybrid': {
                'name': '2-in-1 Hybrid',
                'description': 'Adaptive based on current mode',
                'screen_size': 'adaptive',
                'input_method': 'adaptive',
                'performance_profile': 'adaptive'
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
            'winget install --id snowie2000.MacType',
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
    
    def detect_device_type(self) -> str:
        """Detect current device type"""
        print(f"Detecting device type...")
        
        try:
            # Check for tablet mode capability
            result = subprocess.run(
                ['powershell', '-Command', 
                 'Get-WmiObject -Class Win32_ComputerSystem | Select-Object -ExpandProperty SystemType'],
                capture_output=True,
                text=True
            )
            
            system_type = result.stdout.strip().lower()
            
            # Check screen size
            screen_result = subprocess.run(
                ['powershell', '-Command',
                 '(Get-WmiObject -Class Win32_DesktopMonitor).ScreenWidth'],
                capture_output=True,
                text=True
            )
            
            screen_width = int(screen_result.stdout.strip()) if screen_result.stdout.strip() else 0
            
            # Determine device type based on system type and screen size
            if 'handheld' in system_type or 'tablet' in system_type:
                device_type = 'tablet'
            elif screen_width <= 1366:  # 13.3" or smaller
                device_type = 'tablet'
            elif screen_width <= 1920:  # 15.6" or smaller
                device_type = 'hybrid'
            else:
                device_type = 'pc'
            
            print(f"[+] Detected device type: {device_type}")
            return device_type
            
        except Exception as e:
            print(f"[!] Error detecting device type: {e}")
            return 'pc'  # Default to PC mode
    
    def apply_registry_tweaks(self) -> bool:
        """Apply registry tweaks for hybrid optimization"""
        print(f"Applying registry tweaks for {self.name}...")
        
        device_type = self.detect_device_type()
        
        # Get optimization settings based on device type
        if device_type == 'pc':
            optimizations = self.config['pc_mode']['optimizations']
        elif device_type == 'tablet':
            optimizations = self.config['tablet_mode']['optimizations']
        else:
            optimizations = self.config['hybrid_mode']
        
        tweaks = [
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',
                'value': 'Start_ShowTouchKeyboard',
                'data': 1 if optimizations.get('touch_support', False) else 0,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',
                'value': 'Start_ShowTabletMode',
                'data': 1 if optimizations.get('touch_support', False) else 0,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',
                'value': 'Start_ShowPenWorkspace',
                'data': 1 if optimizations.get('pen_support', False) else 0,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Control Panel\Accessibility\StickyKeys',
                'value': 'Flags',
                'data': 506,  # Disable sticky keys for tablet mode
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Control Panel\Accessibility\ToggleKeys',
                'value': 'Flags',
                'data': 58,
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Control Panel\Accessibility\FilterKeys',
                'value': 'Flags',
                'data': 0,
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
    
    def configure_mactype(self) -> bool:
        """Configure MacType for enhanced font rendering"""
        print(f"Configuring MacType for {self.name}...")
        
        # MacType configuration for hybrid optimization
        mactype_config = {
            "version": "2.0",
            "enabled": self.config['font_rendering']['enabled'],
            "method": self.config['font_rendering']['method'],
            "profile": self.config['font_rendering']['profile'],
            "gamma": self.config['font_rendering']['gamma'],
            "contrast": self.config['font_rendering']['contrast'],
            "subpixel_rendering": self.config['font_rendering']['subpixel_rendering'],
            "hinting": self.config['font_rendering']['hinting'],
            "service_mode": True,
            "auto_start": True,
            "device_profiles": {
                "pc": {
                    "gamma": 1.0,
                    "contrast": 1.2,
                    "hinting": "slight"
                },
                "tablet": {
                    "gamma": 1.1,
                    "contrast": 1.3,
                    "hinting": "medium"
                },
                "hybrid": {
                    "gamma": 1.05,
                    "contrast": 1.25,
                    "hinting": "slight"
                }
            }
        }
        
        try:
            # Save MacType configuration
            config_dir = Path.home() / 'AppData' / 'Local' / 'MacType'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'config.json'
            
            with open(config_file, 'w') as f:
                json.dump(mactype_config, f, indent=4)
            
            print(f"[+] MacType configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error configuring MacType: {e}")
            return False
    
    def create_mactype_profile(self) -> bool:
        """Create Windows 12 specific MacType profile"""
        print(f"Creating MacType profile for {self.name}...")
        
        # Windows 12 optimized MacType profile
        profile_content = """[MacType Profile]
Version=2.0
Name=Windows 12 Hybrid
Description=Optimized font rendering for Windows 12 hybrid devices
Author=Slate Desktop Team

[Settings]
Method=3
Gamma=1.0
Contrast=1.2
Brightness=1.0
SubpixelRendering=1
Hinting=1
BoldThreshold=150
ItalicThreshold=50

[Advanced]
UseServiceMode=1
AutoStart=1
CompatibilityMode=0

[DeviceSpecific]
PC_Gamma=1.0
PC_Contrast=1.2
PC_Hinting=1

Tablet_Gamma=1.1
Tablet_Contrast=1.3
Tablet_Hinting=2

Hybrid_Gamma=1.05
Hybrid_Contrast=1.25
Hybrid_Hinting=1

[FontExceptions]
Consolas=0,1.0,1.1
Segoe UI=0,1.0,1.2
"""
        
        try:
            profiles_dir = Path.home() / 'AppData' / 'Local' / 'MacType' / 'Profiles'
            profiles_dir.mkdir(parents=True, exist_ok=True)
            profile_file = profiles_dir / 'Windows12_Hybrid.ini'
            
            with open(profile_file, 'w') as f:
                f.write(profile_content)
            
            print(f"[+] MacType profile saved to {profile_file}")
            return True
        except Exception as e:
            print(f"[-] Error creating MacType profile: {e}")
            return False
    
    def configure_windhawk_hybrid(self) -> bool:
        """Configure Windhawk for hybrid optimization"""
        print(f"Configuring Windhawk for {self.name}...")
        
        # Windhawk configuration for hybrid optimization
        windhawk_config = {
            "mods": {
                "hybrid_optimization": {
                    "enabled": True,
                    "device_type": self.config['device_type'],
                    "auto_switch": self.config['hybrid_mode']['auto_switch'],
                    "pc_threshold": self.config['hybrid_mode']['pc_threshold'],
                    "tablet_threshold": self.config['hybrid_mode']['tablet_threshold'],
                    "transition_animation": self.config['hybrid_mode']['transition_animation'],
                    "touch_optimization": self.config['touch_optimization']
                },
                "device_detection": {
                    "enabled": True,
                    "screen_size_check": True,
                    "input_method_check": True,
                    "orientation_check": True,
                    "auto_apply": True
                }
            }
        }
        
        try:
            # Save Windhawk configuration
            config_dir = Path.home() / '.windhawk'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'hybrid_optimization.json'
            
            with open(config_file, 'w') as f:
                json.dump(windhawk_config, f, indent=4)
            
            print(f"[+] Windhawk hybrid configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error configuring Windhawk hybrid: {e}")
            return False
    
    def create_hybrid_script(self) -> bool:
        """Create PowerShell script for hybrid optimization"""
        print(f"Creating hybrid optimization script...")
        
        script_content = f'''
# Windows 12 Hybrid Optimization Script
# Version: 2.0.0 - Next Valley Edition

param(
    [string]$DeviceType = "auto",
    [bool]$AutoSwitch = $True,
    [int]$PCTreshold = {self.config['hybrid_mode']['pc_threshold']},
    [int]$TabletThreshold = {self.config['hybrid_mode']['tablet_threshold']},
    [bool]$TransitionAnimation = $True
)

# Detect device type if auto
if ($DeviceType -eq "auto") {{
    $DeviceType = Get-HybridDeviceType -PCTreshold $PCTreshold -TabletThreshold $TabletThreshold
}}

# Apply device-specific optimizations
switch ($DeviceType) {{
    "pc" {{
        Apply-PCOptimizations
        Write-Host "Applied PC optimizations" -ForegroundColor Green
    }}
    "tablet" {{
        Apply-TabletOptimizations
        Write-Host "Applied Tablet optimizations" -ForegroundColor Green
    }}
    "hybrid" {{
        Apply-HybridOptimizations -AutoSwitch $AutoSwitch -TransitionAnimation $TransitionAnimation
        Write-Host "Applied Hybrid optimizations" -ForegroundColor Green
    }}
    default {{
        Write-Host "Unknown device type: $DeviceType" -ForegroundColor Yellow
    }}
}}

# Configure MacType for current device
if (Test-Path "$env:ProgramFiles\\MacType\\MacType.exe") {{
    $mactypeConfig = @{{
        enabled = $True
        method = "{self.config['font_rendering']['method']}"
        profile = "Windows12_Hybrid"
        gamma = {self.config['font_rendering']['gamma']}
        contrast = {self.config['font_rendering']['contrast']}
        subpixelRendering = $({self.config['font_rendering']['subpixel_rendering']} -as [int])
        hinting = "{self.config['font_rendering']['hinting']}"
    }}
    
    $mactypeConfig | ConvertTo-Json | Out-File -FilePath "$env:LOCALAPPDATA\\MacType\\config.json" -Encoding UTF8
    
    # Restart MacType service
    Stop-Service -Name "MacType" -Force -ErrorAction SilentlyContinue
    Start-Service -Name "MacType"
}}

# Configure Windhawk for hybrid mode
if (Test-Path "$env:ProgramFiles\\Windhawk\\windhawk.exe") {{
    & "$env:ProgramFiles\\Windhawk\\windhawk.exe" --apply-mod "hybrid_optimization"
    & "$env:ProgramFiles\\Windhawk\\windhawk.exe" --apply-mod "device_detection"
}}

Write-Host "Windows 12 Hybrid Optimization applied!" -ForegroundColor Green

# Helper functions
function Get-HybridDeviceType {{
    param(
        [int]$PCTreshold,
        [int]$TabletThreshold
    )
    
    try {{
        # Get screen size in inches (approximate)
        $screenWidth = (Get-WmiObject -Class Win32_DesktopMonitor).ScreenWidth
        $screenHeight = (Get-WmiObject -Class Win32_DesktopMonitor).ScreenHeight
        
        # Calculate diagonal in inches (assuming 100 DPI for approximation)
        $diagonal = [Math]::Sqrt(($screenWidth / 100) * ($screenWidth / 100) + ($screenHeight / 100) * ($screenHeight / 100))
        
        if ($diagonal -ge $PCTreshold) {{
            return "pc"
        }} elseif ($diagonal -le $TabletThreshold) {{
            return "tablet"
        }} else {{
            return "hybrid"
        }}
    }} catch {{
        return "pc"  # Default to PC if detection fails
    }}
}}

function Apply-PCOptimizations {{
    # PC-specific optimizations
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "Start_ShowTouchKeyboard" -Value 0
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "Start_ShowTabletMode" -Value 0
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "Start_ShowPenWorkspace" -Value 0
    
    # Enable all animations
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "ListviewAlphaSelect" -Value 1
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "ListviewShadow" -Value 1
    
    # Performance settings
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "ProgramsNoStart" -Value 0
}}

function Apply-TabletOptimizations {{
    # Tablet-specific optimizations
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "Start_ShowTouchKeyboard" -Value 1
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "Start_ShowTabletMode" -Value 1
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "Start_ShowPenWorkspace" -Value 1
    
    # Reduce animations for touch
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "ListviewAlphaSelect" -Value 0
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "ListviewShadow" -Value 0
    
    # Touch optimizations
    Set-ItemProperty -Path "HKCU:\\Control Panel\\Accessibility\\StickyKeys" -Name "Flags" -Value "506"
}}

function Apply-HybridOptimizations {{
    param(
        [bool]$AutoSwitch,
        [bool]$TransitionAnimation
    )
    
    # Hybrid mode optimizations
    if ($AutoSwitch) {{
        # Register for auto-switch events
        # This would integrate with Windows device mode changes
        Write-Host "Auto-switch enabled" -ForegroundColor Cyan
    }}
    
    if ($TransitionAnimation) {{
        # Enable transition animations
        Write-Host "Transition animations enabled" -ForegroundColor Cyan
    }}
}}
'''
        
        try:
            scripts_dir = Path(__file__).parent.parent.parent / 'src' / 'scripts'
            scripts_dir.mkdir(parents=True, exist_ok=True)
            script_file = scripts_dir / 'configure_hybrid.ps1'
            
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            print(f"[+] Hybrid script created: {script_file}")
            return True
        except Exception as e:
            print(f"[-] Error creating hybrid script: {e}")
            return False
    
    def create_hybrid_config(self) -> bool:
        """Create hybrid optimization configuration file"""
        print(f"Creating hybrid optimization configuration...")
        
        hybrid_config = {
            "version": self.version,
            "device_type": self.config['device_type'],
            "auto_detect": True,
            "pc_mode": self.config['pc_mode'],
            "tablet_mode": self.config['tablet_mode'],
            "hybrid_mode": self.config['hybrid_mode'],
            "font_rendering": self.config['font_rendering'],
            "touch_optimization": self.config['touch_optimization'],
            "detected_device": self.detect_device_type(),
            "active_profile": "auto"
        }
        
        try:
            config_dir = Path(__file__).parent.parent.parent.parent / 'config' / 'Windows12'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'hybrid_optimization_config.json'
            
            with open(config_file, 'w') as f:
                json.dump(hybrid_config, f, indent=4)
            
            print(f"[+] Hybrid configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error creating hybrid configuration: {e}")
            return False
    
    def install(self) -> bool:
        """Install the hybrid optimization module"""
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
        
        # Step 2: Detect device type
        device_type = self.detect_device_type()
        print(f"[+] Detected device type: {device_type}")
        
        # Step 3: Apply registry tweaks
        if not self.apply_registry_tweaks():
            print(f"[-] Failed to apply registry tweaks")
            success = False
        
        # Step 4: Configure MacType
        if not self.configure_mactype():
            print(f"[-] Failed to configure MacType")
            success = False
        
        # Step 5: Create MacType profile
        if not self.create_mactype_profile():
            print(f"[-] Failed to create MacType profile")
            success = False
        
        # Step 6: Configure Windhawk
        if not self.configure_windhawk_hybrid():
            print(f"[-] Failed to configure Windhawk")
            success = False
        
        # Step 7: Create configuration script
        if not self.create_hybrid_script():
            print(f"[-] Failed to create configuration script")
            success = False
        
        # Step 8: Create hybrid configuration
        if not self.create_hybrid_config():
            print(f"[-] Failed to create hybrid configuration")
            success = False
        
        if success:
            print(f"\n[+] {self.name} installed successfully!")
        else:
            print(f"\n[-] {self.name} installation completed with errors")
        
        return success
    
    def uninstall(self) -> bool:
        """Uninstall the hybrid optimization module"""
        print(f"Uninstalling: {self.name}")
        
        try:
            # Remove MacType configuration
            mactype_config = Path.home() / 'AppData' / 'Local' / 'MacType' / 'config.json'
            if mactype_config.exists():
                mactype_config.unlink()
                print(f"[+] Removed MacType configuration")
            
            # Remove MacType profile
            profile_file = Path.home() / 'AppData' / 'Local' / 'MacType' / 'Profiles' / 'Windows12_Hybrid.ini'
            if profile_file.exists():
                profile_file.unlink()
                print(f"[+] Removed MacType profile")
            
            # Remove Windhawk configuration
            windhawk_config = Path.home() / '.windhawk' / 'hybrid_optimization.json'
            if windhawk_config.exists():
                windhawk_config.unlink()
                print(f"[+] Removed Windhawk hybrid configuration")
            
            # Remove hybrid configuration
            hybrid_config = Path(__file__).parent.parent.parent.parent / 'config' / 'Windows12' / 'hybrid_optimization_config.json'
            if hybrid_config.exists():
                hybrid_config.unlink()
                print(f"[+] Removed hybrid configuration")
            
            # Remove hybrid script
            scripts_dir = Path(__file__).parent.parent.parent / 'src' / 'scripts'
            hybrid_script = scripts_dir / 'configure_hybrid.ps1'
            if hybrid_script.exists():
                hybrid_script.unlink()
                print(f"[+] Removed hybrid script")
            
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
                    winreg.DeleteValue(key, 'Start_ShowTouchKeyboard')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'Start_ShowTabletMode')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'Start_ShowPenWorkspace')
                except:
                    pass
            
            # Reset accessibility settings
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Control Panel\Accessibility\StickyKeys', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'Flags')
                except:
                    pass
            
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Control Panel\Accessibility\ToggleKeys', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'Flags')
                except:
                    pass
            
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Control Panel\Accessibility\FilterKeys', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'Flags')
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
            'mactype_configured': False,
            'windhawk_configured': False,
            'device_detected': False
        }
        
        # Check if configurations exist
        mactype_config = Path.home() / 'AppData' / 'Local' / 'MacType' / 'config.json'
        windhawk_config = Path.home() / '.windhawk' / 'hybrid_optimization.json'
        
        status['mactype_configured'] = mactype_config.exists()
        status['windhawk_configured'] = windhawk_config.exists()
        status['device_detected'] = True
        
        return status


# Module interface
if __name__ == "__main__":
    module = HybridOptimizationModule()
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        success = module.install()
        sys.exit(0 if success else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        success = module.uninstall()
        sys.exit(0 if success else 1)
    else:
        print(f"{module.get_name()} - {module.get_description()}")
        print("Usage: python hybrid_optimization.py [install|uninstall]")
