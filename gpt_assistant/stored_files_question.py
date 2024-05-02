from openai import OpenAI
import time
from config import config
import os
client = OpenAI(api_key=config.OPENAI_API_KEY)

# Define el ID del vector file existente
vector_store_id = "vs_i4Wu7afB8GIap6otRLD2tDNQ"

def chatWithStoredFile(question) -> str:
    startTime = time.time()

    assistant = client.beta.assistants.create(
        name="Scouting assistant",
        instructions='Eres un asistente virtual de una aplicacion de scouting para FRC, tu proposito es que con estos datos que estan en un json de una google sheets que es nuestra data base, respondas cualquier pregunta que te hagan acerca de los equipoos scouteados',
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store_id]
                }
         },
        model="gpt-3.5-turbo",
    )

    # Sube la pregunta junto con la referencia al vector file existente
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store_id]
                }
         },
    )
        
    # Crea un hilo y adjunta el archivo a este mensaje
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")
    endtime = time.time()
    duration = endtime - startTime
    print(message_content.value )
    print('Tiempoo de respuesta:' + str(duration))


