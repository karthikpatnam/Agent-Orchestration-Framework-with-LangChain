# LangChain Agent Console Environment

A lightweight, console-based multi-agent environment built using Python, LangChain, LangGraph, and Google's Gemini models.

This system demonstrates dynamic tool calling functionality, seamlessly switching between a symbolic **Calculator** and a real-time **Weather API** based on the context of the user's console prompt.

## Features

- **Google Gemini Integration**: Uses `gemini-2.5-flash` for high-speed, intelligent reasoning.
- **Calculator Tool**: Leverages `sympy` to solve complex mathematical expressions and algebraic equations.
- **Weather Tool**: Communicates with the OpenWeather API to retrieve real-time weather metrics for any given city.
- **LangGraph React Agent**: Dynamically invokes the tools required and combines the results before presenting the final answer.

## Prerequisites

- **Python 3.9+**
- **Google GenAI API Key**: Get it from [Google AI Studio](https://aistudio.google.com/).
- **OpenWeather API Key**: Get it from [OpenWeatherMap](https://openweathermap.org/api).

## Setup Instructions

1. **Clone or Download the Workspace**
   Ensure you are in the project's root folder (`p:\Langchain_all_milestones` if running locally).

2. **Install Dependencies**
   It's highly recommended to use a virtual environment. Install the needed packages via `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Environment**
   Create a `.env` file in the root of the directory that looks exactly like this:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   WEATHER_API_KEY=your_openweather_api_key_here
   ```
   *(Ensure you replace the placeholders with your actual active keys).*

## How to Test

1. Launch your terminal/console.
2. Ensure you are in the project directory.
3. Start the LangChain setup by running:
   ```bash
   python agent_console.py
   ```
4. **Interact with the Agent!**
   Type queries directly into the console to test its capabilities. Examples you can try:
   - *"What is the weather in New York?"*
   - *"Calculate the solutions for x**2 - 2*x + 1 = 0"*
   - *"What's the weather in Seattle today, and also tell me what is 8943 * 123?"*
5. Type `exit` or `quit` to cleanly terminate the session.

## Error Handling

The application has comprehensive `try ... except` blocks for both APIs. 
- If the OpenWeather API limit is hit or an invalid API key is given, it will safely relay the status code error directly.
- The `sympy` calculator has an `eval` fallback safeguard to prevent agent crashing on malformed algebraic inputs.
