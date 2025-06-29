import requests
import csv
import ssl
from urllib3.util.ssl_ import create_urllib3_context

# Ignore SSL cert warnings (for government websites that fail cert checks)
ssl._create_default_https_context = ssl._create_unverified_context

# List of websites you want to test
urls = [
    "https://www.iitm.ac.in/",                          # IIT Madras
    "https://www.annauniv.edu/",                        # Anna University
    "https://www.srmuniv.ac.in/",                       # SRM Institute of Science and Technology
    "https://www.psgtech.edu/",                         # PSG College of Technology
    "https://www.kluniversity.in/",                     # KLU (Note: KLU is actually in Andhra Pradesh; remove if strictly TN)
    "https://www.nittrichy.ac.in/",                     # NIT Trichy
    "https://www.sastra.edu/",                           # SASTRA University
    "https://www.cherraan.org/",                         # Cherraan's College of Engineering
    "https://www.velammal.edu.in/",                      # Velammal Engineering College
    "https://www.kct.ac.in/",                            # Kumaraguru College of Technology
    "https://www.kongu.ac.in/",                          # Kongu Engineering College
    "https://www.kalasalingam.ac.in/",                   # Kalasalingam Academy of Research and Education
    "https://www.ctenggcollege.edu.in/",                 # Coimbatore Institute of Technology
    "https://www.bannari.am.in/",                        # Bannari Amman Institute of Technology
    "https://www.sethu.ac.in/",                           # Sethu Institute of Technology
    "https://www.pacia.in/",                              # Panimalar Engineering College
    "https://www.measi.edu.in/",                          # MEASI Institute of Management
    "https://www.stthomascollege.edu.in/",               # St. Thomas College of Engineering
    "https://www.princedegreese.edu.in/",                # Prince Engineering College
    "https://www.robertsoncollege.org/",                 # Robertson College of Engineering
    "https://www.karunya.edu/",                           # Karunya Institute of Technology and Sciences
    "https://www.hindustanuniv.ac.in/",                  # Hindustan Institute of Technology and Science
    "https://www.saveetha.ac.in/",                        # Saveetha Engineering College
    "https://www.prist.ac.in/",                           # PRIST University
    "https://www.mahendra.info/",                         # Mahendra Engineering College
    "https://www.tce.edu/",                               # Thiagarajar College of Engineering
    "https://www.knowledgeinstitutes.edu.in/",           # Knowledge Institute of Technology
    "https://www.mepcoeng.ac.in/",                        # Mepco Schlenk Engineering College
    "https://www.klnec.edu.in/",                          # KLN College of Engineering
    "https://www.srmist.edu.in/",                         # SRM Institute of Science and Technology
    "https://www.nitt.edu/",                              # National Institute of Technology, Trichy
    "https://www.srmist.edu.in/",                         # SRM Institute of Science and Technology
    "https://www.vit.ac.in/",                             # Vellore Institute of Technology
    "https://www.pmu.edu/",                               # Periyar Maniammai Institute of Science & Technology
    "https://www.psgrkcw.ac.in/",                         # PSGR Krishnammal College for Women
    "https://www.mitindia.edu/",                          # Madras Institute of Technology
    "https://www.annauniv.edu/",                          # Anna University (multiple campuses)
    "https://www.drmgrdu.ac.in/",                         # Dr. M.G.R. Educational and Research Institute
    "https://www.rajagiri.edu.in/",                       # Rajagiri School of Engineering & Technology
    "https://www.sonaedu.in/",                            # Sona College of Technology
    "https://www.stthomasengg.edu.in/",                   # St. Thomas College of Engineering & Technology
    "https://www.psr.edu.in/",                            # PSR Engineering College
    "https://www.veltech.edu.in/",                        # Veltech University
    "https://www.adit.ac.in/",                            # ADIT (Anand Institute of Technology)
    "https://www.kct.ac.in/",                             # Kumaraguru College of Technology
    "https://www.rknec.edu.in/",                          # RKNEC College of Engineering
    "https://www.kcet.ac.in/",                            # KCET College of Engineering
    "https://www.srmist.edu.in/",                         # SRMIST Chennai
    "https://www.psgtech.edu/",                           # PSG College of Technology
    "https://www.nmrec.edu.in/",                          # NMREC (Nadimpalli Satyanarayana Raju Engineering College)
    "https://www.sssutms.co.in/",                         # SSSUTMS (Shri Shankaracharya Technical Campus)
    "https://www.psgtech.edu/",                           # PSG Tech (duplicate - to remove)
    "https://www.prist.ac.in/",                           # PRIST (duplicate - to remove)
    "https://www.mepcoeng.ac.in/",                        # MEPCO Schlenk Engineering College (duplicate - to remove)
    # Add more to reach 100, these are top ones
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
output_file = "website_headers_dataset5.csv"

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
