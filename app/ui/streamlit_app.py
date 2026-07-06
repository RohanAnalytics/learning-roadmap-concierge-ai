    import sys
    from pathlib import Path

    # Add the project root to Python's module search path
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))


    from app.agents.planner_agent import PlannerAgent
    from app.agents.resource_agent import ResourceAgent
    from app.agents.quiz_agent import QuizAgent
    from app.agents.progress_agent import ProgressAgent
    from app.agents.analytics_agent import AnalyticsAgent
    from tools.profile_tool import ProfileTool
    from tools.progress_storage_tool import ProgressStorageTool
    from tools.analytics_tool import AnalyticsTool
    from config.constants import DEFAULT_USER

    import streamlit as st

    st.set_page_config(
        page_title="Learning Roadmap Concierge AI",
        page_icon="🎓",
        layout="wide",
    )
    planner = PlannerAgent()
    resource_agent = ResourceAgent()
    quiz_agent = QuizAgent()
    progress_agent = ProgressAgent()
    analytics_agent = AnalyticsAgent()
    profile_tool = ProfileTool()
    progress_storage_tool = ProgressStorageTool()
    analytics_tool = AnalyticsTool()

    # ----------------------------
    # Sidebar
    # ----------------------------

    st.sidebar.title("🎓 Learning Roadmap Concierge AI")

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "🗺️ Roadmap",
            "📚 Resources",
            "📝 Quiz",
            "📈 Progress",
            "📊 Analytics",
            "👤 Profile",
        ],
    )

    # ----------------------------
    # Home
    # ----------------------------

    if page == "🏠 Home":

        st.title("🎓 Learning Roadmap Concierge AI")

        st.write(
            "Welcome to your personal AI learning assistant."
        )

        analytics = analytics_tool.analyze(DEFAULT_USER)

        if analytics:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Goal",
                    analytics["goal"]
                )

            with col2:
                st.metric(
                    "Completion",
                    f"{analytics['completion']}%"
                )

            with col3:
                st.metric(
                    "Next Topic",
                    analytics["next_topic"]
                )

            st.divider()

            st.subheader("Current Phase")

            st.success(analytics["phase"])

            st.subheader("AI Recommendation")

            st.info(
                analytics["recommendation"]
            )

        else:

            st.info(
                "Generate your first roadmap to begin learning."
            )

    # ----------------------------
    # Placeholder Pages
    # ----------------------------

    elif page == "🗺️ Roadmap":

        st.title("🗺️ AI Learning Roadmap")

        goal = st.text_input(
            "Learning Goal",
            placeholder="Example: Machine Learning",
        )

        weeks = st.slider(
            "Duration (Weeks)",
            min_value=4,
            max_value=52,
            value=12,
        )

        if st.button("Generate Roadmap"):

            if not goal.strip():

                st.warning("Please enter a learning goal.")

            else:

                with st.spinner("Generating roadmap..."):

                    try:

                        roadmap = planner.process(goal, weeks=weeks)

                        st.success("Roadmap Generated!")

                        st.markdown(roadmap)

                    except Exception as e:

                        st.error(str(e))

    elif page == "📚 Resources":

        st.title("📚 Learning Resources")

        profile = planner.profile.get_profile(DEFAULT_USER)

        if not profile:

            st.warning("Please generate a roadmap first.")

        else:

            goal = profile.get("goal", "")

            st.info(f"Current Learning Goal: **{goal}**")

            if st.button("Get Recommended Resources"):

                with st.spinner("Finding the best learning resources..."):

                    try:

                        resources = resource_agent.process("resources")

                        st.success("Resources Generated!")

                        st.markdown(resources)

                    except Exception as e:

                        st.error(str(e))

    elif page == "📝 Quiz":

        st.title("📝 AI Quiz")

        st.write(
            "Generate a quiz based on your current learning progress."
        )

        if st.button("Generate Quiz"):

            with st.spinner("Creating quiz..."):

                try:

                    quiz = quiz_agent.process("quiz")

                    st.success("Quiz Generated!")

                    st.markdown(quiz)

                except Exception as e:

                    st.error(str(e))

    elif page == "📈 Progress":

        st.title("📈 Learning Progress")

        st.write(
            "Track your learning journey and update completed topics."
        )

        try:

            profile = progress_agent.profile.get_profile(DEFAULT_USER)

            if not profile:

                st.warning(
                    "Please generate a roadmap first."
                )

            else:

                goal = profile.get("goal")

                progress = progress_agent.storage.get_progress(DEFAULT_USER)

                course = progress.get(goal, {})

                completed = course.get("completed", [])

                remaining = course.get("remaining", [])

                st.subheader("Current Goal")

                st.success(goal)

                st.metric(
                    "Completed Topics",
                    len(completed),
                )

                st.metric(
                    "Remaining Topics",
                    len(remaining),
                )

                st.divider()

                st.subheader("Completed")

                if completed:

                    for topic in completed:

                        st.success(f"✅ {topic}")

                else:

                    st.info("No completed topics yet.")

                st.divider()

                st.subheader("Remaining")

                if remaining:

                    selected_topic = st.selectbox(

                        "Choose topic to mark completed",

                        remaining,

                    )

                    if st.button("Mark Completed"):

                        message = progress_agent.process(
                            f"complete {selected_topic}"
                        )

                        st.success(message)

                        st.rerun()

                else:

                    st.success(
                        "🎉 Congratulations! Roadmap completed."
                    )

        except Exception as e:

            st.error(str(e))

    elif page == "📊 Analytics":

        st.title("📊 Learning Analytics")

        st.write(
            "View your current learning performance."
        )

        try:

            analytics = analytics_agent.tool.analyze(DEFAULT_USER)

            if analytics is None:

                st.warning(
                    "Please generate a roadmap first."
                )

            else:

                st.metric(
                    "Completion",
                    f"{analytics['completion']}%"
                )

                st.metric(
                    "Current Phase",
                    analytics["phase"]
                )

                st.metric(
                    "Next Topic",
                    analytics["next_topic"]
                )

                st.metric(
                    "Completed",
                    analytics["completed_count"]
                )

                st.metric(
                    "Remaining",
                    analytics["remaining_count"]
                )

                st.divider()

                st.subheader("Goal")

                st.success(
                    analytics["goal"]
                )

                st.subheader("AI Learning Insights")

                st.markdown(
                    analytics["insights"]
                )

                st.subheader("Recommendation")

                st.info(
                    analytics["recommendation"]
                )

                st.subheader("Recommended Pace")

                st.success(
                    analytics["recommended_pace"]
                )

        except Exception as e:

            st.error(str(e))

    elif page == "👤 Profile":

        st.title("👤 Learner Profile")

        profile = profile_tool.get_profile(DEFAULT_USER)

        if not profile:

            st.warning(
                "No learner profile found.\n\nGenerate a roadmap first."
            )

        else:

            st.subheader("Learning Goal")

            st.success(profile.get("goal", "Not Set"))

            st.subheader("Current Level")

            st.info(
                profile.get(
                    "current_level",
                    "Unknown"
                )
            )

            st.subheader("Recommended Level")

            st.info(
                profile.get(
                    "recommended_level",
                    "Unknown"
                )
            )

            st.subheader("Known Skills")

            skills = profile.get(
                "skills",
                []
            )

            if skills:

                for skill in skills:

                    st.write(f"✅ {skill}")

            else:

                st.write("No known skills detected.")

            st.subheader("Missing Skills")

            missing = profile.get(
                "missing_skills",
                []
            )

            if missing:

                for skill in missing:

                    st.write(f"🔹 {skill}")

            else:

                st.write("None")

            st.subheader("Progress")

            st.metric(
                "Completed Topics",
                profile.get(
                    "completed_topics",
                    0
                )
            )

            st.metric(
                "Total Topics",
                profile.get(
                    "total_topics",
                    0
                )
            )