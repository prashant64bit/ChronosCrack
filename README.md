# ChronosCrack

ChronosCrack is a lightweight Python tool for recovering password-protected PDF files using date-based brute-force patterns. It is designed around the common habit of some government or banking PDFs use the document holder’s date of birth as the password.

## Overview

- Attempts PDF passwords based on calendar dates
- Starts from the current date and moves backward in time
- Prioritizes recent dates for faster results
- Simple and minimal terminal experience
- Brute-forces date-based password patterns
- Saves an unlocked copy of the PDF

## Supported Date Formats

- `ddmmyyyy`  
  - Example: `15082003`
- `yyyymmdd`  
  - Example: `20030815`
- `ddmmyy`  
  - Example: `150803`
- `mmddyyyy`  
  - Example: `08152003`
- `mmddyy`  
  - Example: `081503`

## Requirements

- Python 3.7 or newer
- `pypdf` library

## License

This project is licensed under the [MIT License](LICENSE).

---

Made by **Prashant Thakur**  
GitHub: [https://github.com/prashant64bit](https://github.com/prashant64bit)  
Portfolio: [https://PrashantThakur.is-a.dev](https://PrashantThakur.is-a.dev)  
LinkedIn: [https://linkedin.com/in/prashant64bit](https://linkedin.com/in/prashant64bit)
