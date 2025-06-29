import requests

# Websites dictionary: filename -> URL
websites = {
    "vtu_pg_mysuru": "https://vtu.ac.in/pg-studies-mysuru/",
    "vtu_pg_kalaburagi": "https://kalaburagi.nic.in/en/public-utility/vtu-pg-center-kalaburagi/",
    "manipal": "https://www.manipal.edu/mu.html",
    "gttc_magadi": "https://gttc.karnataka.gov.in/86/magadi-stu-36/en",
    "khti_gadag": "https://khtigadag.ac.in/aboutus.php",
    "vtu_pg_muddenahalli": "https://vtu.ac.in/pg-studies-muddenahalli/",
    "dsu": "https://www.dsu.edu.in/",
    "gttc_devanahalli": "https://gttc.karnataka.gov.in/85/devanahalli-stu-35/en",
    "gpt_holealur": "https://gpt.karnataka.gov.in/gptgadag/public/en",
    "gec_hassan": "https://gec.karnataka.gov.in/gecm/public/21/contact-us/en",
    "sampoorna": "https://www.sampoornainstitutions.org/",
    "gpt_ramanagara": "https://gpt.karnataka.gov.in/gptramanagara/public/en",
    "reva": "https://www.reva.edu.in/",
    "gpt_mosalehosahalli": "https://gpt.karnataka.gov.in/gptmosalehosahalli/public/en",
    "gttc_gokak": "https://gttc.karnataka.gov.in/31/gokak-stu-27/en",
    "gec_gangavathi": "https://gec.karnataka.gov.in/gecgangavathi/public/en",
    "bti_bangalore": "https://www.btibangalore.org/",
    "gpt_women_holenarasipura": "https://gpt.karnataka.gov.in/gwptholenarasipura/public/en",
    "smvitm_bantakal": "https://smvitm.edu.in/",
    "sarang_tumkur": "https://www.sarangpolytechnic.ac.in/",
    "jaincer_belgaum": "https://jaincer.edu.in/",
    "ajiet_mangalore": "https://ajiet.edu.in/",
    "gpt_channagiri": "https://gpt.karnataka.gov.in/gptchannagiri/public/15/the-college/en",
    "gpt_malavalli": "https://dtek.karnataka.gov.in/page/Institutions/Polytechnics/Govt.Polytechnics/en",
    "gpt_kollegal": "https://gpt.karnataka.gov.in/gptchamarajanagar/public/en",
    "gpt_kadur": "https://gpt.karnataka.gov.in/gptkadur/public/en",
    "sharnbasva": "https://www.sharnbasvauniversity.edu.in/",
    "msruas": "https://www.msruas.ac.in/",
    "vsmsrkit": "https://www.vsmsrkit.edu.in/",
    "srinivas_engg": "https://srinivasuniversity.edu.in/Institute-Of-Engineering-Technology",
    "rvitm": "https://www.rvitm.edu.in/"
}

def fetch_and_save_headers(websites_dict):
    success_log = open("success.log", "w", encoding="utf-8")
    error_log = open("errors.log", "w", encoding="utf-8")

    for name, url in websites_dict.items():
        try:
            response = requests.get(url, timeout=10, verify=False)  # SSL verification disabled
            headers = response.headers

            with open(f"{name}.header", "w", encoding="utf-8") as file:
                for key, value in headers.items():
                    file.write(f"{key}: {value}\n")

            success_log.write(f"{name}: {url}\n")
            print(f"✅ Saved headers for {name}")

        except Exception as err:
            error_log.write(f"{name}: {url} -- {err}\n")
            print(f"❌ Error fetching {url}: {err}")

    success_log.close()
    error_log.close()

if __name__ == "__main__":
    fetch_and_save_headers(websites)
