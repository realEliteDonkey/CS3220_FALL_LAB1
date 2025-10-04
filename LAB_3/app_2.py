from src.environmentClass import *
from src.catFriendlyHouse import *
from src.task2_rules import *
from src.agentPrograms import TableDrivenAgentProgram
from src.agentClass import *
import streamlit as st



def AgentStep():
    e1 = st.session_state.e1
    a1 = st.session_state.a1
    
    if e1.is_agent_alive(a1):
        stepActs = e1.step()
        st.session_state.step_count += 1
        
        st.success("Agent decided to do: {}.".format(",".join(stepActs)))
        st.success("Cat Agent is located at {} now.".format(a1.location))
        st.info("Cat Agent performance: {}.".format(a1.performance))
        st.code(e1.status_str())
    else:
        st.error("Agent in location {} and it is dead.".format(a1.location))

def init_env_and_agent():
    e1 = CatFriendlyHouse()
    e1.things = []
    
    a1 = Cat(TableDrivenAgentProgram(feeding_rules))
    e1.add_thing(a1)

    st.session_state.e1 = e1
    st.session_state.a1 = a1
    st.session_state.step_count = 0
    
    

def main():  
    if "e1" not in st.session_state:
        init_env_and_agent()

    e1 = st.session_state.e1
    a1 = st.session_state.a1

    st.title('Table Driven Agent | Task 2')
    st.header("Cat House Environment", divider=True)
 
    st.info(f"{a1} has the performance: {a1.performance}") 
    st.info("Agent in location {}.".format(a1.location))
    st.code(e1.status_str())
    st.button("STEP", on_click=AgentStep)
    st.write("Total steps: ", st.session_state.step_count)

    
    
if __name__ == "__main__":
    main()
    
    
    
    