from typing import Dict
from autogen.agentchat.agent import Agent
import streamlit as st
import asyncio
from autogen import AssistantAgent, UserProxyAgent, GroupChatManager, GroupChat


st.write("""# AutoGen Chat Agents. Chat TERMINATE when done""")


class TrackableGroupChatManager(GroupChatManager):
    def _process_received_message(self, message: Dict | str, sender: Agent, silent: bool):
        if not message.rstrip().endswith("TERMINATE"):
            with st.chat_message(sender.name):
                st.markdown(message)
        st.session_state["messages"].append((sender.name, message))
        return super()._process_received_message(message, sender, silent)
    
class ModifiedUserProxyAgent(UserProxyAgent):
    def get_human_input(self, prompt: str) -> str:
        while True:
            pass ##Wait forever, or until I find something to do with this.
    
@st.cache_resource
def initiate_agents():
    llm_config = {
        "config_list": [
            {
                "model": "gpt-3.5-turbo",
                "api_key": ""
            }
        ]
    }
    # create an AssistantAgent instance named "assistant"
    assistant = AssistantAgent(
        name="Assistant", llm_config=llm_config,
        system_message="Assistant. Provide support for any questions but code. You do not write code, instead, let the Engineer do it. You do not write code.",)
    
    code_assistant = AssistantAgent(
        name="Engineer", llm_config=llm_config,
        system_message="""Engineer. You follow an approved plan. You write python/shell code to solve tasks, then tell the executor to execute such codes. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
        Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
        If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
        """,
    )

    user_proxy = ModifiedUserProxyAgent(
        name="User", human_input_mode="ALWAYS", code_execution_config={"use_docker": False}, system_message="User. A human admin user.",
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        )
    
    executor = UserProxyAgent(
        name="Executor",
        system_message="Executor. Execute every code written and report the result.",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=5,
        code_execution_config={
            "last_n_messages": 3,
            "work_dir": "coding",
            "use_docker": False,
        }, 
    )
    
    speaker_transitions_dict = {user_proxy: [user_proxy]} #do not force user to repeat

    groupchat = GroupChat(
            agents=[user_proxy, assistant, code_assistant, executor], 
            messages=[], 
            allowed_or_disallowed_speaker_transitions=speaker_transitions_dict,
            speaker_transitions_type="disallowed",
    )
    for agent in groupchat.agents:
        agent.reset()
    manager = TrackableGroupChatManager(groupchat=groupchat, llm_config=llm_config, name="Manager", 
                                        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),)

    return user_proxy, manager

user_proxy, manager = initiate_agents()


st.button("Reset", type="primary")
if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')

with st.container():
    user_input = st.chat_input("Type something...")
    if user_input:
        if not user_input.rstrip().endswith("TERMINATE"):
            for sender_name, message in st.session_state["messages"]:
                with st.chat_message(sender_name):
                    st.markdown(message)
        #user_input delet everything for some reason idk
        user_proxy.send(user_input, manager, True)
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [("Manager", "New Chat. Shall we start?")]
    for sender_name, message in st.session_state["messages"]:
        with st.chat_message(sender_name):
            st.markdown(message)
    #this is for outside widgets that also deletes everything


    

    
        
