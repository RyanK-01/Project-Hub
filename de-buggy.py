import os
import PyPDF2

def diagnose_pdf(pdf_path):
    print(f"🔍 DIAGNOSTIC REPORT FOR: {pdf_path}")
    print("-" * 40)

    # CHECK 1: Does file exist?
    if not os.path.exists(pdf_path):
        print("❌ ERROR: File not found.")
        print(f"   I am looking in: {os.getcwd()}")
        print("   Make sure the PDF is in this exact folder.")
        return

    print("✅ File found.")

    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            
            # CHECK 2: Is it encrypted?
            if reader.is_encrypted:
                print("❌ ERROR: PDF is password protected/encrypted.")
                return

            # CHECK 3: How many pages?
            num_pages = len(reader.pages)
            print(f"✅ PDF has {num_pages} pages.")

            if num_pages == 0:
                print("❌ ERROR: PDF appears to be empty.")
                return

            # CHECK 4: Try to read Page 1
            print("Trying to read Page 1...")
            page1_text = reader.pages[0].extract_text()

            if not page1_text:
                print("❌ ERROR: No text found on Page 1.")
                print("   ⚠️  DIAGNOSIS: This is likely a SCANNED PDF (Image).")
                print("   PyPDF2 cannot read images. You need an OCR tool.")
            else:
                print("✅ SUCCESS! Text found:")
                print(f"   Sample: {page1_text[:100]}...") # Print first 100 chars

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")

# --- RUN IT ---
# Make sure to change 'test.pdf' to your actual file name!
diagnose_pdf('file-sample_150kB.pdf')