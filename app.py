import streamlit as st
import pandas as pd
from core.models import Process
from algorithms import ALGORITHMS
from data.sample_data import DATASETS
from visualization.charts import plot_gantt_chart, plot_comparison_bar_chart

st.set_page_config(
    page_title="GanttMaster: CPU Scheduling Visualizer",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS for clean, academic look
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #1E293B;
    }
    .stButton>button {
        background-color: #3b5998;
        color: white;
        border-radius: 4px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2d4373;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def render_sidebar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Simulation", "Algorithm Comparison", "Algorithm Guide"])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**COOS Mini Project**")
    st.sidebar.markdown("**GanttMaster**")
    
    return page

def get_session_state_processes():
    if 'processes' not in st.session_state:
        st.session_state.processes = DATASETS["Basic"]()
    return st.session_state.processes

def render_home():
    st.title("GanttMaster")
    st.markdown("### CPU Scheduling Visualizer")
    
    st.markdown("---")
    st.markdown("""
    Welcome to **GanttMaster**, a technical simulation tool built for analyzing how operating systems manage process execution.
    
    ### Available Algorithms
    - **FCFS** (First Come First Serve)
    - **SJF** (Shortest Job First)
    - **SRTF** (Shortest Remaining Time First)
    - **Priority Scheduling**
    - **Round Robin**
    
    ### Features
    - **Simulation:** Configure process workloads and visualize execution via Gantt charts.
    - **Comparison:** Run identical workloads through multiple algorithms to analyze performance metrics like Waiting Time and Turnaround Time.
    
    Use the sidebar to navigate to the **Simulation** or **Algorithm Comparison** sections to begin.
    """)

