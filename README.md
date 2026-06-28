# ChronosCrack - Date-Based PDF Password Recovery

ChronosCrack is a Python command-line utility for recovering passwords from encrypted PDF files by testing passwords generated from dates. It was created for a common real-world scenario where a PDF password is based on a memorable date, such as a birthday, anniversary, joining date, or another important event.

Many users choose date-based passwords because they are easy to remember when the document is created. However, after months or years, remembering the exact format that was used can become difficult. A password might have been written as `15081998`, `19980815`, `150898`, or another variation. Manually trying every possibility is repetitive and time-consuming. ChronosCrack automates this process by generating multiple date formats and testing them against the encrypted PDF.

The application is intended only for recovering passwords from PDF files that you own or that you have explicit permission to access. It does not exploit vulnerabilities or bypass PDF encryption. Instead, it performs an automated search using passwords that are derived from dates.

---

## Features

- Interactive command-line interface
- Multiple password search modes
- Support for several common date formats
- Search across a complete date range
- Start searching from a custom date
- Option to search using only one selected date format
- Resume interrupted searches
- Live progress display showing completed attempts
- Automatically saves the decrypted PDF when the correct password is found
- Lightweight with minimal dependencies

---

## Supported Password Formats

ChronosCrack currently generates passwords using several common date representations, including:

- DDMMYYYY
- MMDDYYYY
- YYYYMMDD
- DDMMYY
- MMDDYY
- YYMMDD

The password generation logic is isolated in a dedicated function, making it straightforward to extend with additional formats if needed.

---

## Project Structure

```
ChronosCrack/
│
├── project.py
├── test_project.py
├── requirements.txt
├── README.md
└── LICENSE
```

### project.py

Contains the main application logic.

Major responsibilities include:

- displaying the command-line menu
- generating passwords
- attempting PDF decryption
- displaying search progress
- saving search progress
- resuming interrupted searches

The file contains the `main()` function along with several helper functions:

- `printProgress()`
- `getDateFormats()`
- `generatePassword()`
- `unlockPdf()`
- `saveProgress()`
- `loadProgress()`

---

### test_project.py

Contains unit tests written using `pytest`.

The tests verify important functionality such as:

- date format generation
- password generation
- helper functions
- expected return values
- handling of invalid inputs where appropriate

---

### requirements.txt

The project has only one external dependency:

```
pypdf
```

All remaining functionality uses Python's standard library.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/prashant64bit/ChronosCrack.git
cd ChronosCrack
```

Install the required package:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the application by providing an encrypted PDF file.

```bash
python project.py protected.pdf
```

The program will present an interactive menu with several search options.

Depending on the selected mode, ChronosCrack can:

- search every supported date format
- search using only one selected format
- begin from a custom start date
- resume a previous search

During execution the program continuously updates the progress display so the user can monitor the search.

If the correct password is found, a decrypted copy of the PDF is automatically created.

Example:

```
Password Found!

Password:
15081998

Saved as:
protected_unlocked.pdf
```

If no password is found within the selected range, the program completes normally and reports that no matching password was discovered.

---

## How It Works

ChronosCrack generates candidate passwords from dates within a specified range.

For every generated password, the application attempts to decrypt the PDF using the `pypdf` library.

The workflow is straightforward:

1. Generate a date.
2. Convert the date into one or more password formats.
3. Attempt to unlock the PDF.
4. Repeat until a password succeeds or every possibility has been tested.

Since many date ranges can include tens of thousands of possible passwords, the application periodically updates the progress display while continuing the search.

---

## Resume Functionality

Searching a large date range can take a significant amount of time.

To avoid restarting from the beginning after the program is interrupted, ChronosCrack stores the current search state in a JSON file.

When launched again, the program detects the saved progress and allows the user to continue from the previous stopping point.

This makes long-running searches much more practical.

---

## Dependencies

ChronosCrack intentionally minimizes external dependencies.

Required:

- Python 3.10 or newer
- pypdf

Standard library modules used include:

- datetime
- json
- os
- sys

No database or additional frameworks are required.

---

## Design Decisions

The project was designed with readability and maintainability in mind.

Password generation, progress management, and PDF handling are separated into individual functions instead of combining everything into one large loop. This keeps the code easier to understand, test, and extend.

A progress-saving mechanism was included because searching several decades of dates can involve a large number of attempts. Rather than forcing users to restart from the beginning after closing the program or encountering an interruption, the application stores the current state so the search can continue later.

The progress display is updated periodically instead of after every attempt. Updating too frequently adds unnecessary overhead, while updating too rarely provides little feedback. A moderate update interval offers a good balance between responsiveness and performance.

The project also includes unit tests for the most important helper functions to reduce the likelihood of regressions when making future changes.

---

## Limitations

ChronosCrack is intentionally specialized.

It works best when the password is directly based on a calendar date.

It is not intended to recover:

- randomly generated passwords
- long alphanumeric passwords
- passwords containing unrelated words
- passwords with special characters unrelated to dates
- passwords generated by password managers

The time required for a search depends on the selected date range and the number of password formats being tested.

---

## Future Improvements

Possible future enhancements include:

- support for custom password templates
- support for name and date combinations
- multithreaded password testing
- improved command-line arguments
- exportable search logs
- graphical user interface
- batch processing multiple PDF files
- additional password generation strategies
- configurable progress update intervals

These features were intentionally left out of the current version to keep the project focused, understandable, and easy to maintain.

---

## Disclaimer

ChronosCrack is intended solely for recovering passwords from PDF documents that you own or that you are legally authorized to access. Users are responsible for ensuring that their use of this software complies with all applicable laws and the permissions associated with the documents they attempt to recover.

---

## License

This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for additional information.

---

Made by **Prashant Thakur**  
Portfolio: [https://PrashantThakur.is-a.dev](https://PrashantThakur.is-a.dev)  
LinkedIn: [https://linkedin.com/in/prashant64bit](https://linkedin.com/in/prashant64bit)
