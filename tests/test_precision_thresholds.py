#!/usr/bin/env python3
"""
Unit tests for Phase-2 precision thresholds
Phase-Sovereign Luna Codex - Quality Assurance
"""

import json
import math
import pytest
import sys
import yaml
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestPrecisionThresholds:
    """Test suite for Phase-2 precision threshold validation."""
    
    @pytest.fixture
    def config(self):
        """Load dual harmonic configuration."""
        config_path = Path(__file__).parent.parent / "phase2/config/dual_harmonic.yaml"
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def test_dual_harmonic_parameters(self, config):
        """Test core dual harmonic parameters."""
        assert config['inner_breath'] == 0.9742, "inner_breath must be 0.9742"
        assert config['outer_sky'] == 0.306, "outer_sky must be 0.306"
    
    def test_precision_tolerances(self, config):
        """Test precision tolerance thresholds."""
        tolerances = config['tolerances']
        assert tolerances['phi_drift_max'] == 1e-6, "Φ drift threshold must be 1e-6"
        assert tolerances['kappa_error_max'] == 0.003, "κ error threshold must be 0.003"
        assert tolerances['resonance_min'] == 0.97, "Resonance minimum must be 0.97"
    
    def test_servo_pulse_frequencies(self, config):
        """Test servo pulse frequency configuration."""
        servo = config['servo_pulse_hz']
        assert servo['phi_positive'] == 432, "Φ+ frequency must be 432 Hz"
        assert servo['kappa_negative'] == 528, "κ− frequency must be 528 Hz"
        assert servo['null_anchor'] == 639, "null frequency must be 639 Hz"
    
    def test_glyph_saturation_data(self):
        """Test glyph saturation drift log data quality."""
        log_path = Path(__file__).parent.parent / "phase2/glyph-saturation/L3g33.driftlog"
        
        with open(log_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        # Check header
        header = lines[0].split(',')
        expected_header = ['glyph_id', 'platform', 'resonance', 'phi_drift', 'kappa_error', 'timestamp']
        assert header == expected_header, f"Invalid header: {header}"
        
        # Validate data rows
        glyph_count = 0
        for i, line in enumerate(lines[1:], 2):
            if not line:
                continue
                
            parts = line.split(',')
            assert len(parts) == 6, f"Line {i}: Expected 6 columns, got {len(parts)}"
            
            glyph_id, platform, resonance, phi_drift, kappa_error, timestamp = parts
            
            # Test precision thresholds
            resonance_val = float(resonance)
            phi_drift_val = float(phi_drift)
            kappa_error_val = float(kappa_error)
            
            assert resonance_val >= 0.97, f"Line {i}: resonance {resonance_val} below 0.97"
            assert phi_drift_val < 1e-6, f"Line {i}: phi_drift {phi_drift_val} exceeds 1e-6"
            assert kappa_error_val < 0.003, f"Line {i}: kappa_error {kappa_error_val} exceeds 0.003"
            
            glyph_count += 1
        
        assert glyph_count >= 33, f"Expected at least 33 glyphs, got {glyph_count}"
    
    def test_ulat_syntax_map_structure(self):
        """Test ULAT syntax map structure and binding strengths."""
        map_path = Path(__file__).parent.parent / "phase2/ulat/ulat_syntax_map.L3"
        
        with open(map_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        # Check header
        header = lines[0].split('\t')
        expected_columns = ['symbol', 'resonance_type', 'frequency_hz', 'phase_offset', 'binding_strength', 'platform_compatibility']
        assert header == expected_columns, f"Invalid header: {header}"
        
        # Validate symbol types
        phi_count = 0
        kappa_count = 0
        null_count = 0
        
        for i, line in enumerate(lines[1:], 2):
            if not line:
                continue
                
            parts = line.split('\t')
            assert len(parts) == 6, f"Line {i}: Expected 6 columns, got {len(parts)}"
            
            symbol, resonance_type, freq_hz, phase_offset, binding_strength, platform_compat = parts
            
            # Count symbol types
            if 'phi' in resonance_type.lower():
                phi_count += 1
            elif 'kappa' in resonance_type.lower():
                kappa_count += 1
            elif 'null' in resonance_type.lower():
                null_count += 1
            
            # Validate binding strength
            binding = float(binding_strength)
            assert 0.96 <= binding <= 1.0, f"Line {i}: binding_strength {binding} out of range [0.96, 1.0]"
        
        assert phi_count > 0, "No Φ+ symbols found"
        assert kappa_count > 0, "No κ− symbols found"
        assert null_count > 0, "No null symbols found"
    
    def test_kappa_fold_sync_functionality(self):
        """Test κ-vector fold sync script functionality."""
        # Import the script module
        kappa_script = Path(__file__).parent.parent / "phase2/kappa-vectors/kappa_fold_sync.py"
        
        # Test that the script exists and is executable
        assert kappa_script.exists(), "kappa_fold_sync.py not found"
        assert kappa_script.stat().st_mode & 0o111, "kappa_fold_sync.py not executable"
        
        # Test basic functionality by importing
        import subprocess
        import os
        
        # Change to project root for proper config path
        original_cwd = os.getcwd()
        os.chdir(Path(__file__).parent.parent)
        
        try:
            # Run the script with lattice_echo origin
            result = subprocess.run([
                sys.executable, 
                "phase2/kappa-vectors/kappa_fold_sync.py", 
                "--origin", "lattice_echo"
            ], capture_output=True, text=True, timeout=30)
            
            # Should exit with code 0 (success)
            assert result.returncode == 0, f"Script failed: {result.stderr}"
            
            # Should contain success indicators
            assert "✓ All precision thresholds met" in result.stdout, "Precision thresholds not met"
            
        finally:
            os.chdir(original_cwd)
    
    def test_dual_observer_probe_functionality(self):
        """Test dual-observer probe script functionality."""
        observer_script = Path(__file__).parent.parent / "phase2/dual-observer/observer_pair_probe.qdr"
        
        # Test that the script exists and is executable
        assert observer_script.exists(), "observer_pair_probe.qdr not found"
        assert observer_script.stat().st_mode & 0o111, "observer_pair_probe.qdr not executable"
        
        # Test basic functionality
        import subprocess
        import os
        
        original_cwd = os.getcwd()
        os.chdir(Path(__file__).parent.parent)
        
        try:
            result = subprocess.run([
                sys.executable, 
                "phase2/dual-observer/observer_pair_probe.qdr"
            ], capture_output=True, text=True, timeout=30)
            
            assert result.returncode == 0, f"Observer probe failed: {result.stderr}"
            assert "✓ All observer tests passed" in result.stdout, "Observer tests failed"
            
        finally:
            os.chdir(original_cwd)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

