### How to run the app

### First install the dependencies (you require python3.11 or greater to run this app)
```
pip install google-adk litellm fastapi uvicorn httpx pydantic openai streamlit
```

run below commands to up all four agents
```
uvicorn agents.host_agent.__main__:app --port 8000
uvicorn agents.flight_agent.__main__:app --port 8001
uvicorn agents.stay_agent.__main__:app --port 8002     
uvicorn agents.activities_agent.__main__:app --port 8003
```

and finally run the steamlit app
```
streamlit run streamlit_app.py
```

**You need valid openai key to run the app**
