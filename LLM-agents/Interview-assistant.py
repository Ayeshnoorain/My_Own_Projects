import autogen
from autogen import  ConversableAgent, AssistantAgent, UserProxyAgent
import pprint

llm_config = {
    "model": "gpt-4o-mini", 
    "api_key": "openAI-api-key"
    }

task1 = """ You are a helpful mock interviewer that will train the user with mock interview questions based on the users prefered topic of interest.
* Train only on the topic the user has selected. 
* Ask questions and correct the answer to help the user to learn. 
* After correcting the answer continue asking the next interview question. 
* Return 'TERMINATE' when you have finished the mock interview.
 """

couch_2 = autogen.ConversableAgent(
    name="Scenario_based_interview",
    llm_config=llm_config,
    system_message=""" You are a helpful mock interviewer that will train the user with case study based interview. 
    Give a scenario based on the user information you get and ask mock interview questions.
    Correct the user answer and continue asking the next question.
    Return 'Terminate' when you have finished the mock interview.""",
)

couch_3 = autogen.ConversableAgent(
    name="Mock_Interviewer",
    llm_config=llm_config,
    system_message="""
    You are a helpful mock interviewer that will train the user with mock interview questions based on the users prefered topic of interest.
    Correct the user answers and continue asking the next interview question with previously corrected answer
    Return 'TERMINATE' when you have finished the mock interview.""",
)

Couch = autogen.ConversableAgent(
    name = "Couch",
    system_message=""" You are a helpful assistant that will take input from the user and then suggest topics that the user might be intrested in learning.
    Return 'TERMINATE' when you have gathered all the information.""",
    llm_config=llm_config,
    code_execution_config={"use_docker": False},
    human_input_mode="NEVER",
)

user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    code_execution_config={"use_docker": False},
    human_input_mode="ALWAYS",
    llm_config = False,
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),
)


chat_results = autogen.initiate_chats( [
     {
            "sender": Couch,
            "recipient": user_proxy,
            "message": "Hello, I'm here to help you get started with your interview preparation."
            "Can you give me information on your professonal background?",
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt": "Summarize the collected personal information as JSON only"
                "{'role': '', 'years_of_experience': '', 'Topic_of_interest': ''}",
            },
            "max_turns": 2,
            "clear_history": False,
        },
         {
            "sender": user_proxy,
            "recipient": couch_3,
            "message": task1[0],
            "summary_method": "reflection_with_llm",
            "max_turns": 5,
            "clear_history": True,
        },
        {
            "sender": user_proxy,
            "recipient": couch_2,
            "message": "Lets begin with a scenario based mock interview",
            "summary_method": "reflection_with_llm",
            "max_turns": 5,
            "clear_history": True,
        },
    
]
)

# print(chat_results)

for chat_result in chat_results:
    pprint.pprint(chat_result.summary)
    pprint.pprint("\n")
