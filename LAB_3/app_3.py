from src.CompanyEnvironmentClass import CompanyEnvironment
from src.Task3YourClasses import Student, ITStaff, OfficeManager
from src.agents import ReflexAgentA2pro
import streamlit as st


def AgentStep():
    e1 = st.session_state.e1
    a1 = st.session_state.a1
    
    if e1.is_agent_alive(a1):
        stepActs = e1.step()
        st.session_state.step_count += 1
        
        st.success(" Agent decided to do: {}.".format(",".join(stepActs)))
        st.success("DeliveryAgent is located at {} now.".format(a1.location))
        st.info("Current Agent performance: {}.".format(a1.performance))
        st.code(e1.status())
    else:
        st.error("Agent in location {} and it is dead.".format(a1.location))
        
def init_env_and_agent():
    e1 = CompanyEnvironment()
    s = Student()
    i = ITStaff()
    o = OfficeManager()
    a1 = ReflexAgentA2pro()

    e1.things = []
    e1.add_thing(i)
    e1.add_thing(s)
    e1.add_thing(o)
    e1.add_thing(a1)

    st.session_state.e1 = e1
    st.session_state.a1 = a1
    st.session_state.step_count = 0
    
    

def main():  
    if "e1" not in st.session_state:
        init_env_and_agent()

    e1 = st.session_state.e1
    a1 = st.session_state.a1

    st.title('Reflexive Agent | Task 3')
    st.header("Office Environment", divider=True)
 
    st.info(f"{a1} has the performance: {a1.performance}") 
    st.info("Agent in location {}.".format(a1.location))
    st.code(e1.status())
    st.button("STEP", on_click=AgentStep)
    st.write("Total steps: ", st.session_state.step_count)

    
    
if __name__ == "__main__":
    main()
    
    
    
    
    