from openai import AuthenticationError, OpenAI
import openai
import config.config as config

client = OpenAI(api_key=config.OPENAI_API_KEY)

def chat_with_gpt(promt: str, cont: str,) -> str:
    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # {"role": "system", "content": 'Eres un asistente virtual de una aplicacion de scouting para FRC, tu proposito es que con estos datos que estan en un json de una google sheets que es nuestra data base, respondas cualquier pregunta que te hagan acerca de los equipoos scouteados. para los numeros que estan '+ cont},
            {"role": "system", "content": 'Eres un asistente virtual, ayuda en lo que puedas'},

            {"role": "user", "content": promt}
        ]
        )
        return response.choices[0].message.content
    except AuthenticationError:
        return "Invalid OpenAI API key. Please check your configuration."
    except (ConnectionError, TimeoutError) as e:
        return f"Network error: {e}. Please try again later."
    except Exception as e:  # Catch other unexpected errors
        return f"An error occurred: {e}. Please contact support."