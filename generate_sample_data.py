from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "Insurance Policy FAQ")
    
    # Content
    c.setFont("Helvetica", 12)
    y_position = height - 100
    
    qa_pairs = [
        ("Q: How do I file a claim?", 
         "A: You can file a claim by logging into your account on our website, navigating to the 'Claims' section, and filling out the online form. Alternatively, you can call our 24/7 claims hotline at 1-800-INSURE-ME."),
        
        ("Q: What is a deductible?", 
         "A: A deductible is the amount you pay out of pocket before your insurance coverage kicks in. For example, if you have a $500 deductible and a $2,000 claim, you pay $500 and we pay $1,500."),
        
        ("Q: How do I add a driver?", 
         "A: To add a driver to your policy, please contact our support agent or visit the 'My Policy' section in the mobile app. You will need the driver's license number and date of birth."),
        
        ("Q: What documents are required for a claim?", 
         "A: Typically, you will need a police report (if applicable), photos of the damage, and any relevant receipts or medical bills. Our claims adjuster will guide you through specific requirements.")
    ]
    
    for q, a in qa_pairs:
        # Question
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, q)
        y_position -= 20
        
        # Answer (simple wrapping by splitting lines roughly)
        c.setFont("Helvetica", 12)
        # Very basic wrapping for the sake of the sample
        words = a.split()
        line = ""
        for word in words:
            if c.stringWidth(line + word) < 500:
                line += word + " "
            else:
                c.drawString(70, y_position, line)
                y_position -= 15
                line = word + " "
        c.drawString(70, y_position, line)
        y_position -= 30
        
    c.save()

if __name__ == "__main__":
    output_dir = os.path.join("backend", "data")
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "Insurance_FAQ.pdf")
    create_pdf(pdf_path)
    print(f"PDF generated at: {pdf_path}")
