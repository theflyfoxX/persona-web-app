from motor.motor_asyncio import AsyncIOMotorClient

uri = "mongodb+srv://flifoxrassas:K6qdNxSGmnBJ5qW4@persona.9szfe.mongodb.net/?retryWrites=true&w=majority&appName=persona"

client = AsyncIOMotorClient(uri)
database = client["persona-mongo"]  # Your MongoDB database
messages_collection = database["Messages"]  # Your Messages collection

# Optional: Function to test MongoDB connection
async def test_connection():
    try:
        result = await messages_collection.find_one()
        print("✅ MongoDB Connected:", result)
    except Exception as e:
        print("❌ Connection Failed:", e)
