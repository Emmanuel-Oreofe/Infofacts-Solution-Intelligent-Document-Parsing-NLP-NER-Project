#import re

'''text = """
Bank A/C No: 1234567890
IFSC: SBIN0001234
Date: 12/02/2026
Amount: Rs. 45,000
"""

clean_text = re.sub(r"[^a-zA-Z0-9./: ]", "", text) # Remove special characters

account = re.findall(r"\d{9,18}", text) # Extract account

ifsc = re.findall(r"[A-Z]{4}0[A-Z0-9]{6}", text)# Extract IFSC

date = re.findall(r"\d{2}[-/]\d{2}[-/]\d{4}", text) # Extract date

amount = re.findall(r"Rs\.?\s?(\d{1,3}(?:,\d{3})*)", text)# Extract amount


account = account[0] if account else None
ifsc = ifsc[0] if ifsc else None
date = date[0] if date else None
amount = amount[0] if amount else None


if amount:                                  #normalize the amount
    amount = amount.replace(",", "")
    amount = float(amount)


data = {                      #structured output    
    "account_no": account,
    "ifsc": ifsc,
    "date": date,
    "amount": amount
}

print("Data:",data)
#print("Account:", account)
#print("IFSC:", ifsc)
#print("Date:", date)
#print("Amount:", amount)'''


import re
def fix_ocr_errors(text):

    
    text = text.replace("8ank", "Bank")  # Fix common OCR mistakes 
    text = text.replace("N0", "No")
    text = text.replace("IF5C", "IFSC")
    
    text = re.sub(r"(?<=\d)[oO]", "0", text) # Replace small o or capital O when next to digits
    text = re.sub(r"(?<=\d)[lI]", "1", text) # Replace l or I when inside numbers
    text = re.sub(r"SB1N", "SBIN", text) # Fix IFSC mistake 1 → I

    return text

def extract_data(text):

    text = fix_ocr_errors(text)
    text = text.upper()
   
    account = re.findall(r"\d{9,18}", text)
    account = account[0] if account else None

    ifsc_match = re.search(r"[A-Z0-9]{11}", text)

    if ifsc_match:
      ifsc = ifsc_match.group()
      ifsc = ifsc.replace("1", "I")
      ifsc = ifsc.replace("O", "0")
    else:
      ifsc = None
 
    date = re.findall(r"\d{2}[-/]\d{2}[-/]\d{4}", text)
    date = date[0] if date else None

    amount_match = re.search(r"RS\.?\s?([\d,]+)", text)
    if amount_match:
        amount = amount_match.group(1)
        amount = amount.replace(",", "")
        amount = float(amount)
    else:
        amount = None

    return {
        "account_no": account,
        "ifsc": ifsc,
        "date": date,
        "amount": amount
    }

# Test the function
text = """
Bank A/C No: 123456789o 
IFSC: SB1N0001234
Date: 12/02/2026
Amount: Rs. 45,00o
"""

result = extract_data(text)
print(result)
print(extract_data(text))