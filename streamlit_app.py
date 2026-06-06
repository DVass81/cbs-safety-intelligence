import pandas as pd
import streamlit as st

st.set_page_config(page_title="CBS Safety Intelligence", page_icon="CBS", layout="wide", initial_sidebar_state="expanded")

DEPTS = pd.DataFrame([
    ["Machine Shop",86,71,12,"A",91],["Assembly",92,42,5,"B",96],["Shipping",74,83,16,"A",82],
    ["Maintenance",79,77,9,"C",84],["Winding",88,49,7,"B",89],["Quality",95,25,2,"A",98],
], columns=["Department","Score","Risk","Hazards","Shift","Training"])
ACTIONS = pd.DataFrame([
    ["CA-1048","Install fixed guard on press brake #4","M. Rivera","Today","Critical","Overdue"],
    ["CA-1051","Retrain Shipping A shift on pedestrian aisles","T. Lewis","Tomorrow","High","Open"],
    ["CA-1057","Verify new eyewash station signage","S. Patel","Jun 10","Medium","Verification"],
    ["CA-1060","Close JHA approval for coil winding setup","A. Chen","Jun 12","Medium","Open"],
], columns=["ID","Action","Owner","Due","Priority","Status"])
TRAINING = pd.DataFrame([
    ["Forklift",88,4,"14 days"],["Crane",94,1,"31 days"],["Lockout/Tagout",86,6,"8 days"],
    ["HazCom",97,0,"72 days"],["PPE",92,2,"21 days"],["Bloodborne Pathogens",81,8,"5 days"],
], columns=["Training","Complete","Overdue","Expires"])
KPI = [("Safety Score","84/100","On track","good"),("Open Hazards","51","12 high risk","warn"),("Near Misses","18","+5 from last month","neutral"),("Overdue Actions","7","3 escalated","critical"),("Training Compliance","91%","Forklift due soon","good"),("JHA Completion","76%","8 jobs missing","warn"),("Incidents This Month","2","1 recordable","critical"),("Risk Trend","-11%","30-day rolling","good")]

st.markdown('''<style>
:root{--navy:#08111f;--steel:#5ea1d8;--green:#34d399;--amber:#f5b84b;--red:#f16063;--muted:#8da0b8}.stApp{background:radial-gradient(circle at top left,rgba(94,161,216,.22),transparent 34rem),var(--navy);color:#edf4ff}[data-testid="stSidebar"]{background:rgba(6,14,26,.92);border-right:1px solid rgba(255,255,255,.1)}h1,h2,h3{letter-spacing:0!important}.hero,.card,.feed,.kpi{padding:18px;border-radius:16px;border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.075);box-shadow:0 24px 70px rgba(0,0,0,.22)}.hero{padding:28px}.hero h1{font-size:clamp(2rem,5vw,4rem);line-height:1;margin:.2rem 0 .7rem}.subtle{color:var(--muted)}.chip{display:inline-flex;align-items:center;min-height:28px;padding:0 10px;margin:4px 6px 4px 0;border-radius:999px;font-size:12px;font-weight:800;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.1)}.good{background:var(--green);color:#063820}.warn{background:var(--amber);color:#3e2700}.critical{background:var(--red);color:#40070a}.kpi{min-height:120px}.kpi strong{display:block;font-size:2rem;line-height:1;margin:.5rem 0}.heat{padding:16px;border-radius:14px;min-height:108px;border:1px solid rgba(255,255,255,.1)}.heat strong,.heat span,.heat small{display:block}.heat span{font-size:1.6rem;font-weight:900;margin:.5rem 0}.hot{background:linear-gradient(135deg,rgba(241,96,99,.95),rgba(118,23,36,.7))}.warm{background:linear-gradient(135deg,rgba(245,184,75,.95),rgba(120,78,12,.62));color:#1b1305}.cool{background:linear-gradient(135deg,rgba(52,211,153,.9),rgba(16,92,85,.62));color:#041d15}.mobile-form{max-width:440px;padding:18px;border-radius:22px;border:1px solid rgba(255,255,255,.12);background:#0b1625}</style>''', unsafe_allow_html=True)

def chip(text,tone=""): return f'<span class="chip {tone}">{text}</span>'
def card(title, text="Production-ready workflow placeholder with mock data."): st.markdown(f'<div class="card"><h3>{title}</h3><p class="subtle">{text}</p></div>', unsafe_allow_html=True)

