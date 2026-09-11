import json
import wikipedia

def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        user_query = body.get("user_query", "").strip()

        if not user_query:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'user_query' parameter"})
            }

        search_title = wikipedia.search(user_query)

        if not search_title:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'search_title' parameter"})
            }
        else:
            summery = wikipedia.summary(search_title[0], sentences=3)
            answer = f"Wikipedia agent summery for {search_title[0]}: \n\n {summery}"

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"response": answer})
        }

        pass
    except wikipedia.exceptions.DisambiguationError as e:
        return{
            "statusCode":200,
            "body":json.dumps({"response": f"🌐 **Wikipedia Agent:** Your query was ambiguous. Did you mean: {', '.join(e.options[:3])}?"})
        }
    except wikipedia.exceptions.PageError:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"response": f"🌐 **Wikipedia Agent:** The entry for '{user_query}' could not be located."})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Internal agent system tracking breakdown: {str(e)}"})
        }