from groq import Groq
from dotenv import load_dotenv
import os
import re

# =========================
# LOAD ENV
# =========================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# TOOLS
# =========================

def weather_tool(city):

    weather_data = {
        "chennai": 35,
        "delhi": 28,
        "mumbai": 30
    }

    temperature = weather_data.get(
        city.lower(),
        25
    )

    return {
        "city": city,
        "celsius": temperature
    }


def fahrenheit_converter(celsius):

    fahrenheit = (celsius * 9/5) + 32

    return round(fahrenheit, 2)


def calculator_tool(expression):

    try:

        result = eval(expression)

        return result

    except Exception as e:

        return f"Calculator Error: {str(e)}"

# =========================
# AGENT
# =========================

def agent(question):

    print("\n========================")
    print("USER QUESTION:")
    print(question)

    observations = []

    # =====================
    # CASE 1
    # TEMPERATURE QUERY
    # =====================

    if "temperature" in question.lower() \
       or "weather" in question.lower():

        # -----------------
        # THOUGHT 1
        # -----------------

        print("\nTHOUGHT 1:")
        print("I need weather information.")

        # Extract city

        city = "Chennai"

        cities = [
            "chennai",
            "delhi",
            "mumbai"
        ]

        for c in cities:

            if c in question.lower():
                city = c

        # -----------------
        # ACTION 1
        # -----------------

        print("\nACTION 1:")
        print("Calling weather tool...")

        weather_result = weather_tool(city)

        # -----------------
        # OBSERVATION 1
        # -----------------

        print("\nOBSERVATION 1:")
        print(weather_result)

        observations.append(weather_result)

        # -----------------
        # THOUGHT 2
        # -----------------

        if "fahrenheit" in question.lower():

            print("\nTHOUGHT 2:")
            print(
                "Need to convert Celsius "
                "to Fahrenheit."
            )

            celsius = weather_result["celsius"]

            # -------------
            # ACTION 2
            # -------------

            print("\nACTION 2:")
            print(
                "Calling Fahrenheit "
                "conversion tool..."
            )

            fahrenheit = fahrenheit_converter(
                celsius
            )

            # -------------
            # OBSERVATION 2
            # -------------

            print("\nOBSERVATION 2:")
            print(
                f"{celsius}°C = "
                f"{fahrenheit}°F"
            )

            observations.append(
                {
                    "fahrenheit": fahrenheit
                }
            )

            # -------------
            # FINAL ANSWER
            # -------------

            final_answer = (
                f"{city.title()} temperature is "
                f"{celsius}°C "
                f"and {fahrenheit}°F."
            )

        else:

            final_answer = (
                f"{city.title()} temperature is "
                f"{weather_result['celsius']}°C."
            )

    # =====================
    # CASE 2
    # CALCULATOR QUERY
    # =====================

    else:

        print("\nTHOUGHT:")
        print("This is a math problem.")

        expression = re.sub(
            r"[^0-9+\-*/().]",
            "",
            question
        )

        if expression:
            expression = expression[0]

        # -----------------
        # ACTION
        # -----------------

        print("\nACTION:")
        print("Calling calculator tool...")

        result = calculator_tool(expression)

        # -----------------
        # OBSERVATION
        # -----------------

        print("\nOBSERVATION:")
        print(result)

        final_answer = (
            f"The result is {result}"
        )

    # =====================
    # FINAL ANSWER
    # =====================

    print("\nFINAL ANSWER:")
    print(final_answer)

    print("========================\n")


# =========================
# MAIN LOOP
# =========================

while True:

    question = input(
        "Ask Question (exit to quit): "
    )

    if question.lower() == "exit":
        break

    agent(question)