import streamlit as st
from openai import OpenAI
from CareerAIAgent import MultiAgentCareerSimulator

def main():
    st.set_page_config(page_title="Day in the Life Simulator", page_icon="🎯")
    
    st.title("🎯 Career Day Simulator")
    st.markdown("Experience a day in any career with AI agents")
    
    # Initialize session state
    if 'simulator' not in st.session_state:
        st.session_state.simulator = None
        st.session_state.started = False
        st.session_state.messages = []
    
    # API Key input (sidebar)
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("NVIDIA API Key", type="password", value="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")
        
        if st.button("Reset Simulation"):
            st.session_state.simulator = None
            st.session_state.started = False
            st.session_state.messages = []
            st.rerun()
    
    # Career input
    if not st.session_state.started:
        career = st.text_input("🎬 What career would you like to experience?", placeholder="e.g., Software Engineer, Chef, Doctor")
        
        if st.button("Start Simulation") and career and api_key:
            with st.spinner("🤖 Agents analyzing career..."):
                st.session_state.simulator = MultiAgentCareerSimulator(api_key)
                opening = st.session_state.simulator.start_simulation(career)
                st.session_state.messages.append({"role": "assistant", "content": opening})
                st.session_state.started = True
            st.rerun()
    
    # Display conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # User input
    if st.session_state.started and st.session_state.simulator:
        if st.session_state.simulator.simulation_state["scenarios_completed"] < 5:
            user_input = st.chat_input("💬 What do you do?")
            
            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                with st.spinner("🤖 Agents processing..."):
                    response = st.session_state.simulator.process_user_decision(user_input)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
                st.rerun()
        else:
            st.success("🏆 Career day complete!")
            if st.button("Generate Summary"):
                summary = st.session_state.simulator.generate_summary()
                st.markdown(f"**Career:** {summary['career']}")
                st.markdown(f"**Scenarios:** {summary['scenarios_completed']}")
                st.markdown(f"**Skills:** {', '.join(summary['skills'][:5])}")
                st.markdown(summary['summary'])

if __name__ == "__main__":
    main()