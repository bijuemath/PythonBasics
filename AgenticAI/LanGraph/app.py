import streamlit as st

from story_graph import graph


st.set_page_config(
    page_title="LangGraph Story Generator"
)

st.title(
    "Interactive Story Generator"
)


if "started" not in st.session_state:
    st.session_state.started = False

if "state" not in st.session_state:
    st.session_state.state = None


with st.sidebar:

    characters = st.text_area(
        "Characters",
        "Arjun, Maya"
    )

    environment = st.text_area(
        "Environment",
        "Ancient jungle temple"
    )

    max_steps = st.number_input(
        "Story Steps",
        min_value=1,
        max_value=10,
        value=4
    )

    if st.button("Start Story"):

        result = graph.invoke(
            {
                "characters": characters,
                "environment": environment,

                "current_step": 1,
                "max_steps": max_steps,

                "last_choice": "",

                "story_text": "",

                "option1": "",
                "option2": ""
            }
        )

        st.session_state.started = True
        st.session_state.state = result


if st.session_state.started:

    state = st.session_state.state

    st.subheader("Story")

    st.write(
        state["story_text"]
    )

    finished = (
        state["current_step"]
        >=
        state["max_steps"]
    )

    if finished:

        st.success(
            "The Story Has Ended"
        )

    else:

        col1, col2 = st.columns(2)

        with col1:  


            if st.button(
                state["option1"],
                key=f"option1_{state['current_step']}",
                use_container_width=True
            ):

                state["current_step"] += 1
                state["last_choice"] = state["option1"]

                result = graph.invoke(state)

                print(result)

                st.session_state.state = result

                st.rerun()

        with col2:

           if st.button(
            state["option2"],
            key=f"option2_{state['current_step']}",
            use_container_width=True
           ):
                

                state["current_step"] += 1
                state["last_choice"] = state["option2"]

                result = graph.invoke(state)
                print(result)
                st.session_state.state = result

                st.rerun()

                