def render_process_input():
    st.subheader("Workload Configuration")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Load Sample Dataset**")
        sample_choice = st.selectbox("Select Sample", list(DATASETS.keys()))
        if st.button("Load Dataset"):
            st.session_state.processes = DATASETS[sample_choice]()
            st.rerun()
            
    with col2:
        st.markdown("**Add Custom Process**")
        with st.form("add_process_form", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns(4)
            pid = c1.text_input("Process ID", value=f"P{len(get_session_state_processes())+1}")
            at = c2.number_input("Arrival Time", min_value=0, step=1, value=0)
            bt = c3.number_input("Burst Time", min_value=1, step=1, value=1)
            priority = c4.number_input("Priority", min_value=1, step=1, value=1)
            
            submitted = st.form_submit_button("Add Process")
            if submitted:
                if any(p.pid == pid for p in st.session_state.processes):
                    st.error(f"Process ID '{pid}' already exists.")
                else:
                    st.session_state.processes.append(Process(pid, int(at), int(bt), int(priority)))
                    st.rerun()
                    
    if st.button("Clear All Processes"):
        st.session_state.processes = []
        st.rerun()
        
    processes = get_session_state_processes()
    if processes:
        df_input = pd.DataFrame([vars(p) for p in processes])
        df_input.columns = ["Process ID", "Arrival Time", "Burst Time", "Priority"]
        st.dataframe(df_input, use_container_width=True, hide_index=True)
    else:
        st.warning("No processes defined. Please add processes or load a sample dataset.")
        
    return processes

def render_simulation():
    st.title("Simulation Engine")
    processes = render_process_input()
    
    if not processes:
        return
        
    st.markdown("---")
    st.subheader("Algorithm Selection")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        algo_name = st.selectbox("Select Algorithm", list(ALGORITHMS.keys()))
        
    tq = 2
    if algo_name == "Round Robin":
        with col2:
            tq = st.number_input("Time Quantum", min_value=1, step=1, value=2)
            
    animate = st.checkbox("Step-by-step Animation", value=False)
            
    if st.button("Run Simulation", type="primary"):
        run_simulation(processes, algo_name, tq, animate)

def run_simulation(processes, algo_name, tq, animate=False):
    algo_func = ALGORITHMS[algo_name]
    
    # Deep copy processes to avoid mutating state
    import copy
    processes_copy = copy.deepcopy(processes)
    
    try:
        result = algo_func(processes_copy, tq=tq)
    except Exception as e:
        st.error(f"An error occurred during simulation: {e}")
        return
        
    st.markdown("---")
    st.subheader("Gantt Chart")
    
    if animate:
        import time
        import matplotlib.pyplot as plt
        chart_placeholder = st.empty()
        max_time = result.gantt[-1].end_time if result.gantt else 0
        current_segments = []
        
        for segment in result.gantt:
            current_segments.append(segment)
            fig = plot_gantt_chart(current_segments, max_time=max_time)
            chart_placeholder.pyplot(fig)
            time.sleep(0.6)
            plt.close(fig)
    else:
        fig = plot_gantt_chart(result.gantt)
        st.pyplot(fig)
    
    st.subheader("Process Metrics")
    df_metrics = pd.DataFrame([vars(m) for m in result.processes])
    df_metrics.columns = ["Process ID", "Arrival Time", "Burst Time", "Priority", 
                          "Completion Time", "Turnaround Time", "Waiting Time", "Response Time"]
    st.dataframe(df_metrics, use_container_width=True, hide_index=True)
    
    st.subheader("Overall Performance")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Avg Waiting Time", f"{result.avg_wt:.2f}")
    c2.metric("Avg Turnaround", f"{result.avg_tat:.2f}")
    c3.metric("Avg Response Time", f"{result.avg_rt:.2f}")
    c4.metric("CPU Util.", f"{result.cpu_utilization:.2f}%")
    c5.metric("Throughput", f"{result.throughput:.2f}/u")
    c6.metric("Idle Time", f"{result.idle_time}")

def render_comparison():
    st.title("Algorithm Comparison")
    processes = render_process_input()
    
    if not processes:
        return
        
    st.markdown("---")
    tq = st.number_input("Round Robin Time Quantum (for comparison)", min_value=1, step=1, value=2)
    
    if st.button("Compare All Algorithms", type="primary"):
        import copy
        results = []
        
        for name, func in ALGORITHMS.items():
            p_copy = copy.deepcopy(processes)
            res = func(p_copy, tq=tq)
            results.append({
                "Algorithm": name,
                "Avg WT": res.avg_wt,
                "Avg TAT": res.avg_tat,
                "Avg RT": res.avg_rt,
                "CPU Util (%)": res.cpu_utilization,
                "Throughput": res.throughput
            })
            
        df_comp = pd.DataFrame(results)
        
        st.subheader("Comparison Table")
        st.dataframe(df_comp, use_container_width=True, hide_index=True)
        
        st.subheader("Performance Graphs")
        c1, c2 = st.columns(2)
        
        with c1:
            fig_wt = plot_comparison_bar_chart(df_comp, "Avg WT", "Average Waiting Time (Lower is Better)", "Time Units")
            st.pyplot(fig_wt)
            
            fig_rt = plot_comparison_bar_chart(df_comp, "Avg RT", "Average Response Time (Lower is Better)", "Time Units")
            st.pyplot(fig_rt)
            
        with c2:
            fig_tat = plot_comparison_bar_chart(df_comp, "Avg TAT", "Average Turnaround Time (Lower is Better)", "Time Units")
            st.pyplot(fig_tat)
            
            fig_cpu = plot_comparison_bar_chart(df_comp, "CPU Util (%)", "CPU Utilization (Higher is Better)", "Percentage")
            st.pyplot(fig_cpu)
            
        st.subheader("Result Interpretation")
        best_wt = df_comp.loc[df_comp['Avg WT'].idxmin()]
        best_tat = df_comp.loc[df_comp['Avg TAT'].idxmin()]
        best_rt = df_comp.loc[df_comp['Avg RT'].idxmin()]
        
        interpretation = f"""
        Based on the current workload:
        - **{best_wt['Algorithm']}** achieved the lowest Average Waiting Time ({best_wt['Avg WT']:.2f}).
        - **{best_tat['Algorithm']}** achieved the lowest Average Turnaround Time ({best_tat['Avg TAT']:.2f}).
        - **{best_rt['Algorithm']}** provides the fastest initial response, with an Average Response Time of {best_rt['Avg RT']:.2f}.
        
        *Note: If multiple algorithms yield the exact same minimum value, the first evaluated one is listed. No single algorithm is universally optimal for all possible workloads.*
        """
        st.info(interpretation)

def render_guide():
    st.title("Algorithm Guide")
    
    st.markdown("""
    ### FCFS (First Come First Serve)
    - **Type**: Non-preemptive
    - **Principle**: Processes are scheduled strictly in the order they arrive.
    - **Advantage**: Simple to implement and understand.
    - **Limitation**: Suffers from the "Convoy Effect" where short processes wait a long time for a long process to finish.
    
    ### SJF (Shortest Job First)
    - **Type**: Non-preemptive
    - **Principle**: Selects the process with the shortest burst time among those available in the ready queue.
    - **Advantage**: Provably optimal for minimizing average waiting time.
    - **Limitation**: Cannot be implemented exactly since burst times are rarely known in advance. Can cause starvation of longer processes.
    
    ### SRTF (Shortest Remaining Time First)
    - **Type**: Preemptive
    - **Principle**: The preemptive version of SJF. If a new process arrives with a shorter burst time than what is remaining of the current process, the current process is preempted.
    - **Advantage**: Extremely responsive and provides lowest average waiting time.
    - **Limitation**: High overhead due to context switching; starvation of long processes is still an issue.
    
    ### Priority Scheduling
    - **Type**: Non-preemptive
    - **Principle**: Each process is assigned a priority. The CPU is allocated to the highest priority process (lowest numerical value).
    - **Advantage**: Allows the system to prioritize critical tasks.
    - **Limitation**: Lower priority processes may suffer from starvation (often mitigated by aging).
    
    ### Round Robin
    - **Type**: Preemptive
    - **Principle**: Each process is given a small, fixed unit of CPU time (time quantum). After this time has elapsed, the process is preempted and added to the back of the ready queue.
    - **Advantage**: Excellent for timesharing systems, ensuring fair CPU allocation and good response times.
    - **Limitation**: Performance heavily depends on the size of the time quantum. If too large, it degrades to FCFS. If too small, context switching overhead dominates.
    """)

def main():
    page = render_sidebar()
    
    if page == "Home":
        render_home()
    elif page == "Simulation":
        render_simulation()
    elif page == "Algorithm Comparison":
        render_comparison()
    elif page == "Algorithm Guide":
        render_guide()

if __name__ == "__main__":
    main()
