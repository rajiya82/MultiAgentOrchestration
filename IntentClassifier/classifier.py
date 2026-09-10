import os
import boto3
import json
from botocore.exceptions import ClientError

br_service = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        user_query = body.get("user_query", "")

        intent_classifier_persona = [
            {
                "text": (
                    "You are an expert intent classifier agent. "
                    "Categorize the incoming user input into exactly ONE of these uppercase labels:\n"
                    "- APPOINTMENT_BOOKING\n"
                    "- GENERAL_INFO\n"
                    "- FINANCIAL_INFO\n"
                    "- SENSITIVE_DATA\n\n"
                    "You must strictly follow the output template structure below. "
                    "Do not include greeting phrases, small talk, or markdown formatting.\n"
                    "USER_INTENT: <enter selected intent here>\n"
                    "REASONING: <brief description of your decision profile>"
                )
            }
        ]

        guard_rail_id = os.environ.get("BEDROCK_GUARDRAIL_ID")
        guard_rail_version = os.environ.get("BEDROCK_GUARDRAIL_VERSION")

        converse_args = {
            "modelId": "amazon.nova-micro-v1:0",
            "system": intent_classifier_persona,
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": user_query}]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 50,
                "temperature": 0.0,
                "stopSequences": ["\nREASONING:", "REASONING"]
            }
        }

        if guard_rail_id and guard_rail_version:
            converse_args["guardrailConfig"] = {
                "guardrailIdentifier": guard_rail_id,
                "guardrailVersion": guard_rail_version
            }

        response = br_service.converse(**converse_args)
        answer = response["output"]["message"]["content"][0]["text"]
        # return output_text.replace("REASONING:", "").strip()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(answer)
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Bedrock service invocation error raised: {e}"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Internal system tracking breakdown {str(e)}"})
        }




