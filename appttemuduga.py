import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Flashcard Temuduga",
    page_icon="📋",
    layout="wide"
)

# =====================
# BACA EXCEL
# =====================

df = pd.read_excel("Soalan Penemuduga.xlsx")

DIMENSION_INFO = {

    "Komunikasi": {
        "weight": "30%",
        "description": "Penilaian kejelasan, kelancaran dan keberkesanan komunikasi lisan dan bukan lisan."
    },

    "Pengetahuan": {
        "weight": "10%",
        "description": "Penilaian pengetahuan am, pengetahuan bidang dan kepekaan terhadap soalan."
    },

    "Penguasaan Bahasa": {
        "weight": "10%",
        "description": "Penilaian kemahiran dalam bahasa utama dan bahasa kedua."
    },

    "Personaliti dan Sahsiah": {
        "weight": "20%",
        "description": "Penilaian penampilan, kesopanan dan motivasi calon."
    },

    "Kepimpinan dan Ketrampilan": {
        "weight": "30%",
        "description": "Penilaian penglibatan dalam aktiviti dan kemahiran tambahan."
    }

}

# =====================
# SESSION
# =====================

if "status" not in st.session_state:

    st.session_state.status = {}

    for idx in df.index:
        st.session_state.status[idx] = False

if "current" not in st.session_state:

    st.session_state.current = {}

    for dim in df["Dimensi"].unique():
        st.session_state.current[dim] = 0

# =====================
# DASHBOARD
# =====================

st.title("📋 Flashcard Temuduga")

total = len(df)

completed = sum(
    st.session_state.status.values()
)

progress = completed / total

st.subheader("Dashboard Keseluruhan")

st.progress(progress)

c1, c2, c3 = st.columns(3)

c1.metric("Jumlah Soalan", total)
c2.metric("Telah Ditanya", completed)
c3.metric("Belum Ditanya", total-completed)

st.divider()

# =====================
# TABS
# =====================

dimensions = list(df["Dimensi"].unique())

tabs = st.tabs(dimensions)

for tab_idx, dimensi in enumerate(dimensions):

    with tabs[tab_idx]:

        data = df[df["Dimensi"] == dimensi].reset_index()

        info = DIMENSION_INFO.get(
            dimensi,
            {"weight":"-", "description":"-"}
        )

        st.info(
            f"""
            📊 Pemberat: {info['weight']}

            📝 {info['description']}
            """
        )

        current = st.session_state.current[dimensi]

        row = data.iloc[current]

        real_index = row["index"]

        asked = sum(
            st.session_state.status[idx]
            for idx in data["index"]
        )

        percent = asked / len(data)

        c1, c2, c3 = st.columns(3)

        c1.metric("Telah Ditanya", asked)
        c2.metric("Belum Ditanya", len(data)-asked)
        c3.metric("Kemajuan", f"{percent*100:.0f}%")

        st.progress(percent)

        done = st.session_state.status[real_index]

        color = "#d4edda" if done else "#ffffff"

        st.markdown(
            f"""
            <div style="
                background:{color};
                padding:30px;
                border-radius:15px;
                border-left:8px solid #1f77b4;
                margin-top:20px;
            ">
                <h3>{row['No. Soalan']}</h3>
                <p style="font-size:22px;">
                    {row['Soalan']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            f"**Soalan {current+1} daripada {len(data)}**"
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            if st.button(
                "⬅ Sebelumnya",
                key=f"prev_{dimensi}"
            ):
                if current > 0:
                    st.session_state.current[dimensi] -= 1
                    st.rerun()

        with col2:
            if st.button(
                "➡ Seterusnya",
                key=f"next_{dimensi}"
            ):
                if current < len(data)-1:
                    st.session_state.current[dimensi] += 1
                    st.rerun()

        with col3:
            if st.button(
                "✅ Tandakan Ditanya",
                key=f"done_{real_index}"
            ):
                st.session_state.status[real_index] = True
                st.rerun()

        with col4:
            if st.button(
                "❌ Batalkan",
                key=f"undo_{real_index}"
            ):
                st.session_state.status[real_index] = False
                st.rerun()

        with col5:
            if st.button(
                "🎲 Rawak",
                key=f"random_{dimensi}"
            ):
                import random

                st.session_state.current[dimensi] = random.randint(
                    0,
                    len(data)-1
                )
                st.rerun()

        st.divider()

        st.subheader("Senarai Soalan")

        cols = st.columns(4)

        for i, r in enumerate(data.itertuples()):

            icon = "✅" if st.session_state.status[r.index] else "⬜"

            if cols[i % 4].button(
                f"{icon} {r[2]}",
                key=f"jump_{dimensi}_{i}"
            ):
                st.session_state.current[dimensi] = i
                st.rerun()

# =====================
# RESET
# =====================

st.divider()

if st.button("🔄 RESET SEMUA"):

    for k in st.session_state.status:
        st.session_state.status[k] = False

    st.rerun()
