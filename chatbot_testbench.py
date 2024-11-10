from openai import OpenAI
import time
import sys

# Based on openAI cookbook: https://cookbook.openai.com/examples/assistants_api_overview_python

#Get assistant name and behaviour from input parameter, e.g. /pathtopythonenvironment/python3 chatbot_conversation.py asst_xyz noinstructions_html_temp_max
#Result: 3 output files containing the behaviour as name and the 100 question / answer combinations
myassistant = str(sys.argv[1])
botname_pfad = str(sys.argv[2])

#Every questions gets its own output file
bankpakete_outputpfad = "output/bankpakete_" + botname_pfad
easy_outputpfad = "output/easy_" + botname_pfad
youngo_outputpfad = "output/youngo_" + botname_pfad

#Your API-key here
client = OpenAI(api_key='')

#Questions about Baloise Bank:
user_message_bankpakete="Welche Bankpakete bietet die Baloise Bank an?"
user_message_easy="Ist beim Bankpaket Easy der Baloise Bank eine Kreditkarte enthalten?"
user_message_youngo="Welche Konditionen gelten für die Kreditkarte im Bankpaket YounGo der Baloise Bank?"

#Add message to thread
def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

#Ask the question
def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(myassistant, thread, user_input)
    return thread, run

# Pretty printing helper. Get response
def pretty_print_bankpakete(messages, counter):
    f = open (bankpakete_outputpfad, "a")    
    f.write("Messung "+str(i) +"\n")
    for m in messages:     
        f.write( m.content[0].text.value)
        f.write("\n\n")
    f.write("\n")
    f.close()

def pretty_print_easy(messages, counter):
    f = open (easy_outputpfad, "a")    
    f.write("Messung "+str(i) +"\n")
    for m in messages:     
        f.write( m.content[0].text.value)
        f.write("\n\n")
    f.write("\n")
    f.close()

def pretty_print_youngo(messages, counter):
    f = open (youngo_outputpfad, "a")    
    f.write("Messung "+str(i) +"\n")
    for m in messages:     
        f.write( m.content[0].text.value)
        f.write("\n\n")
    f.write("\n")
    f.close()


# Wait until finished
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

# Get response and repeat 100 times
for i in range (1, 101):
# Every question gets a thread
    thread1, run1 = create_thread_and_run(user_message_bankpakete)
    thread2, run2 = create_thread_and_run(user_message_easy)
    thread3, run3 = create_thread_and_run(user_message_youngo)

    run1 = wait_on_run(run1, thread1)
    pretty_print_bankpakete(get_response(thread1),i)

    run2 = wait_on_run(run2, thread2)
    pretty_print_easy(get_response(thread2),i)

    run3 = wait_on_run(run3, thread3)
    pretty_print_youngo(get_response(thread3),i)
    print("Messung "+str(i)+" erledigt")
    time.sleep(10)



