
import os
import azure.ai.vision as sdk

VISION_KEY = "4d4c7f514b7344a6875e8d3c61680a83"
VISION_ENDPOINT = "https://naro-cv.cognitiveservices.azure.com/"

# service_options = sdk.VisionServiceOptions(os.environ["VISION_ENDPOINT"],
#                                            os.environ["VISION_KEY"])

service_options = sdk.VisionServiceOptions(VISION_ENDPOINT,
                                           VISION_KEY)

# vision_source = sdk.VisionSource(
#     url="https://learn.microsoft.com/azure/cognitive-services/computer-vision/media/quickstarts/presentation.png")

vision_source = sdk.VisionSource(
    url="https://github.com/Narottam36/mlproject_7days/blob/main/Screenshot_2023-09-17_121256.png")

analysis_options = sdk.ImageAnalysisOptions()

analysis_options.features = (
    sdk.ImageAnalysisFeature.CAPTION |
    sdk.ImageAnalysisFeature.TEXT
)

analysis_options.language = "en"

analysis_options.gender_neutral_caption = True

image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)

result = image_analyzer.analyze()

if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:

    if result.caption is not None:
        print(" Caption:")
        print("   '{}', Confidence {:.4f}".format(result.caption.content, result.caption.confidence))

    if result.text is not None:
        print(" Text:")
        for line in result.text.lines:
            points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
            print("   Line: '{}', Bounding polygon {}".format(line.content, points_string))
            for word in line.words:
                points_string = "{" + ", ".join([str(int(point)) for point in word.bounding_polygon]) + "}"
                print("     Word: '{}', Bounding polygon {}, Confidence {:.4f}"
                      .format(word.content, points_string, word.confidence))

else:

    error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
    print(" Analysis failed.")
    print("   Error reason: {}".format(error_details.reason))
    print("   Error code: {}".format(error_details.error_code))
    print("   Error message: {}".format(error_details.message))