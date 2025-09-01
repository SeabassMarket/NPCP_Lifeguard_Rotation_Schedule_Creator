from fastapi import FastAPI, Request
import logging

from Google_Sheet_Interpreter import SpreadsheetInterpreter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/read_data")
async def read_data(request: Request):
    body = await request.json()
    logger.info(f"Received request: {body}")  # logs raw JSON

    # Convert JSON to objects
    try:
        interpreter = SpreadsheetInterpreter(body)

        spreadsheet = interpreter.spreadsheet

        for sheet in spreadsheet.sheets:
            logger.info(f"Info for {sheet.name}:")
            logger.info(f"Rows ({len(sheet.rows)}): {sheet.rows}")
            logger.info(f"Columns ({len(sheet.columns)}): {sheet.columns}")

        response = interpreter.interpret()

    except Exception as e:
        logger.error(f"could not parse information: {e}")
        return {"status": "error", "message": str(e)}

    # Return something simple for testing
    return {"status": "success", "response": response}


@app.get("/")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8080))  # Use Cloud Run PORT env variable
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
