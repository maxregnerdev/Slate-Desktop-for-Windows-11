#!/usr/bin/env python3
"""
Slate Desktop for Windows 11 - CI/CD Pipeline
Version: 2.0.0 - Next Valley Edition

Continuous Integration script for Windows 12 UI Transformation
Handles testing, validation, and build processes.
"""

import os
import sys
import json
import platform
import subprocess
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)


class CIPipeline:
    """CI/CD Pipeline for Windows 12 UI Transformation"""
    
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.src_dir = self.root_dir / "src"
        self.config_dir = self.root_dir / "config"
        self.sources_dir = self.root_dir / "sources"
        
        # CI Configuration
        self.ci_config = {
            "version": "2.0.0",
            "name": "Windows 12 UI Transformation CI",
            "stages": [
                "validate_environment",
                "check_dependencies",
                "syntax_check",
                "import_test",
                "validate_configuration",
                "build_preparation"
            ],
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
            "platform": platform.system(),
            "success": True,
            "errors": []
        }
    
    def print_header(self):
        """Print CI Pipeline Header"""
        print(Fore.CYAN + "=" * 60)
        print(Fore.CYAN + "Slate Desktop - Windows 12 UI Transformation CI")
        print(Fore.CYAN + "Version: 2.0.0 - Next Valley Edition")
        print(Fore.CYAN + "=" * 60)
        print()
    
    def validate_environment(self):
        """Validate CI environment"""
        print(Fore.YELLOW + "[CI] Validating environment...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            error = "Python 3.8+ required"
            print(Fore.RED + f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
            return False
        else:
            print(Fore.GREEN + f"  ✓ Python {self.ci_config['python_version']}")
        
        # Check platform
        if platform.system() != "Windows":
            error = "Windows platform required"
            print(Fore.RED + f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
            return False
        else:
            print(Fore.GREEN + f"  ✓ Platform: {self.ci_config['platform']}")
        
        # Check if running in CI environment
        ci_env = os.environ.get('CI', 'false').lower() == 'true'
        if ci_env:
            print(Fore.GREEN + "  ✓ CI Environment detected")
        else:
            print(Fore.YELLOW + "  ⚠ Not running in CI environment")
        
        print()
        return True
    
    def check_dependencies(self):
        """Check Python dependencies"""
        print(Fore.YELLOW + "[CI] Checking dependencies...")
        
        # Check if requirements.txt exists
        requirements_file = self.root_dir / "requirements.txt"
        if not requirements_file.exists():
            error = "requirements.txt not found"
            print(Fore.RED + f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
            return False
        
        print(Fore.GREEN + "  ✓ requirements.txt found")
        
        # Try to check if dependencies are installed
        try:
            import colorama
            print(Fore.GREEN + "  ✓ colorama installed")
        except ImportError:
            error = "colorama not installed"
            print(Fore.RED + f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
        
        try:
            import requests
            print(Fore.GREEN + "  ✓ requests installed")
        except ImportError:
            error = "requests not installed"
            print(Fore.RED + f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
        
        try:
            import psutil
            print(Fore.GREEN + "  ✓ psutil installed")
        except ImportError:
            error = "psutil not installed"
            print(Fore.RED + f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
        
        try:
            import pywin32
            print(Fore.GREEN + "  ✓ pywin32 installed")
        except ImportError:
            error = "pywin32 not installed"
            print(Fore.RED + f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
        
        try:
            import rich
            print(Fore.GREEN + "  ✓ rich installed")
        except ImportError:
            error = "rich not installed"
            print(Fore.RED + f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
        
        print()
        return self.ci_config["success"]
    
    def syntax_check(self):
        """Check Python syntax for all source files"""
        print(Fore.YELLOW + "[CI] Checking Python syntax...")
        
        python_files = list(self.src_dir.rglob("*.py"))
        
        if not python_files:
            error = "No Python files found"
            print(Fore.RED + f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
            return False
        
        print(Fore.GREEN + f"  ✓ Found {len(python_files)} Python files")
        
        syntax_errors = []
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), str(py_file), 'exec')
                print(Fore.GREEN + f"  ✓ {py_file.name}")
            except SyntaxError as e:
                error = f"{py_file.name}: {e}"
                print(Fore.RED + f"  ✗ {error}")
                syntax_errors.append(error)
                self.ci_config["success"] = False
                self.ci_config["errors"].append(error)
        
        if syntax_errors:
            print(Fore.RED + f"  ✗ Found {len(syntax_errors)} syntax errors")
        else:
            print(Fore.GREEN + "  ✓ All Python files have valid syntax")
        
        print()
        return self.ci_config["success"]
    
    def import_test(self):
        """Test importing all modules"""
        print(Fore.YELLOW + "[CI] Testing module imports...")
        
        modules_to_test = [
            'main',
            'modules.taskbar',
            'modules.widgets',
            'modules.ai_integration',
            'modules.fluent_design',
            'modules.hybrid_optimization',
            'themes.windows12_theme',
            'themes.modular_design',
            'themes.copilot_integration'
        ]
        
        import_errors = []
        for module_name in modules_to_test:
            try:
                __import__(f'src.{module_name}')
                print(Fore.GREEN + f"  ✓ {module_name}")
            except ImportError as e:
                error = f"{module_name}: {e}"
                print(Fore.RED + f"  ✗ {error}")
                import_errors.append(error)
                self.ci_config["success"] = False
                self.ci_config["errors"].append(error)
            except Exception as e:
                error = f"{module_name}: {e}"
                print(Fore.RED + f"  ✗ {error}")
                import_errors.append(error)
                self.ci_config["success"] = False
                self.ci_config["errors"].append(error)
        
        if import_errors:
            print(Fore.RED + f"  ✗ Found {len(import_errors)} import errors")
        else:
            print(Fore.GREEN + "  ✓ All modules imported successfully")
        
        print()
        return self.ci_config["success"]
    
    def validate_configuration(self):
        """Validate configuration files"""
        print(Fore.YELLOW + "[CI] Validating configuration files...")
        
        # Check if config directory exists
        if not self.config_dir.exists():
            print(Fore.YELLOW + "  ⚠ Config directory not found (will be created during install)")
        else:
            print(Fore.GREEN + "  ✓ Config directory exists")
        
        # Check if sources directory exists
        if not self.sources_dir.exists():
            print(Fore.YELLOW + "  ⚠ Sources directory not found (will be created during install)")
        else:
            print(Fore.GREEN + "  ✓ Sources directory exists")
        
        # Check install.bat
        install_bat = self.root_dir / "install.bat"
        if install_bat.exists():
            print(Fore.GREEN + "  ✓ install.bat exists")
        else:
            error = "install.bat not found"
            print(Fore.RED + f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
        
        # Check requirements.txt
        requirements_txt = self.root_dir / "requirements.txt"
        if requirements_txt.exists():
            print(Fore.GREEN + "  ✓ requirements.txt exists")
        else:
            error = "requirements.txt not found"
            print(Fore.RED + f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
        
        print()
        return self.ci_config["success"]
    
    def build_preparation(self):
        """Prepare for build/release"""
        print(Fore.YELLOW + "[CI] Preparing for build...")
        
        # Check git status
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.root_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                if result.stdout.strip():
                    print(Fore.YELLOW + f"  ⚠ Uncommitted changes detected")
                    print(Fore.YELLOW + f"    {result.stdout.strip()}")
                else:
                    print(Fore.GREEN + "  ✓ No uncommitted changes")
            else:
                print(Fore.YELLOW + "  ⚠ Git not available or not a git repo")
        except Exception as e:
            print(Fore.YELLOW + f"  ⚠ Git check failed: {e}")
        
        # Check if README exists
        readme = self.root_dir / "README.md"
        if readme.exists():
            print(Fore.GREEN + "  ✓ README.md exists")
        else:
            print(Fore.YELLOW + "  ⚠ README.md not found")
        
        # Check LICENSE
        license_file = self.root_dir / "LICENSE"
        if license_file.exists():
            print(Fore.GREEN + "  ✓ LICENSE exists")
        else:
            print(Fore.YELLOW + "  ⚠ LICENSE not found")
        
        print()
        return True
    
    def generate_ci_report(self):
        """Generate CI report"""
        print(Fore.YELLOW + "[CI] Generating CI report...")
        
        report = {
            "ci_pipeline": self.ci_config,
            "timestamp": self.get_timestamp(),
            "summary": {
                "total_checks": len(self.ci_config["stages"]),
                "passed": len(self.ci_config["stages"]) if self.ci_config["success"] else 0,
                "failed": len(self.ci_config["errors"]),
                "warnings": 0
            },
            "details": {
                "environment": {
                    "python_version": self.ci_config["python_version"],
                    "platform": self.ci_config["platform"],
                    "working_directory": str(self.root_dir)
                },
                "errors": self.ci_config["errors"]
            }
        }
        
        # Save report
        report_file = self.root_dir / "ci_report.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=4, ensure_ascii=False)
            print(Fore.GREEN + f"  ✓ CI report saved to {report_file.name}")
        except Exception as e:
            print(Fore.RED + f"  ✗ Failed to save CI report: {e}")
        
        print()
        return report
    
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def print_summary(self):
        """Print CI summary"""
        print(Fore.CYAN + "=" * 60)
        print(Fore.CYAN + "CI Pipeline Summary")
        print(Fore.CYAN + "=" * 60)
        
        if self.ci_config["success"]:
            print(Fore.GREEN + "✓ CI Pipeline PASSED")
        else:
            print(Fore.RED + "✗ CI Pipeline FAILED")
        
        print()
        print(Fore.WHITE + f"Version: {self.ci_config['version']}")
        print(Fore.WHITE + f"Timestamp: {self.get_timestamp()}")
        print(Fore.WHITE + f"Python: {self.ci_config['python_version']}")
        print(Fore.WHITE + f"Platform: {self.ci_config['platform']}")
        
        if self.ci_config["errors"]:
            print()
            print(Fore.RED + "Errors:")
            for error in self.ci_config["errors"]:
                print(Fore.RED + f"  - {error}")
        
        print(Fore.CYAN + "=" * 60)
    
    def run(self):
        """Run the CI pipeline"""
        self.print_header()
        
        # Run all stages
        for stage in self.ci_config["stages"]:
            print(Fore.CYAN + f"\n{'=' * 60}")
            print(Fore.CYAN + f"Stage: {stage}")
            print(Fore.CYAN + "=" * 60)
            
            stage_method = getattr(self, stage, None)
            if stage_method:
                if not stage_method():
                    print(Fore.RED + f"✗ Stage '{stage}' failed")
                    # Continue with other stages to collect all errors
            else:
                error = f"Unknown stage: {stage}"
                print(Fore.RED + f"  ✗ {error}")
                self.ci_config["success"] = False
                self.ci_config["errors"].append(error)
        
        # Generate report
        report = self.generate_ci_report()
        
        # Print summary
        self.print_summary()
        
        return self.ci_config["success"]


def main():
    """Main entry point"""
    pipeline = CIPipeline()
    success = pipeline.run()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