def dashboard():
    left,right=st.columns([1.55,.85],gap="large")
    with left: st.markdown('''<div class="hero"><p class="subtle"><strong>CBS Safety Intelligence</strong> - A Lean Safety Operating System for Manufacturers</p><h1>What needs attention today</h1><p class="subtle">Plant risk is improving, but Shipping and Machine Shop need action before second shift.</p><span class="chip critical">3 critical actions</span><span class="chip good">91% training compliance</span><span class="chip warn">JHA gap in Winding</span></div>''', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="feed"><h3>AI Safety Feed</h3>', unsafe_allow_html=True)
        for t,a,d,tone in [("8:12 AM","AI flagged repeat pinch-point risk","Machine Shop - press brake #4","critical"),("9:05 AM","LOTO refresher expires for 6 employees","Maintenance and Winding","warn"),("10:22 AM","Corrective action verified","Shipping dock edge guard installed","good"),("11:40 AM","Safe act recognized","Assembly team used stop-and-fix protocol","good")]:
            st.markdown(f"**{t}**  \n{a}  \n<span class='subtle'>{d}</span> {chip(tone.title(),tone)}", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    cols=st.columns(4)
    for i,(label,value,delta,tone) in enumerate(KPI):
        with cols[i%4]: st.markdown(f'<div class="kpi"><span>{label}</span><strong>{value}</strong><span class="{tone}">{delta}</span></div>', unsafe_allow_html=True)
    st.subheader("Department Risk Heat Map")
    cols=st.columns(3)
    for i,r in DEPTS.iterrows():
        tone="hot" if r.Risk>75 else "warm" if r.Risk>55 else "cool"
        with cols[i%3]: st.markdown(f'<div class="heat {tone}"><strong>{r.Department}</strong><span>Risk {r.Risk}</span><small>{r.Hazards} open hazards - Shift {r.Shift}</small></div>', unsafe_allow_html=True)
    st.subheader("Priority Action Center"); st.dataframe(ACTIONS,use_container_width=True,hide_index=True)

def setup():
    st.subheader("Login / Company Setup"); c1,c2=st.columns(2)
    with c1: st.text_input("Company name","CBS Manufacturing"); st.text_area("Locations","Cleveland Plant\nWest Dock\nService Center"); st.multiselect("Departments",DEPTS.Department.tolist(),default=DEPTS.Department.tolist())
    with c2: st.multiselect("Shifts",["A Shift","B Shift","C Shift"],default=["A Shift","B Shift","C Shift"]); st.multiselect("Roles",["Admin","Safety Manager","Supervisor","Team Leader","Employee"],default=["Admin","Safety Manager","Supervisor","Team Leader","Employee"]); st.button("Save company setup",type="primary")

def report():
    st.subheader("Employee Hazard Reporting"); st.markdown('<div class="mobile-form">',unsafe_allow_html=True)
    st.file_uploader("Take/upload photo",type=["png","jpg","jpeg"]); kind=st.segmented_control("Type",["Hazard","Near Miss","Unsafe Act","Safe Act","Improvement Idea"],default="Hazard"); area=st.selectbox("Area / Department",DEPTS.Department.tolist()); note=st.text_area("Optional comment",placeholder="What happened? Keep it simple.")
    if st.button("Submit report",type="primary",use_container_width=True): st.success(f"{kind} submitted for {area}. AI analysis drafted."); ai_analysis(note)
    st.markdown('</div>',unsafe_allow_html=True)

def ai_analysis(context=""):
    st.subheader("AI Hazard Analysis"); c1,c2,c3,c4=st.columns(4); c1.metric("Category","Machine Guarding"); c2.metric("Severity","Serious"); c3.metric("Probability","Likely"); c4.metric("Risk Score","18 / 25")
    st.markdown("""**Recommended immediate containment:** Stop use of the affected equipment or area and barricade exposure until supervisor verification.

**Recommended corrective action:** Install engineered control, update JHA, retrain affected employees, and require before/after photo verification.

**Similar past issues:** HZ-1880, HZ-1934, CA-0941""")

def root_cause():
    st.subheader("AI Root Cause Analysis"); left,right=st.columns([.85,1.15],gap="large")
    with left: st.text_area("Incident summary","Maintenance technician cut left index finger while replacing slitter blade on Winding line 2."); st.selectbox("Injury type",["Laceration","Sprain","Burn","Contusion"]); st.selectbox("Body part",["Hand/finger","Arm","Back","Eye"]); st.text_area("Approved root cause","Blade change method allowed hand exposure during alignment.")
    with right:
        tabs=st.tabs(["5 Why","Fishbone","5M1E","Fault Tree","FMEA","Pareto","Action Plan"]); texts=["Why was hand exposed? No fixture. Why no fixture? Task evolved without JHA update.","Methods, machine guarding, training, material handling, environment, and measurement factors mapped.","Man: new tech. Machine: blade cart gap. Method: informal alignment. Environment: low light.","Top event linked to missing fixture, expired JHA, and incomplete verification.","Highest RPN: manual blade alignment. Recommended control: engineered fixture.","Blade change issues represent 26% of Winding maintenance hazards.","Create fixture, revise JHA, train team, verify with before/after photos."]
        for tab,text in zip(tabs,texts):
            with tab: st.text_area("Editable AI output",text,height=180)
        st.button("Approve AI output",type="primary")

def jha():
    st.subheader("JHA Builder"); task=st.text_input("Job/task name","Press brake tooling change")
    if st.button("AI draft from task name",type="primary"): st.info(f"Drafting JHA for {task}")
    st.data_editor(pd.DataFrame([["Prepare equipment","Slip/trip, pinch point","5S, guarded tooling","Safety glasses"],["Isolate energy","Stored energy","LOTO verification","Cut gloves"],["Remove guard","Sharp edge","Two-person lift","Cut gloves"],["Restore and verify","Unexpected startup","Supervisor check","Standard PPE"]],columns=["Step","Hazards","Controls","PPE"]),use_container_width=True,num_rows="dynamic")

def training(): st.subheader("Training Management"); st.dataframe(TRAINING,use_container_width=True,hide_index=True); st.bar_chart(TRAINING.set_index("Training")["Complete"])
def analytics(): st.subheader("Analytics"); c1,c2=st.columns(2); c1.bar_chart(DEPTS.set_index("Department")[["Risk","Hazards"]]); c2.line_chart(DEPTS.set_index("Department")[["Score","Training"]]); st.dataframe(DEPTS,use_container_width=True,hide_index=True)
def board(title,items): st.subheader(title); cols=st.columns(3); [cols[i%3].markdown(f'<div class="card"><h3>{x}</h3><p class="subtle">Tap to open a production workflow.</p></div>',unsafe_allow_html=True) for i,x in enumerate(items)]

with st.sidebar:
    st.markdown("## CBS Safety Intelligence"); st.caption("Lean Safety OS")
    page=st.radio("Module",["Dashboard","Company Setup","Hazard Reporting","AI Hazard Analysis","Corrective Actions","Incident Investigation","AI Root Cause","JHA Builder","Safety Observations","Training","Lean Safety / QDIPS","Recognition","Analytics","Admin Settings"])

if page=="Dashboard": dashboard()
elif page=="Company Setup": setup()
elif page=="Hazard Reporting": report()
elif page=="AI Hazard Analysis": ai_analysis()
elif page=="Corrective Actions": st.subheader("Corrective Action System"); st.data_editor(ACTIONS,use_container_width=True,hide_index=True)
elif page=="Incident Investigation": board("Incident Investigation",["Incident details","People involved","Injury type","Body part","Location","Photos/documents","Witness notes","Immediate containment","Root cause","Corrective action"])
elif page=="AI Root Cause": root_cause()
elif page=="JHA Builder": jha()
elif page=="Safety Observations": board("Safety Observations",["Safe act","Unsafe act","Coaching conversation","Gemba walk finding","Stop-and-fix action","Improvement suggestion"])
elif page=="Training": training()
elif page=="Lean Safety / QDIPS": board("Lean Safety / QDIPS",["Safety KPI board","Daily safety metric","Pareto symptoms","Action plan","Department scorecards","Blue scheduled indicator"])
elif page=="Recognition": board("Recognition / Engagement",["Hazard submitted +10","Near miss submitted +15","Corrective action completed +20","JHA completed +25","Suggestion implemented +30","Monthly leaderboard"])
elif page=="Analytics": analytics()
elif page=="Admin Settings": board("Admin Settings",["Departments","Users","Roles","Hazard categories","Risk matrix","Notification rules","Training types","Custom safety metrics"])
