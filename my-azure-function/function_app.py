import azure.functions as func
import json

app = func.FunctionApp()

@app.function_name(name="myHttpFunction")
@app.route(route="myHttpFunction", auth_level=func.AuthLevel.ANONYMOUS)
def my_http_function(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function that checks for authentication."""
    name = req.params.get('name', 'Guest')  # Provide a default value
    response_data = {"message": f"Hello, {name} from Azure Function!"}
    
    return func.HttpResponse(
        json.dumps(response_data),  # Ensure response is always valid JSON
        mimetype="application/json",
        status_code=200
    )
