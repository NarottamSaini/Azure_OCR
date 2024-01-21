
## reference link:: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/use-sdk-rest-api?view=doc-intel-3.0.0&preserve-view=true%3Fpivots%3Dprogramming-language-python&tabs=windows&pivots=programming-language-python

## Code link:: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/use-sdk-rest-api?view=doc-intel-3.0.0&preserve-view=true%3Fpivots%3Dprogramming-language-python&tabs=windows&pivots=programming-language-python#use-the-read-model

# image_path = 'E:\Learning\OCR_HTR_githubharald\Azure_OCR\data\20230911_122152.jpg'
# image_path = 'E:/Learning/OCR_HTR_githubharald/Azure_OCR/data/20230911_122152.jpg' 
# image_path = 'E:/Learning/OCR_HTR_githubharald/Azure_OCR/data/20230911_122152.pdf'

import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# use your `key` and `endpoint` environment variables
# key = os.environ.get('FR_KEY')
# endpoint = os.environ.get('FR_ENDPOINT')

key = 'ab19941ad4a3495e92da12061397d193'
endpoint = 'https://naro-document-intelli.cognitiveservices.azure.com/'

# formatting function
def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])


def analyze_read():
    # sample document
    formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/read.png"
    # formUrl = "https://github.com/Narottam36/mlproject_7days/blob/main/Screenshot_2023-09-17_121256.png"
    
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document_from_url(
        "prebuilt-read", formUrl
    )

    # poller = document_analysis_client.begin_analyze_document(
    #     "prebuilt-read", image_path
    #     )

    result = poller.result()

    print("Document contains content: ", result.content)

    for idx, style in enumerate(result.styles):
        print(
            "Document contains {} content".format(
                "handwritten" if style.is_handwritten else "no handwritten"
            )
        )

    for page in result.pages:
        print("----Analyzing Read from page #{}----".format(page.page_number))
        print(
            "Page has width: {} and height: {}, measured with unit: {}".format(
                page.width, page.height, page.unit
            )
        )

        for line_idx, line in enumerate(page.lines):
            print(
                "...Line # {} has text content '{}' within bounding box '{}'".format(
                    line_idx,
                    line.content,
                    format_polygon(line.polygon),
                )
            )

        for word in page.words:
            print(
                "...Word '{}' has a confidence of {}".format(
                    word.content, word.confidence
                )
            )

    print("----------------------------------------")


if __name__ == "__main__":
    print("Execution started")
    analyze_read()