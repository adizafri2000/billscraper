from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

class Message(BaseModel):
    number: str
    message: str

# Start the Go process when the application starts
go_process = None

@app.on_event("startup")
def startup_event():
    global go_process
    # Ensure the Go binary is executable
    os.chmod("/app/mdtest/go_app", 0o755)
    # Start the Go process with stdin set to subprocess.PIPE
    go_process = subprocess.Popen(
        ["/app/mdtest/go_app"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

@app.get("/")
def read_root():
    return {"message": "FastAPI is up and running!"}

@app.post("/send_message")
def send_message(msg: Message):
    if go_process.poll() is not None:
        raise HTTPException(status_code=500, detail="Go process is not running")
    try:
        # Send message to Go process and capture the output
        command = f"send {msg.number} {msg.message}"
        output = execute_go_program(command.split())
        
        return {"output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to execute the Go program and capture its output
def execute_go_program(command):
    try:
        if go_process.poll() is None:
            # Send the command to the Go process
            go_process.stdin.write('\n'.join(command) + '\n')
            go_process.stdin.flush()  # Flush the input to ensure it's sent immediately

            # Read the output from the Go process
            output = go_process.stdout.readline().strip()

            return output
        else:
            raise HTTPException(status_code=500, detail="Go process is not running")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Go process: {str(e)}")
