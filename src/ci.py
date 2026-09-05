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

# Try to import colorama for colored output
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    # Fallback for environments without colorama
    HAS_COLORAMA = False
    class ColorFallback:
        def __getattr__(self, name):
            return ''
    Fore = ColorFallback()
    Style = ColorFallback()


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
        if HAS_COLORAMA:
            print(Fore.YELLOW + "[CI] Validating environment...")
        else:
            print("[CI] Validating environment...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            error = "Python 3.8+ required"
            if HAS_COLORAMA:
                print(Fore.RED + f"  ✗ {error}")
            else:
                print(f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
            return False
        else:
            if HAS_COLORAMA:
                print(Fore.GREEN + f"  ✓ Python {self.ci_config['python_version']}")
            else:
                print(f"  ✓ Python {self.ci_config['python_version']}")
        
        # Check platform
        if platform.system() != "Windows":
            # This is expected on non-Windows CI environments
            # Don't fail the entire pipeline, just note it
            warning = "Windows platform required (running on " + platform.system() + ")"
            if HAS_COLORAMA:
                print(Fore.YELLOW + f"  ⚠ {warning}")
            else:
                print(f"  ⚠ {warning}")
            # Don't mark as failure - this is expected on non-Windows
            return True
        else:
            if HAS_COLORAMA:
                print(Fore.GREEN + f"  ✓ Platform: {self.ci_config['platform']}")
            else:
                print(f"  ✓ Platform: {self.ci_config['platform']}")
        
        # Check if running in CI environment
        ci_env = os.environ.get('CI', 'false').lower() == 'true'
        if ci_env:
            if HAS_COLORAMA:
                print(Fore.GREEN + "  ✓ CI Environment detected")
            else:
                print("  ✓ CI Environment detected")
        else:
            if HAS_COLORAMA:
                print(Fore.YELLOW + "  ⚠ Not running in CI environment")
            else:
                print("  ⚠ Not running in CI environment")
        
        if HAS_COLORAMA:
            print()
        else:
            print()
        return True
    
    def check_dependencies(self):
        """Check Python dependencies"""
        if HAS_COLORAMA:
            print(Fore.YELLOW + "[CI] Checking dependencies...")
        else:
            print("[CI] Checking dependencies...")
        
        # Check if requirements.txt exists
        requirements_file = self.root_dir / "requirements.txt"
        if not requirements_file.exists():
            error = "requirements.txt not found"
            if HAS_COLORAMA:
                print(Fore.RED + f"  ✗ {error}")
            else:
                print(f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
            return False
        
        if HAS_COLORAMA:
            print(Fore.GREEN + "  ✓ requirements.txt found")
        else:
            print("  ✓ requirements.txt found")
        
        # Try to check if dependencies are installed
        dependencies = [
            ('colorama', 'colorama'),
            ('requests', 'requests'),
            ('psutil', 'psutil'),
            ('rich', 'rich'),
            ('pywin32', 'pywin32')
        ]
        
        for name, module in dependencies:
            try:
                __import__(module)
                if HAS_COLORAMA:
                    print(Fore.GREEN + f"  ✓ {name} installed")
                else:
                    print(f"  ✓ {name} installed")
            except ImportError:
                # For Windows-only packages, don't fail on non-Windows
                if module == 'pywin32' and platform.system() != "Windows":
                    if HAS_COLORAMA:
                        print(Fore.YELLOW + f"  ⚠ {name} not installed (Windows-only)")
                    else:
                        print(f"  ⚠ {name} not installed (Windows-only)")
                else:
                    error = f"{name} not installed"
                    if HAS_COLORAMA:
                        print(Fore.RED + f"  ✗ {error}")
                    else:
                        print(f"  ✗ {error}")
                    self.ci_config["success"] = False
                    self.ci_config["errors"].append(error)
        
        if HAS_COLORAMA:
            print()
        else:
            print()
        return self.ci_config["success"]
    
    def syntax_check(self):
        """Check Python syntax for all source files"""
        if HAS_COLORAMA:
            print(Fore.YELLOW + "[CI] Checking Python syntax...")
        else:
            print("[CI] Checking Python syntax...")
        
        python_files = list(self.src_dir.rglob("*.py"))
        
        if not python_files:
            error = "No Python files found"
            if HAS_COLORAMA:
                print(Fore.RED + f"  ✗ {error}")
            else:
                print(f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
            return False
        
        if HAS_COLORAMA:
            print(Fore.GREEN + f"  ✓ Found {len(python_files)} Python files")
        else:
            print(f"  ✓ Found {len(python_files)} Python files")
        
        syntax_errors = []
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), str(py_file), 'exec')
                if HAS_COLORAMA:
                    print(Fore.GREEN + f"  ✓ {py_file.name}")
                else:
                    print(f"  ✓ {py_file.name}")
            except SyntaxError as e:
                error = f"{py_file.name}: {e}"
                if HAS_COLORAMA:
                    print(Fore.RED + f"  ✗ {error}")
                else:
                    print(f"  ✗ {error}")
                syntax_errors.append(error)
                self.ci_config["success"] = False
                self.ci_config["errors"].append(error)
        
        if syntax_errors:
            if HAS_COLORAMA:
                print(Fore.RED + f"  ✗ Found {len(syntax_errors)} syntax errors")
            else:
                print(f"  ✗ Found {len(syntax_errors)} syntax errors")
        else:
            if HAS_COLORAMA:
                print(Fore.GREEN + "  ✓ All Python files have valid syntax")
            else:
                print("  ✓ All Python files have valid syntax")
        
        if HAS_COLORAMA:
            print()
        else:
            print()
        return self.ci_config["success"]
    
    def import_test(self):
        """Test importing all modules"""
        if HAS_COLORAMA:
            print(Fore.YELLOW + "[CI] Testing module imports...")
        else:
            print("[CI] Testing module imports...")
        
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
                if HAS_COLORAMA:
                    print(Fore.GREEN + f"  ✓ {module_name}")
                else:
                    print(f"  ✓ {module_name}")
            except ImportError as e:
                # For Windows-only modules, don't fail on non-Windows
                if 'winreg' in str(e) or 'pywin32' in str(e):
                    if HAS_COLORAMA:
                        print(Fore.YELLOW + f"  ⚠ {module_name}: {e} (Windows-only)")
                    else:
                        print(f"  ⚠ {module_name}: {e} (Windows-only)")
                else:
                    error = f"{module_name}: {e}"
                    if HAS_COLORAMA:
                        print(Fore.RED + f"  ✗ {error}")
                    else:
                        print(f"  ✗ {error}")
                    import_errors.append(error)
                    self.ci_config["success"] = False
                    self.ci_config["errors"].append(error)
            except Exception as e:
                error = f"{module_name}: {e}"
                if HAS_COLORAMA:
                    print(Fore.RED + f"  ✗ {error}")
                else:
                    print(f"  ✗ {error}")
                import_errors.append(error)
                self.ci_config["success"] = False
                self.ci_config["errors"].append(error)
        
        if import_errors:
            if HAS_COLORAMA:
                print(Fore.RED + f"  ✗ Found {len(import_errors)} import errors")
            else:
                print(f"  ✗ Found {len(import_errors)} import errors")
        else:
            if HAS_COLORAMA:
                print(Fore.GREEN + "  ✓ All modules imported successfully")
            else:
                print("  ✓ All modules imported successfully")
        
        if HAS_COLORAMA:
            print()
        else:
            print()
        return self.ci_config["success"]
    
    def validate_configuration(self):
        """Validate configuration files"""
        if HAS_COLORAMA:
            print(Fore.YELLOW + "[CI] Validating configuration files...")
        else:
            print("[CI] Validating configuration files...")
        
        # Check if config directory exists
        if not self.config_dir.exists():
            if HAS_COLORAMA:
                print(Fore.YELLOW + "  ⚠ Config directory not found (will be created during install)")
            else:
                print("  ⚠ Config directory not found (will be created during install)")
        else:
            if HAS_COLORAMA:
                print(Fore.GREEN + "  ✓ Config directory exists")
            else:
                print("  ✓ Config directory exists")
        
        # Check if sources directory exists
        if not self.sources_dir.exists():
            if HAS_COLORAMA:
                print(Fore.YELLOW + "  ⚠ Sources directory not found (will be created during install)")
            else:
                print("  ⚠ Sources directory not found (will be created during install)")
        else:
            if HAS_COLORAMA:
                print(Fore.GREEN + "  ✓ Sources directory exists")
            else:
                print("  ✓ Sources directory exists")
        
        # Check install.bat
        install_bat = self.root_dir / "install.bat"
        if install_bat.exists():
            if HAS_COLORAMA:
                print(Fore.GREEN + "  ✓ install.bat exists")
            else:
                print("  ✓ install.bat exists")
        else:
            error = "install.bat not found"
            if HAS_COLORAMA:
                print(Fore.RED + f"  ✗ {error}")
            else:
                print(f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
        
        # Check requirements.txt
        requirements_txt = self.root_dir / "requirements.txt"
        if requirements_txt.exists():
            if HAS_COLORAMA:
                print(Fore.GREEN + "  ✓ requirements.txt exists")
            else:
                print("  ✓ requirements.txt exists")
        else:
            error = "requirements.txt not found"
            if HAS_COLORAMA:
                print(Fore.RED + f"  ✗ {error}")
            else:
                print(f"  ✗ {error}")
            self.ci_config["success"] = False
            self.ci_config["errors"].append(error)
        
        if HAS_COLORAMA:
            print()
        else:
            print()
        return self.ci_config["success"]
    
    def build_preparation(self):
        """Prepare for build/release"""
        if HAS_COLORAMA:
            print(Fore.YELLOW + "[CI] Preparing for build...")
        else:
            print("[CI] Preparing for build...")
        
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
                    if HAS_COLORAMA:
                        print(Fore.YELLOW + f"  ⚠ Uncommitted changes detected")
                        print(Fore.YELLOW + f"    {result.stdout.strip()}")
                    else:
                        print(f"  ⚠ Uncommitted changes detected")
                        print(f"    {result.stdout.strip()}")
                else:
                    if HAS_COLORAMA:
                        print(Fore.GREEN + "  ✓ No uncommitted changes")
                    else:
                        print("  ✓ No uncommitted changes")
            else:
                if HAS_COLORAMA:
                    print(Fore.YELLOW + "  ⚠ Git not available or not a git repo")
                else:
                    print("  ⚠ Git not available or not a git repo")
        except Exception as e:
            if HAS_COLORAMA:
                print(Fore.YELLOW + f"  ⚠ Git check failed: {e}")
            else:
                print(f"  ⚠ Git check failed: {e}")
        
        # Check if README exists
        readme = self.root_dir / "README.md"
        if readme.exists():
            if HAS_COLORAMA:
                print(Fore.GREEN + "  ✓ README.md exists")
            else:
                print("  ✓ README.md exists")
        else:
            if HAS_COLORAMA:
                print(Fore.YELLOW + "  ⚠ README.md not found")
            else:
                print("  ⚠ README.md not found")
        
        # Check LICENSE
        license_file = self.root_dir / "LICENSE"
        if license_file.exists():
            if HAS_COLORAMA:
                print(Fore.GREEN + "  ✓ LICENSE exists")
            else:
                print("  ✓ LICENSE exists")
        else:
            if HAS_COLORAMA:
                print(Fore.YELLOW + "  ⚠ LICENSE not found")
            else:
                print("  ⚠ LICENSE not found")
        
        if HAS_COLORAMA:
            print()
        else:
            print()
        return True
    
    def generate_ci_report(self):
        """Generate CI report"""
        if HAS_COLORAMA:
            print(Fore.YELLOW + "[CI] Generating CI report...")
        else:
            print("[CI] Generating CI report...")
        
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
            if HAS_COLORAMA:
                print(Fore.GREEN + f"  ✓ CI report saved to {report_file.name}")
            else:
                print(f"  ✓ CI report saved to {report_file.name}")
        except Exception as e:
            if HAS_COLORAMA:
                print(Fore.RED + f"  ✗ Failed to save CI report: {e}")
            else:
                print(f"  ✗ Failed to save CI report: {e}")
        
        if HAS_COLORAMA:
            print()
        else:
            print()
        return report
    
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def print_summary(self):
        """Print CI summary"""
        if HAS_COLORAMA:
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
        else:
            print("=" * 60)
            print("CI Pipeline Summary")
            print("=" * 60)
            
            if self.ci_config["success"]:
                print("✓ CI Pipeline PASSED")
            else:
                print("✗ CI Pipeline FAILED")
            
            print()
            print(f"Version: {self.ci_config['version']}")
            print(f"Timestamp: {self.get_timestamp()}")
            print(f"Python: {self.ci_config['python_version']}")
            print(f"Platform: {self.ci_config['platform']}")
            
            if self.ci_config["errors"]:
                print()
                print("Errors:")
                for error in self.ci_config["errors"]:
                    print(f"  - {error}")
            
            print("=" * 60)
    
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
