def process_file(filepath, filename):
    if filename.endswith(".csv"):
        df = pd.read_csv(filepath)
    elif filename.endswith(".xls") or filename.endswith(".xlsx"):
        df = pd.read_excel(filepath)
    elif filename.endswith(".pdf"):
        df = extract_data_from_pdf(filepath)
    else:
        return "unsupported file format"
    return df

def extract_data_from_pdf(filepath):
    with open(filepath, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()

    # Convert extracted text to structured format (requires custom logic)
    structured_data = parse_pdf_text_to_dataframe(extracted_text)

    return structured_data

def parse_pdf_text_to_dataframe(text):
    # Example: Manually extracting expenses from PDF text
    lines = text.split("\n")
    extracted_data = []

    for line in lines:
        parts = line.split()
        if len(parts) >= 4:
            extracted_data.append({
                "user_id": int(parts[0]),  # Adjust based on PDF format
                "expense_category": parts[1],
                "date": parts[2],
                "amount": float(parts[3])
            })

    return pd.DataFrame(extracted_data)
