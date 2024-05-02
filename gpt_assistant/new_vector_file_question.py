from openai import OpenAI
from config import config
client = OpenAI(api_key=config.OPENAI_API_KEY)

def chatWithNewFile(question) -> str:
    assistant = client.beta.assistants.create(
    name="Scouting assistant",
    instructions='Eres un asistente virtual de una aplicacion de scouting para FRC, tu proposito es que con estos datos que estan en un json de una google sheets que es nuestra data base, respondas cualquier pregunta que te hagan acerca de los equipoos scouteados',
    tools=[{"type": "file_search"}],
    model="gpt-3.5-turbo",
    )

    vector_store = client.beta.vector_stores.create(name="Scouted teams")

    file_paths = ["scouted_teams.json"]
    file_streams = [open(path, "rb") for path in file_paths] 
    
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
    )   

    assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    # Upload the user provided file to OpenAI
    message_file = client.files.create(
    file=open("scouted_teams.json", "rb"), purpose="assistants"
    )
    
    # Create a thread and attach the file to the message
    thread = client.beta.threads.create(
    messages=[
        {
        "role": "user",
        "content": question,
        # Attach the new file to the message.
        "attachments": [
            { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
        ],
        }
    ]
    )
        
    # Use the create and poll SDK helper to create a run and poll the status of
    # the run until it's in a terminal state.

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

    print(message_content.value)

