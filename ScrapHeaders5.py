import requests
import csv
import ssl

# Ignore SSL certificate warnings (for government or self-signed certs)
ssl._create_default_https_context = ssl._create_unverified_context

# List of websites to test
urls = [
    "https://www.nitk.ac.in/",
    "https://manipal.edu/",
    "https://www.iisc.ac.in/",
    "https://www.iitm.ac.in/",  # Added IIT Madras URL explicitly
]

def fetch_headers(url):
    try:
        session = requests.Session()
        # Set a browser-like User-Agent to reduce blocking chances
        session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; Bot/1.0)'})
        
        response = session.get(url, timeout=10, verify=False)
        headers_lower = {k.lower(): v for k, v in response.headers.items()}

        # Extract HSTS max-age if present
        hsts = headers_lower.get('strict-transport-security', '')
        hsts_max_age = 0
        if 'max-age=' in hsts:
            try:
                hsts_max_age = int(hsts.split('max-age=')[1].split(';')[0])
            except ValueError:
                pass

        return {
            "Website URL": url,
            "HSTS": 1 if hsts else 0,
            "HSTS_max_age": hsts_max_age,
            "CSP": 1 if 'content-security-policy' in headers_lower else 0,
            "XCTO": 1 if 'x-content-type-options' in headers_lower else 0,
            "XFO": headers_lower.get('x-frame-options', 'None'),
            "Referrer_Policy": headers_lower.get('referrer-policy', 'None'),
            "Perm_Policy": 1 if 'permissions-policy' in headers_lower else 0,
            "TLS_Version": "Unknown",  # TLS version not available directly via requests
            "HTTP_Code": response.status_code,
            "Server": headers_lower.get('server', 'Unknown'),
            "CORS": headers_lower.get('access-control-allow-origin', 'None'),
            "Cookie_HttpOnly": 1 if 'httponly' in headers_lower.get('set-cookie', '').lower() else 0,
            "Cookie_Secure": 1 if 'secure' in headers_lower.get('set-cookie', '').lower() else 0
        }
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

# Output CSV file path
output_file = "website_headers_dataset6.csv"

# Extract headers and write to CSV
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
            print(f"✅ Successfully fetched: {url} (Status: {data['HTTP_Code']})")
        else:
            print(f"⚠️  Skipped: {url}")
