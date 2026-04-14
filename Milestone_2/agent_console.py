import os
import requests
import sympy
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# Load environment variables
# Note: For Gemini, set GOOGLE_API_KEY. For Weather, set WEATHER_API_KEY.
load_dotenv()

@tool
def calculator(query: str) -> str:
    """
    Advanced mathematical solver that can handle basic arithmetic,
    algebraic equations, and calculus. 
    Examples: '45 * 8 / 2', 'x**2 - 2*x + 1 = 0'
    """
    try:
        query = query.replace('^', '**')
        
        # Handle equations
        if '=' in query:
            left, right = query.split('=')
            eq = sympy.Eq(sympy.sympify(left.strip()), sympy.sympify(right.strip()))
            
            vars = eq.free_symbols
            if not vars:
                return str(sympy.solve(eq))
            
            solution = sympy.solve(eq, list(vars))
            return f"Solutions for {list(vars)}: {solution}"
        
        # Handle expressions
        result = sympy.sympify(query).evalf()
        if hasattr(result, 'is_number') and not result.is_number:
            return str(sympy.simplify(query))
        
        return str(result)
            
    except Exception as e:
        # Fallback to basic eval if sympy fails
        try:
            return str(eval(query, {"__builtins__": None}, {}))
        except Exception as eval_err:
            return f"Error computing '{query}': {str(e)} | Eval fallback error: {str(eval_err)}"

@tool
def weather_agent(city: str) -> str:
    """
    Fetches real-time weather information for a given city using OpenWeather API.
    Input should be just the city name.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Error: WEATHER_API_KEY is not set in the environment variables."
        
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
             return f"Error: City '{city}' not found."
        elif response.status_code == 401:
             return "Error: Invalid OpenWeather API key."
        elif response.status_code != 200:
             return f"Error: Weather service returned status code {response.status_code}."
             
        data = response.json()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        wind = data["wind"]["speed"]
        
        return f"Weather in {city.title()}: {temp}°C, {condition}, Humidity {humidity}%, Wind {wind} m/s"
        
    except requests.exceptions.RequestException as e:
        return f"Error connecting to weather service: {str(e)}"
    except Exception as e:
        return f"Unexpected error processing weather data: {str(e)}"

def main():
    print("Initializing Multi-Agent Console...")
    
    # Check for API keys
    if "GOOGLE_API_KEY" not in os.environ:
        print("Warning: GOOGLE_API_KEY is not set. The Gemini model may fail to initialize.")
    if "WEATHER_API_KEY" not in os.environ:
        print("Warning: WEATHER_API_KEY is not set. Weather queries will fail.")
        
    # Initialize the LLM (Gemini)
    try:
         llm = ChatGoogleGenerativeAI(
             model="gemini-2.5-flash",
             temperature=0
         )
    except Exception as e:
         print(f"Failed to initialize LLM: {str(e)}")
         return

    # Integrate tools
    tools = [calculator, weather_agent]
    agent = create_react_agent(llm, tools)

    print("\n=======================================================")
    print("Agent Environment Ready!")
    print("Tools available: Calculator, Weather")
    print("Type 'exit' or 'quit' to terminate the application.")
    print("=======================================================\n")

    # Start the console loop
    while True:
        try:
            user_input = input("\nUser: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            # Invoke the LangGraph agent
            # The agent expects a state dictionary, usually holding messages.
            inputs = {"messages": [("user", user_input)]}
            
            # Print a thinking indicator
            print("Agent is thinking...", end="\r")
            
            result = agent.invoke(inputs)
            
            # Print the final output layer over the thinking indicator
            final_message = result["messages"][-1].content
            print(" " * 50, end="\r") # Clear the line
            print(f"Agent: {final_message}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nSystem Error: An unexpected error occurred -> {str(e)}")

if __name__ == "__main__":
    main()
