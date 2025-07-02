import streamlit as st

def enforce_fixed_window_range(max_gesamt_sekunden, min_gesamt_sekunden):
    # Prüfe, ob slider_window_range existiert, sonst abbrechen (z.B. beim ersten Laden)
    if "slider_window_range" not in st.session_state:
        return

    slider_start, slider_end = st.session_state.slider_window_range
    fixed_width = st.session_state.fixed_window_size_s
    max_total_s = max_gesamt_sekunden
    min_total_s = min_gesamt_sekunden
    current_slider_width = slider_end - slider_start

    if abs(current_slider_width - fixed_width) > 0.001:
        if slider_end > max_total_s:
            new_end = max_total_s
            new_start = max(min_total_s, new_end - fixed_width)
        elif slider_start < min_total_s:
            new_start = min_total_s
            new_end = min(max_total_s, new_start + fixed_width)
        elif abs(slider_end - (st.session_state.current_window_start_s + fixed_width)) > abs(slider_start - st.session_state.current_window_start_s):
            new_end = slider_end
            new_start = new_end - fixed_width
            if new_start < min_total_s:
                new_start = min_total_s
                new_end = new_start + fixed_width
        else:
            new_start = slider_start
            new_end = new_start + fixed_width
            if new_end > max_total_s:
                new_end = max_total_s
                new_start = new_end - fixed_width

        st.session_state.current_window_start_s = new_start
        st.session_state.current_window_end_s = new_end

        # Wichtig: slider_window_range synchronisieren, sonst springt der Slider nicht korrekt
        st.session_state.slider_window_range = (new_start, new_end)
    else:
        st.session_state.current_window_start_s = slider_start
        st.session_state.current_window_end_s = slider_end