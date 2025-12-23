"""
YouTube Cookie Exporter
=======================
Run this script with Administrator privileges to export YouTube cookies
for use with the historian_crawler.py script.

Usage: Run as Administrator
    python export_youtube_cookies.py
"""

import os
import sys

def export_cookies():
    """Export YouTube cookies from browser to cookies.txt"""

    output_file = os.path.join(os.path.dirname(__file__), 'youtube_cookies.txt')

    print("=" * 60)
    print("YouTube Cookie Exporter")
    print("=" * 60)
    print()
    print("Attempting to extract cookies from installed browsers...")
    print("Make sure you're logged into YouTube in your browser first!")
    print()

    try:
        import browser_cookie3
    except ImportError:
        print("Installing browser_cookie3...")
        os.system("pip install browser_cookie3")
        import browser_cookie3

    cookies_found = []

    # Try Chrome
    try:
        cj = browser_cookie3.chrome(domain_name='.youtube.com')
        cookies = list(cj)
        if cookies:
            cookies_found.extend(cookies)
            print(f"[OK] Chrome: Found {len(cookies)} cookies")
    except Exception as e:
        print(f"[X] Chrome: {str(e)[:50]}")

    # Try Edge
    try:
        cj = browser_cookie3.edge(domain_name='.youtube.com')
        cookies = list(cj)
        if cookies:
            cookies_found.extend(cookies)
            print(f"[OK] Edge: Found {len(cookies)} cookies")
    except Exception as e:
        print(f"[X] Edge: {str(e)[:50]}")

    # Try Firefox
    try:
        cj = browser_cookie3.firefox(domain_name='.youtube.com')
        cookies = list(cj)
        if cookies:
            cookies_found.extend(cookies)
            print(f"[OK] Firefox: Found {len(cookies)} cookies")
    except Exception as e:
        print(f"[X] Firefox: {str(e)[:50]}")

    if not cookies_found:
        print()
        print("=" * 60)
        print("ERROR: No cookies found!")
        print("=" * 60)
        print()
        print("Please make sure:")
        print("1. You're running this script as Administrator")
        print("2. You're logged into YouTube in your browser")
        print("3. Your browser is closed (cookies may be locked)")
        print()
        print("Manual export option:")
        print("  - Install a browser extension like 'Get cookies.txt'")
        print("  - Export cookies while on youtube.com")
        print("  - Save as 'youtube_cookies.txt' in this folder")
        return False

    # Write cookies in Netscape format
    with open(output_file, 'w') as f:
        f.write("# Netscape HTTP Cookie File\n")
        f.write("# https://curl.se/docs/http-cookies.html\n")
        f.write("# This file was generated automatically.\n\n")

        for cookie in cookies_found:
            secure = "TRUE" if cookie.secure else "FALSE"
            expires = str(cookie.expires) if cookie.expires else "0"
            http_only = "TRUE"  # Assume HTTP only

            line = f"{cookie.domain}\t{http_only}\t{cookie.path}\t{secure}\t{expires}\t{cookie.name}\t{cookie.value}\n"
            f.write(line)

    print()
    print("=" * 60)
    print(f"SUCCESS! Saved {len(cookies_found)} cookies to:")
    print(f"  {output_file}")
    print("=" * 60)
    print()
    print("You can now run the historian_crawler.py script.")
    return True

if __name__ == '__main__':
    # Check if running as admin on Windows
    if sys.platform == 'win32':
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print()
                print("WARNING: Not running as Administrator!")
                print("Cookie extraction may fail.")
                print()
                print("To run as admin:")
                print("  1. Open Command Prompt as Administrator")
                print("  2. Navigate to this folder")
                print("  3. Run: python export_youtube_cookies.py")
                print()
        except:
            pass

    export_cookies()
