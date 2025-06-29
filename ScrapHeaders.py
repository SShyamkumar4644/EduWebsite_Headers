import requests
import csv
import ssl
from urllib3.util.ssl_ import create_urllib3_context

# Ignore SSL cert warnings (for government websites that fail cert checks)
ssl._create_default_https_context = ssl._create_unverified_context

# List of websites you want to test
urls = [
    "https://www.nitk.ac.in/",
    "https://manipal.edu/",
    "https://www.iisc.ac.in/",
    # Add more URLs here
]

def fetch_headers(url):
    try:
        response = requests.get(url, timeout=10, verify=False)
        headers = response.headers
        result = {
            "Website URL": url,
            "HSTS": 1 if 'strict-transport-security' in headers else 0,
            "HSTS_max_age": int(headers.get('strict-transport-security', 'max-age=0').split('=')[1].split(';')[0]) if 'strict-transport-security' in headers else 0,
            "CSP": 1 if 'content-security-policy' in headers else 0,
            "XCTO": 1 if 'x-content-type-options' in headers else 0,
            "XFO": headers.get('x-frame-options', 'None'),
            "Referrer_Policy": headers.get('referrer-policy', 'None'),
            "Perm_Policy": 1 if 'permissions-policy' in headers else 0,
            "TLS_Version": response.raw.version if hasattr(response.raw, 'version') else 'Unknown',
            "HTTP_Code": response.status_code,
            "Server": headers.get('server', 'Unknown'),
            "CORS": headers.get('access-control-allow-origin', 'None'),
            "Cookie_HttpOnly": 1 if 'httponly' in headers.get('set-cookie', '').lower() else 0,
            "Cookie_Secure": 1 if 'secure' in headers.get('set-cookie', '').lower() else 0
        }
        return result
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

# Output CSV file
output_file = "website_headers_dataset.csv"

# Extract and write to CSV
with open(output_file, mode='w', newline='') as csv_file:
    fieldnames = [
        "Website URL", "HSTS", "HSTS_max_age", "CSP", "XCTO", "XFO",
        "Referrer_Policy", "Perm_Policy", "TLS_Version", "HTTP_Code",
        "Server", "CORS", "Cookie_HttpOnly", "Cookie_Secure"
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for url in urls:
        data = fetch_headers(url)
        if data:
            writer.writerow(data)
            print(f"✅ {url} done")
        else:
            print(f"⚠️  Skipped {url}")
