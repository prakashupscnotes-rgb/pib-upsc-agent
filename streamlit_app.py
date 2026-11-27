import runpy

# Ensure compatibility whether Streamlit Cloud looks for streamlit_app.py or web_app.py
runpy.run_path("web_app.py")
