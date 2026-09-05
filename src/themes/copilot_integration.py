#!/usr/bin/env python3
"""
Copilot 2.0 Integration Module for Windows 12 UI Transformation
Version: 2.0.0 - Next Valley Edition

Implements comprehensive Copilot 2.0 integration for Windows 12 UI.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import winreg


class Copilot2IntegrationModule:
    """
    Copilot 2.0 Integration Module
    
    Implements Windows 12 Copilot 2.0 integration including:
    - Deep integration with taskbar and widgets
    - AI-powered search and suggestions
    - Context-aware assistance
    - Voice control integration
    """
    
    def __init__(self):
        self.name = "Copilot 2.0 Integration"
        self.description = "Comprehensive Copilot 2.0 integration for Windows 12 UI"
        self.version = "2.0.0"
        self.author = "Slate Desktop Team"
        self.dependencies = ['powertoys', 'copilot']
        
        # Configuration
        self.config = {
            'enabled': True,
            'copilot_2_enabled': True,
            'integration_points': {
                'taskbar': {
                    'enabled': True,
                    'position': 'left',
                    'width': 300,
                    'auto_show': True,
                    'hotkey': 'Win+C'
                },
                'widgets': {
                    'enabled': True,
                    'size': 'medium',
                    'features': ['search', 'suggestions', 'quick_actions']
                },
                'file_explorer': {
                    'enabled': True,
                    'context_menu': True,
                    'sidebar': True,
                    'quick_actions': ['summarize', 'explain', 'search']
                },
                'start_menu': {
                    'enabled': True,
                    'search_integration': True,
                    'voice_search': False
                },
                'settings': {
                    'enabled': True,
                    'ai_suggestions': True,
                    'automated_troubleshooting': True
                }
            },
            'ai_features': {
                'smart_suggestions': True,
                'context_aware_search': True,
                'natural_language_processing': True,
                'code_assistance': True,
                'image_understanding': True,
                'voice_control': False
            },
            'privacy': {
                'data_collection': False,
                'personalization': True,
                'history': True,
                'local_processing': False
            },
            'performance': {
                'model': 'gpt-4',
                'fallback_model': 'gpt-3.5',
                'local_model': False,
                'max_tokens': 4096,
                'temperature': 0.7
            }
        }
        
        # Copilot 2.0 capabilities
        self.copilot_capabilities = {
            'search': {
                'description': 'AI-powered search with context awareness',
                'features': ['semantic_search', 'context_understanding', 'personalized_results']
            },
            'suggestions': {
                'description': 'Smart suggestions based on current context',
                'features': ['text_suggestions', 'action_suggestions', 'proactive_help']
            },
            'code_assistance': {
                'description': 'AI-powered code assistance',
                'features': ['code_completion', 'code_explanation', 'debugging_help']
            },
            'image_understanding': {
                'description': 'Visual understanding and analysis',
                'features': ['image_description', 'object_recognition', 'visual_search']
            },
            'voice_control': {
                'description': 'Voice commands and dictation',
                'features': ['voice_commands', 'dictation', 'voice_search']
            },
            'automation': {
                'description': 'AI-powered automation',
                'features': ['task_automation', 'workflow_optimization', 'smart_actions']
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
                if dep == 'copilot':
                    # Check for Copilot via winget or direct path
                    result = subprocess.run(
                        ['powershell', '-Command', 'Get-AppxPackage -Name *Copilot*'],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        missing_deps.append(dep)
                else:
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
            'winget install --id Microsoft.PowerToys',
            'winget install --id Microsoft.Copilot'
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
        """Apply registry tweaks for Copilot 2.0 integration"""
        print(f"Applying registry tweaks for {self.name}...")
        
        tweaks = [
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Copilot',
                'value': 'Enabled',
                'data': 1,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Copilot',
                'value': 'AutoLaunch',
                'data': 1,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Copilot',
                'value': 'Hotkey',
                'data': self.config['integration_points']['taskbar']['hotkey'],
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Copilot',
                'value': 'Position',
                'data': self.config['integration_points']['taskbar']['position'],
                'type': winreg.REG_SZ
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',
                'value': 'Start_ShowSearch',
                'data': 1,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\AI',
                'value': 'Enabled',
                'data': 1,
                'type': winreg.REG_DWORD
            },
            {
                'path': r'HKCU\Software\Microsoft\Windows\CurrentVersion\AI',
                'value': 'CopilotEnabled',
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
    
    def configure_copilot_integration(self) -> bool:
        """Configure comprehensive Copilot 2.0 integration"""
        print(f"Configuring Copilot 2.0 integration for {self.name}...")
        
        # Main Copilot configuration
        copilot_config = {
            "version": "2.0",
            "enabled": self.config['copilot_2_enabled'],
            "integration_points": self.config['integration_points'],
            "ai_features": self.config['ai_features'],
            "privacy": self.config['privacy'],
            "performance": self.config['performance'],
            "capabilities": self.copilot_capabilities,
            "ui_settings": {
                "theme": "dark",
                "transparency": 0.9,
                "animation": True,
                "position": self.config['integration_points']['taskbar']['position'],
                "size": self.config['integration_points']['widgets']['size']
            }
        }
        
        try:
            # Save Copilot configuration
            config_dir = Path.home() / 'AppData' / 'Local' / 'Microsoft' / 'Copilot'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'windows12_config.json'
            
            with open(config_file, 'w') as f:
                json.dump(copilot_config, f, indent=4)
            
            print(f"[+] Copilot 2.0 integration configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error configuring Copilot 2.0 integration: {e}")
            return False
    
    def configure_powertoys_copilot(self) -> bool:
        """Configure PowerToys for Copilot 2.0 integration"""
        print(f"Configuring PowerToys for {self.name}...")
        
        # PowerToys Copilot configuration
        pt_config = {
            "powertoys": {
                "copilot_integration": {
                    "enabled": True,
                    "hotkey": self.config['integration_points']['taskbar']['hotkey'],
                    "position": self.config['integration_points']['taskbar']['position'],
                    "auto_show": self.config['integration_points']['taskbar']['auto_show'],
                    "features": {
                        "quick_launch": True,
                        "search_integration": True,
                        "ai_suggestions": True,
                        "context_menu": True
                    }
                },
                "ai_features": {
                    "text_extractor": {
                        "enabled": True,
                        "hotkey": "Win+Shift+T",
                        "ai_analysis": True
                    },
                    "powertoys_run": {
                        "enabled": True,
                        "ai_suggestions": True,
                        "hotkey": "Alt+Space"
                    }
                }
            }
        }
        
        try:
            # Save PowerToys configuration
            config_dir = Path.home() / 'AppData' / 'Local' / 'Microsoft' / 'PowerToys'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'copilot_config.json'
            
            with open(config_file, 'w') as f:
                json.dump(pt_config, f, indent=4)
            
            print(f"[+] PowerToys Copilot configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error configuring PowerToys Copilot: {e}")
            return False
    
    def create_copilot_scripts(self) -> bool:
        """Create Copilot 2.0 related scripts"""
        print(f"Creating Copilot 2.0 scripts for {self.name}...")
        
        scripts = [
            {
                'name': 'enable_copilot_integration.ps1',
                'content': self.create_copilot_integration_script()
            },
            {
                'name': 'configure_copilot_features.ps1',
                'content': self.create_copilot_features_script()
            },
            {
                'name': 'start_copilot_service.ps1',
                'content': self.create_copilot_service_script()
            }
        ]
        
        created = 0
        try:
            scripts_dir = Path(__file__).parent.parent.parent / r'src' / r'scripts'
            scripts_dir.mkdir(parents=True, exist_ok=True)
            
            for script in scripts:
                script_file = scripts_dir / script['name']
                with open(script_file, 'w') as f:
                    f.write(script['content'])
                created += 1
                print(f"[+] Created script: {script_file}")
            
            return created > 0
        except Exception as e:
            print(f"[-] Error creating Copilot scripts: {e}")
            return False
    
    def create_copilot_integration_script(self) -> str:
        """Create Copilot 2.0 integration script"""
        return '''# Windows 12 Copilot 2.0 Integration Script
# Version: 2.0.0 - Next Valley Edition

param(
    [bool]$Enable = $True,
    [string]$Position = "left",
    [int]$Width = 300,
    [string]$Hotkey = "Win+C",
    [bool]$AutoShow = $True
)

# Enable Copilot 2.0 integration
if ($Enable) {
    # Register Copilot URI scheme
    $regContent = @"
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\ms-copilot]
@="URL:Copilot Protocol"
"URL Protocol"=""

[HKEY_CLASSES_ROOT\ms-copilot\DefaultIcon]
@="\"C:\\Program Files\\WindowsApps\\Microsoft.Copilot_1.0.0.0_x64__8wekyb3d8bbwe\\Copilot.exe\",0"

[HKEY_CLASSES_ROOT\ms-copilot\shell]

[HKEY_CLASSES_ROOT\ms-copilot\shell\open]

[HKEY_CLASSES_ROOT\ms-copilot\shell\open\command]
@="\"C:\\Program Files\\WindowsApps\\Microsoft.Copilot_1.0.0.0_x64__8wekyb3d8bbwe\\Copilot.exe\" \"%1\""
"@
    
    $regPath = "$env:TEMP\\copilot_integration.reg"
    $regContent | Out-File -FilePath $regPath -Encoding ASCII
    
    # Apply registry
    Start-Process -FilePath "reg" -ArgumentList "import", $regPath -Wait
    Remove-Item -Path $regPath -Force
    
    # Configure Copilot integration settings
    $copilotConfig = @{
        Enabled = $True
        Position = $Position
        Width = $Width
        Hotkey = $Hotkey
        AutoShow = $AutoShow
        IntegrationPoints = @(
            "taskbar",
            "widgets", 
            "file_explorer",
            "start_menu",
            "settings"
        )
    }
    
    $configPath = "$env:LOCALAPPDATA\\Microsoft\\Copilot\\integration_config.json"
    $copilotConfig | ConvertTo-Json | Out-File -FilePath $configPath -Encoding UTF8
    
    # Enable Windows AI features
    $aiReg = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\AI"
    New-Item -Path $aiReg -Force | Out-Null
    Set-ItemProperty -Path $aiReg -Name "Enabled" -Value 1
    Set-ItemProperty -Path $aiReg -Name "CopilotEnabled" -Value 1
    
    # Launch Copilot
    Start-Process -FilePath "ms-copilot:"
    
    Write-Host "Copilot 2.0 Integration enabled!" -ForegroundColor Green
} else {
    # Disable Copilot integration
    Stop-Process -Name "Copilot" -ErrorAction SilentlyContinue
    
    $copilotConfig = @{
        Enabled = $False
    }
    
    $configPath = "$env:LOCALAPPDATA\\Microsoft\\Copilot\\integration_config.json"
    $copilotConfig | ConvertTo-Json | Out-File -FilePath $configPath -Encoding UTF8
    
    Write-Host "Copilot 2.0 Integration disabled!" -ForegroundColor Yellow
}
'''
    
    def create_copilot_features_script(self) -> str:
        """Create Copilot 2.0 features configuration script"""
        return '''# Windows 12 Copilot 2.0 Features Configuration Script
# Version: 2.0.0 - Next Valley Edition

param(
    [bool]$SmartSuggestions = $True,
    [bool]$ContextAwareSearch = $True,
    [bool]$NaturalLanguageProcessing = $True,
    [bool]$CodeAssistance = $True,
    [bool]$ImageUnderstanding = $True,
    [bool]$VoiceControl = $False
)

# Configure Copilot 2.0 features
$featuresConfig = @{
    SmartSuggestions = $SmartSuggestions
    ContextAwareSearch = $ContextAwareSearch
    NaturalLanguageProcessing = $NaturalLanguageProcessing
    CodeAssistance = $CodeAssistance
    ImageUnderstanding = $ImageUnderstanding
    VoiceControl = $VoiceControl
}

# Apply features configuration
$configPath = "$env:LOCALAPPDATA\\Microsoft\\Copilot\\features_config.json"
$featuresConfig | ConvertTo-Json | Out-File -FilePath $configPath -Encoding UTF8

# Enable AI features in Windows
$aiFeaturesReg = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\AI\\Features"
New-Item -Path $aiFeaturesReg -Force | Out-Null

$featuresConfig.GetEnumerator() | ForEach-Object {
    Set-ItemProperty -Path $aiFeaturesReg -Name $_.Key -Value ($_.Value -as [int])
}

Write-Host "Copilot 2.0 Features configured!" -ForegroundColor Green
'''
    
    def create_copilot_service_script(self) -> str:
        """Create Copilot 2.0 service management script"""
        return '''# Windows 12 Copilot 2.0 Service Management Script
# Version: 2.0.0 - Next Valley Edition

param(
    [string]$Action = "start",
    [bool]$AutoLaunch = $True
)

function Start-CopilotService {
    # Start Copilot service
    $copilotProcess = Get-Process -Name "Copilot" -ErrorAction SilentlyContinue
    
    if (-not $copilotProcess) {
        # Try to start via URI
        Start-Process -FilePath "ms-copilot:"
        
        # Wait for process to start
        Start-Sleep -Seconds 2
        
        $copilotProcess = Get-Process -Name "Copilot" -ErrorAction SilentlyContinue
        if ($copilotProcess) {
            Write-Host "Copilot service started" -ForegroundColor Green
            return $True
        } else {
            Write-Host "Failed to start Copilot service" -ForegroundColor Red
            return $False
        }
    } else {
        Write-Host "Copilot service is already running" -ForegroundColor Green
        return $True
    }
}

function Stop-CopilotService {
    # Stop Copilot service
    $copilotProcess = Get-Process -Name "Copilot" -ErrorAction SilentlyContinue
    
    if ($copilotProcess) {
        Stop-Process -Name "Copilot" -Force
        Write-Host "Copilot service stopped" -ForegroundColor Green
        return $True
    } else {
        Write-Host "Copilot service is not running" -ForegroundColor Yellow
        return $True
    }
}

function Restart-CopilotService {
    Stop-CopilotService
    Start-Sleep -Seconds 1
    Start-CopilotService
}

# Configure auto-launch
if ($AutoLaunch) {
    $autoLaunchReg = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Copilot"
    New-Item -Path $autoLaunchReg -Force | Out-Null
    Set-ItemProperty -Path $autoLaunchReg -Name "AutoLaunch" -Value 1
}

# Perform action
switch ($Action) {
    "start" {
        Start-CopilotService
    }
    "stop" {
        Stop-CopilotService
    }
    "restart" {
        Restart-CopilotService
    }
    "status" {
        $process = Get-Process -Name "Copilot" -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "Copilot service is running" -ForegroundColor Green
        } else {
            Write-Host "Copilot service is not running" -ForegroundColor Red
        }
    }
    default {
        Write-Host "Invalid action: $Action" -ForegroundColor Red
        Write-Host "Usage: .\\start_copilot_service.ps1 -Action [start|stop|restart|status] -AutoLaunch [true|false]"
    }
}

Write-Host "Copilot 2.0 Service management completed!" -ForegroundColor Green
'''
    
    def create_copilot_config(self) -> bool:
        """Create Copilot 2.0 configuration file"""
        print(f"Creating Copilot 2.0 configuration...")
        
        copilot_config = {
            "version": self.version,
            "name": self.name,
            "description": self.description,
            "enabled": self.config['enabled'],
            "copilot_2_enabled": self.config['copilot_2_enabled'],
            "integration_points": self.config['integration_points'],
            "ai_features": self.config['ai_features'],
            "privacy": self.config['privacy'],
            "performance": self.config['performance'],
            "capabilities": self.copilot_capabilities,
            "features": {
                "taskbar_integration": True,
                "widget_integration": True,
                "file_explorer_integration": True,
                "start_menu_integration": True,
                "settings_integration": True
            }
        }
        
        try:
            config_dir = Path(__file__).parent.parent.parent.parent / 'config' / 'Windows12'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'copilot_integration_config.json'
            
            with open(config_file, 'w') as f:
                json.dump(copilot_config, f, indent=4)
            
            print(f"[+] Copilot 2.0 configuration saved to {config_file}")
            return True
        except Exception as e:
            print(f"[-] Error creating Copilot 2.0 configuration: {e}")
            return False
    
    def install(self) -> bool:
        """Install the Copilot 2.0 integration module"""
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
        
        # Step 3: Configure Copilot 2.0 integration
        if not self.configure_copilot_integration():
            print(f"[-] Failed to configure Copilot 2.0 integration")
            success = False
        
        # Step 4: Configure PowerToys Copilot
        if not self.configure_powertoys_copilot():
            print(f"[-] Failed to configure PowerToys Copilot")
            success = False
        
        # Step 5: Create Copilot scripts
        if not self.create_copilot_scripts():
            print(f"[-] Failed to create Copilot scripts")
            success = False
        
        # Step 6: Create Copilot configuration
        if not self.create_copilot_config():
            print(f"[-] Failed to create Copilot configuration")
            success = False
        
        if success:
            print(f"\n[+] {self.name} installed successfully!")
        else:
            print(f"\n[-] {self.name} installation completed with errors")
        
        return success
    
    def uninstall(self) -> bool:
        """Uninstall the Copilot 2.0 integration module"""
        print(f"Uninstalling: {self.name}")
        
        try:
            # Remove Copilot integration configuration
            copilot_config = Path.home() / 'AppData' / 'Local' / 'Microsoft' / 'Copilot' / 'windows12_config.json'
            if copilot_config.exists():
                copilot_config.unlink()
                print(f"[+] Removed Copilot 2.0 integration configuration")
            
            # Remove PowerToys Copilot configuration
            pt_config = Path.home() / 'AppData' / 'Local' / 'Microsoft' / 'PowerToys' / 'copilot_config.json'
            if pt_config.exists():
                pt_config.unlink()
                print(f"[+] Removed PowerToys Copilot configuration")
            
            # Remove Copilot configuration
            config_file = Path(__file__).parent.parent.parent.parent / 'config' / 'Windows12' / 'copilot_integration_config.json'
            if config_file.exists():
                config_file.unlink()
                print(f"[+] Removed Copilot 2.0 configuration")
            
            # Remove Copilot scripts
            scripts_dir = Path(__file__).parent.parent.parent / r'src' / r'scripts'
            for script_name in ['enable_copilot_integration.ps1', 'configure_copilot_features.ps1', 'start_copilot_service.ps1']:
                script_file = scripts_dir / script_name
                if script_file.exists():
                    script_file.unlink()
                    print(f"[+] Removed script: {script_name}")
            
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
            # Reset Copilot settings
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Software\Microsoft\Windows\CurrentVersion\Copilot', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'Enabled')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'AutoLaunch')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'Hotkey')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'Position')
                except:
                    pass
            
            # Reset AI settings
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Software\Microsoft\Windows\CurrentVersion\AI', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'Enabled')
                except:
                    pass
                try:
                    winreg.DeleteValue(key, 'CopilotEnabled')
                except:
                    pass
            
            # Reset Explorer settings
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                   r'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced', 
                                   0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, 'Start_ShowSearch')
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
            'copilot_configured': False,
            'powertoys_configured': False
        }
        
        # Check if configurations exist
        copilot_config = Path.home() / 'AppData' / 'Local' / 'Microsoft' / 'Copilot' / 'windows12_config.json'
        pt_config = Path.home() / 'AppData' / 'Local' / 'Microsoft' / 'PowerToys' / 'copilot_config.json'
        
        status['copilot_configured'] = copilot_config.exists()
        status['powertoys_configured'] = pt_config.exists()
        
        return status


# Module interface
if __name__ == "__main__":
    module = Copilot2IntegrationModule()
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        success = module.install()
        sys.exit(0 if success else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        success = module.uninstall()
        sys.exit(0 if success else 1)
    else:
        print(f"{module.get_name()} - {module.get_description()}")
        print("Usage: python copilot_integration.py [install|uninstall]")
