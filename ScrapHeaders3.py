import requests
import csv
import ssl
from urllib3.util.ssl_ import create_urllib3_context

# Ignore SSL cert warnings (for government websites that fail cert checks)
ssl._create_default_https_context = ssl._create_unverified_context

# List of websites you want to test
urls = [
    "https://nmamit.nitte.edu.in/",
    "https://www.rvce.edu.in/",  # duplicate, skip this
    "https://bietdvg.edu.in/",
    "https://bit-bangalore.edu.in/",  # duplicate, skip this
    "https://kvgengg.edu.in/",
    "https://mangaloreuniversity.ac.in/",
    "https://www.vidyavardhaka.edu.in/",
    "https://www.klnce.edu.in/",
    "https://www.cmr.edu.in/",
    "https://www.siddaganga.org/",  # duplicate, skip this
    "https://www.bmsit.org/",  # duplicate, skip this
    "https://www.oxford.edu.in/",
    "https://www.acharyainstitute.edu.in/",  # Acharya Institute of Technology different domain
    "https://nagarjunacollege.edu.in/",
    "https://www.sharnbasvauniversity.edu.in/",  # duplicate, skip this
    "https://www.srmist.edu.in/",
    "https://www.kletech.ac.in/",  # duplicate, skip this
    "https://www.klnengg.ac.in/",
    "https://www.sjbit.edu.in/",  # duplicate, skip this
    "https://www.msit.in/",
    "https://www.ramaiah.edu.in/",
    "https://www.kssem.edu.in/",
    "https://www.pes.edu/",
    "https://www.gce.kar.nic.in/",
    "https://www.kledeemeduniversity.edu.in/",
    "https://www.vidyabharati.org/",
    "https://www.dietgov.in/",
    "https://www.bnmcollege.com/",
    "https://www.kluniversity.in/",
    "https://www.sjce.ac.in/",
    "https://www.kvgengg.edu.in/",  # duplicate, skip this
    "https://www.rajagiritech.ac.in/",
    "https://www.sitblr.edu.in/",
    "https://www.rvce.edu.in/",  # duplicate, skip this
    "https://www.gtu.ac.in/",
    "https://www.sjbit.edu.in/",  # duplicate, skip this
    "https://www.acharya.ac.in/",  # duplicate, skip this
    "https://www.rguhs.ac.in/",
    "https://www.su.edu.in/",
    "https://www.klescet.ac.in/",
    "https://www.klnce.ac.in/",
    "https://www.kiet.edu/",
    "https://www.pes.edu/",
    "https://www.nitte.edu.in/",
    "https://www.gcehassan.ac.in/",
    "https://www.govtpolytechnic.in/",
    "https://www.gptw.edu.in/",
    "https://www.klescetam.edu.in/",
    "https://www.msruas.ac.in/",  # duplicate, skip this
    "https://www.rnsit.ac.in/",  # duplicate, skip this
    "https://www.gcekolar.in/",
    "https://www.vtu.ac.in/",
    "https://www.kcet.in/",
    "https://www.nmit.ac.in/",  # duplicate, skip this
    "https://www.gcemysore.ac.in/",
    "https://www.sdit.edu.in/",
    "https://www.gcechitradurga.in/",
    "https://www.gcehassan.ac.in/",
    "https://www.gcekolar.in/",
    "https://www.gcejm.edu.in/",
    "https://www.gcebapatala.ac.in/",
    "https://www.acharya.ac.in/",  # duplicate, skip this
    "https://www.klsahd.edu.in/",
    "https://www.gces.edu.in/",
    "https://www.klnengg.ac.in/",  # duplicate, skip this
    "https://www.rvce.edu.in/",  # duplicate, skip this
    "https://www.kyadav.ac.in/",
    "https://www.sssutms.co.in/",
    "https://www.bmsce.in/",  # duplicate, skip this
    "https://www.kletech.ac.in/",  # duplicate, skip this
    "https://www.acharyainstitute.edu.in/",  # duplicate, skip this
    "https://www.klnce.ac.in/",  # duplicate, skip this
    "https://www.srmuniv.ac.in/",
    "https://www.aitpune.com/",
    "https://www.bmsce.ac.in/",  # duplicate, skip this
    "https://www.vidyavardhaka.edu.in/",  # duplicate, skip this
    "https://www.rvce.edu.in/",  # duplicate, skip this
    "https://www.bmsce.ac.in/",  # duplicate, skip this
    "https://www.klescetam.edu.in/",  # duplicate, skip this
    "https://www.jssstuniv.in/",  # duplicate, skip this
    "https://www.sitblr.edu.in/",  # duplicate, skip this
    "https://www.klnce.ac.in/",  # duplicate, skip this
    "https://www.rvce.edu.in/",  # duplicate, skip this
    "https://www.acharya.ac.in/",  # duplicate, skip this
    "https://www.rvce.edu.in/",  # duplicate, skip this
    "https://www.gcehassan.ac.in/",  # duplicate, skip this
    "https://www.aitpune.com/",  # duplicate, skip this
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
output_file = "website_headers_dataset4.csv"

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
