from dotenv import load_dotenv
import os

# Add references
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

def main():

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        # Get config settings
        load_dotenv()
        endpoint = os.getenv('ENDPOINT')
        key = os.getenv('KEY')

        # Set analysis settings
        fileUri = "https://github.com/MicrosoftLearning/mslearn-ai-information-extraction/blob/main/Labfiles/prebuilt-doc-intelligence/sample-invoice/sample-invoice.pdf?raw=true"
        fileLocale = "en-US"
        fileModelId = "prebuilt-invoice"

        print(f"\nConnecting to Forms Recognizer at: {endpoint}")
        print(f"Analyzing invoice at: {fileUri}")

        # Create the client
        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        # Analyse the invoice
        poller = document_analysis_client.begin_analyze_document_from_url(
            fileModelId, fileUri, locale=fileLocale
        )
        receipts = poller.result()

        # Display invoice information to the user
        for idx, receipt in enumerate(receipts.documents):
            print(f"--------Analyzing receipt #{idx + 1}--------")
            vendor_name = receipt.fields.get("VendorName")
            if vendor_name:
                print(f"Vendor Name: {vendor_name.value} has confidence: {vendor_name.confidence}")

            customer_name = receipt.fields.get("CustomerName")
            if customer_name:
                print(f"Customer Name: {customer_name.value} has confidence: {customer_name.confidence}")

            invoice_date = receipt.fields.get("InvoiceDate")
            if invoice_date:
                print(f"Invoice Date: {invoice_date.value} has confidence: {invoice_date.confidence}")

            invoice_total = receipt.fields.get("InvoiceTotal")
            if invoice_total:
                print(f"Invoice Total: {invoice_total.value} has confidence: {invoice_total.confidence}")

    except Exception as ex:
        print(ex)

    print("\nAnalysis complete.\n")

if __name__ == "__main__":
    main()
