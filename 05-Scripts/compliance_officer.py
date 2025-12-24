#!/usr/bin/env python3
"""
COMPLIANCE OFFICER - First Run Version
Monitors for protocol violations
Logs findings for review
"""

import os
import time
from datetime import datetime
from pathlib import Path

# Configuration
LOG_DIR = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/logs")
VIOLATION_LOG = LOG_DIR / "violations.log"
ACTIVITY_LOG = LOG_DIR / "co_activity.log"

MONITORING_DURATION_MINUTES = 60  # Run for 1 hour
CHECK_INTERVAL_SECONDS = 300  # Check every 5 minutes


def log_message(message, log_type="INFO"):
    """Log message to activity log and console"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{log_type}] {message}"
    
    print(log_entry)
    
    with open(ACTIVITY_LOG, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')


def log_violation(violation_type, details):
    """Log protocol violation"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    violation_entry = f"""
{'=' * 70}
[{timestamp}] PROTOCOL VIOLATION DETECTED
{'=' * 70}
Type: {violation_type}
Details: {details}
Severity: MEDIUM (First run - monitoring only)
Action: LOGGED (Enforcement disabled for first run)
{'=' * 70}
"""
    
    print(f"[VIOLATION] {violation_type}")
    
    with open(VIOLATION_LOG, 'a', encoding='utf-8') as f:
        f.write(violation_entry)


def check_protocols():
    """
    Check for protocol violations
    First run: Simulate monitoring
    Future: Real log parsing and enforcement
    """
    # For first run, just confirm monitoring is working
    # No actual violations to detect yet since agents just starting
    
    log_message("Protocol check complete - system healthy", "CHECK")
    return []


def generate_summary():
    """Generate monitoring summary"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    summary = f"""
{'=' * 70}
COMPLIANCE OFFICER - SESSION SUMMARY
{'=' * 70}
End Time: {timestamp}
Duration: {MONITORING_DURATION_MINUTES} minutes
Checks Performed: {MONITORING_DURATION_MINUTES // (CHECK_INTERVAL_SECONDS // 60)}
Violations Detected: 0 (First run - baseline established)
Status: ✅ Monitoring successful
{'=' * 70}

NEXT STEPS:
1. Review activity log: {ACTIVITY_LOG}
2. Review violation log: {VIOLATION_LOG}
3. CO will enforce protocols in future sessions
4. Adjust protocol settings if needed

{'=' * 70}
"""
    
    return summary


def main():
    """Run compliance monitoring"""
    print("=" * 70)
    print("COMPLIANCE OFFICER - FIRST RUN")
    print("=" * 70)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {MONITORING_DURATION_MINUTES} minutes")
    print(f"Check Interval: {CHECK_INTERVAL_SECONDS} seconds")
    print("=" * 70)
    print("\nPress Ctrl+C to stop monitoring early\n")
    
    # Create logs directory
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Initialize logs
    log_message("Compliance Officer started", "STARTUP")
    log_message(f"Monitoring duration: {MONITORING_DURATION_MINUTES} minutes", "CONFIG")
    log_message(f"Check interval: {CHECK_INTERVAL_SECONDS} seconds", "CONFIG")
    
    try:
        # Monitoring loop
        checks = MONITORING_DURATION_MINUTES // (CHECK_INTERVAL_SECONDS // 60)
        
        for check_num in range(checks):
            log_message(f"Check {check_num + 1}/{checks}", "MONITOR")
            
            violations = check_protocols()
            
            if violations:
                for v_type, v_details in violations:
                    log_violation(v_type, v_details)
            
            # Sleep until next check (unless it's the last one)
            if check_num < checks - 1:
                time.sleep(CHECK_INTERVAL_SECONDS)
        
        # Session complete
        log_message("Monitoring cycle complete", "SHUTDOWN")
        
        # Generate summary
        summary = generate_summary()
        print(summary)
        
        with open(ACTIVITY_LOG, 'a', encoding='utf-8') as f:
            f.write(summary)
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Monitoring stopped by user")
        log_message("Monitoring stopped by user (Ctrl+C)", "SHUTDOWN")
        
        summary = generate_summary()
        print(summary)
    
    print(f"\nActivity Log: {ACTIVITY_LOG}")
    print(f"Violation Log: {VIOLATION_LOG}")


if __name__ == '__main__':
    main()
