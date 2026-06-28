import sys
import os
import json
from datetime import datetime, timedelta
from pypdf import PdfReader, PdfWriter


def printProgress(tried, total):
    barLen = 40
    progress = min(tried / total, 1.0)
    filled = int(barLen * progress)
    bar = "█" * filled + "░" * (barLen - filled)
    print(f"\rProgress: |{bar}| {progress*100:5.1f}% ({tried:,}/{total:,})", end="", flush=True)


def getDateFormats():
    return {
        "1": "ddmmyyyy",
        "2": "yyyymmdd",
        "3": "ddmmyy",
        "4": "mmddyyyy",
        "5": "mmddyy"
    }


def generatePassword(d, m, y, fmt):
    dd = f"{d:02d}"
    mm = f"{m:02d}"
    yy = f"{y % 100:02d}"
    yyyy = f"{y:04d}"
    formats = {
        "ddmmyyyy": dd + mm + yyyy,
        "yyyymmdd": yyyy + mm + dd,
        "ddmmyy": dd + mm + yy,
        "mmddyyyy": mm + dd + yyyy,
        "mmddyy": mm + dd + yy
    }
    return formats.get(fmt, "")


def unlockPdf(inputPath, password, outputPath):
    try:
        reader = PdfReader(inputPath)
        if reader.decrypt(password):
            writer = PdfWriter(clone_from=reader)
            with open(outputPath, "wb") as f:
                writer.write(f)
            return True
        return False
    except:
        return False


def loadProgress(progressFile):
    if os.path.exists(progressFile):
        try:
            with open(progressFile) as f:
                return json.load(f)
        except:
            pass
    return None


def saveProgress(progressFile, data):
    with open(progressFile, "w") as f:
        json.dump(data, f)


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    clearScreen()
    print("=======================================================")
    print("                ChronosCrack")
    print("       PDF Date-Based Password Recovery Tool")
    print("=======================================================\n")

    if len(sys.argv) != 2:
        print("Usage: python project.py <your_file.pdf>")
        sys.exit(1)

    filePath = sys.argv[1]

    if not os.path.isfile(filePath) or not filePath.lower().endswith(".pdf"):
        print("Error: Please provide a valid PDF file.")
        sys.exit(1)

    baseName = os.path.splitext(filePath)[0]
    outputPath = baseName + "_unlocked.pdf"
    progressFile = baseName + "_progress.json"

    if not PdfReader(filePath).is_encrypted:
        print("This PDF is not password protected.")
        sys.exit(0)

    while True:
        clearScreen()
        print("=======================================================")
        print("                       MAIN MENU")
        print("=======================================================")
        print("1. Auto Search (All Formats)")
        print("2. Custom Date Range Search")
        print("3. Search with Specific Format")
        print("4. Resume Previous Search")
        print("5. Exit")
        print("=======================================================")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "5":
            print("\nThank you for using ChronosCrack.")
            break

        tried = 0
        fmtList = []
        startDate = datetime.now()

        # Option 1: Auto Search
        if choice == "1":
            fmtList = list(getDateFormats().values())
            print("Starting search from today backwards...\n")

        # Option 2: Custom Date Range
        elif choice == "2":
            print("\nEnter dates in DD MM YYYY format")
            try:
                d1 = input("Start Date (DD MM YYYY): ").strip().split()
                d2 = input("End Date (DD MM YYYY): ").strip().split()
                startDate = datetime(int(d1[2]), int(d1[1]), int(d1[0]))
                endDate = datetime(int(d2[2]), int(d2[1]), int(d2[0]))
                fmtList = list(getDateFormats().values())
            except:
                print("Invalid input. Using default settings.")
                fmtList = list(getDateFormats().values())
                endDate = None

        # Option 3: Specific Format
        elif choice == "3":
            clearScreen()
            print("Available Formats:")
            for k, v in getDateFormats().items():
                print(f"  {k}. {v}")
            sel = input("\nSelect number: ").strip()
            fmtList = [getDateFormats().get(sel, "ddmmyyyy")]
            dateInput = input("\nStart date (YYYY-MM-DD) or Enter for today: ").strip()
            if dateInput:
                try:
                    startDate = datetime.fromisoformat(dateInput)
                except:
                    pass

        # Option 4: Resume
        elif choice == "4":
            progress = loadProgress(progressFile)
            if not progress:
                print("\nNo saved progress found.")
                input("\nPress Enter to continue...")
                continue
            fmtList = [progress["format"]]
            startDate = datetime.fromisoformat(progress["currentDate"])
            tried = progress.get("tried", 0)
            print(f"Resuming search...\n")
        else:
            continue

        found = False
        totalEstimate = len(fmtList) * 45000

        for fmt in fmtList:
            if found:
                break

            clearScreen()
            print(f"Searching format: {fmt.upper()}\n")
            currentDate = startDate

            while not found and currentDate.year >= 1900:
                password = generatePassword(currentDate.day, currentDate.month, currentDate.year, fmt)
                tried += 1

                if tried % 25 == 0:
                    printProgress(tried, totalEstimate)
                    saveProgress(progressFile, {
                        "format": fmt,
                        "currentDate": currentDate.isoformat(),
                        "tried": tried
                    })

                if unlockPdf(filePath, password, outputPath):
                    printProgress(tried, totalEstimate)
                    print(f"\n\nSUCCESS! Password found: {password}")
                    print(f"Unlocked file saved as: {os.path.basename(outputPath)}")
                    found = True
                    if os.path.exists(progressFile):
                        os.remove(progressFile)
                    break

                currentDate -= timedelta(days=1)

        if not found:
            printProgress(tried, totalEstimate)
            print("\n\nPassword not found in searched range.")

        input("\nPress Enter to return to main menu...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
