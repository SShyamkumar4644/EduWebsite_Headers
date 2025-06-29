import requests
import csv
import ssl

# Ignore SSL certificate warnings
ssl._create_default_https_context = ssl._create_unverified_context

# All 50+ institute website URLs
urls = [
    "https://www.nitk.ac.in/",
    "https://manipal.edu/",
    "https://www.iisc.ac.in/",
    "https://iiitb.ac.in/",
    "https://www.msrit.edu.in/",
    "https://www.rvce.edu.in/",
    "https://bmsce.ac.in/",
    "https://pes.edu/",
    "https://www.sit.ac.in/",
    "https://jssstuniv.in/",
    "https://nmamit.nitte.edu.in/",
    "https://www.dsce.edu.in/",
    "https://nmit.ac.in/",
    "https://cmrit.ac.in/",
    "https://alvaseducation.edu.in/",
    "https://newhorizonindia.edu/",
    "https://acharya.ac.in/",
    "https://ewit.edu.in/",
    "https://oxfordcollegeofengineering.com/",
    "https://msengineering.edu.in/",
    "https://sjbit.edu.in/",
    "https://reva.edu.in/",
    "https://kletech.ac.in/",
    "https://bietdvg.edu.in/",
    "https://uvce.ac.in/",
    "https://mitmangalore.in/",
    "https://mvitbengaluru.ac.in/",
    "https://jnnce.ac.in/",
    "https://rnsit.ac.in/",
    "https://knsit.ac.in/",
    "https://gsss.edu.in/",
    "https://kvgengg.edu.in/",
    "https://bmsit.org/",
    "https://mite.mangalore.edu.in/",
    "https://vvce.ac.in/",
    "https://nagarjunacollege.edu.in/",
    "https://www.msruas.ac.in/",
    "https://jssateb.ac.in/",
    "https://www.btibangalore.org/",
    "https://smvitm.edu.in/",
    "https://srinivasuniversity.edu.in/",
    "https://www.vsmsrkit.edu.in/",
    "https://www.rvitm.edu.in/",
    "https://www.sharnbasvauniversity.edu.in/",
    "https://bit-bangalore.edu.in/",
    "https://gec.karnataka.gov.in/"
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

# Output CSV
output_file = "website_headers_dataset1.csv"

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
            print(f"✅ Processed: {url}")
        else:
            print(f"⚠️  Skipped: {url}")
