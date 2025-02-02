import azure.functions as func
import json
import logging

app = func.FunctionApp()

@app.function_name(name="SendNotification")
@app.route(route="send-notification", auth_level=func.AuthLevel.FUNCTION)

def send_notification(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function to process notifications when a user likes a post.
    """
    try:
        # Parse request body
        req_body = req.get_json()
        user_id = req_body.get("user_id")
        post_id = req_body.get("post_id")

        if not user_id or not post_id:
            return func.HttpResponse(
                json.dumps({"error": "Missing user_id or post_id"}), 
                mimetype="application/json",
                status_code=400
            )

        # Simulated notification message
        message = f"🔔 User {user_id} liked post {post_id}!"
        logging.info(message)  # ✅ Log the notification event

        return func.HttpResponse(
            json.dumps({"message": "Notification sent successfully!", "user_id": user_id, "post_id": post_id}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"❌ Error processing notification: {str(e)}")
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)
